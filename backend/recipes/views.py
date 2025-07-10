from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Course, Cuisine, Recipe, RecipeIngredient, Tag
from .serializers import RecipeSerializer
from ingredients.models import Ingredient

from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count


from collections import Counter
import re
import time

def contact_view(request):
    return render(request, 'contact.html')

def faq_view(request):
    return render(request, 'faq.html')

def about_view(request):
    return render(request, 'about.html')

def preepweek_view(request):
    recipes = Recipe.objects.all().order_by('-created')[:8]

    return render(request, 'preepweek.html', {'recipes': recipes })



def search_recipes(request):
    query = request.GET.get('q')  # Get the search query from the request
    recipes = Recipe.objects.all()  # Default: show all recipes

    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) 
        )
        
    if recipes.count() == 1:
        recipe = recipes.first()
        return redirect('recipe_detail', recipe.id)
    
    paginator = Paginator(recipes, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Rebuild the query string excluding 'page'
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()

    context = {
        'recipes': page_obj,
        'query_string': query_string
    }
    return render(request, 'search_results.html', context)

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    
    recipe.notes_list = recipe.notes.split('\n') if recipe.notes else []
    recipe.equipment_list = recipe.equipment.split('\n') if recipe.equipment else []
    recipe.instructions_list = recipe.instructions.split('\n') if recipe.instructions else []
    
    recipe.ingredientsCategories = set()
    recipe.hasCategories = False
    
                

    # Initialize a new list to store the processed instructions
    processed_instructions = []
    step_number = 1  # Counter for instructions without a pre-existing number

    # Define the regex pattern to capture step numbers at the beginning of the instruction
    numbered_step_pattern = r"^\s*(\d+)\.\s*(.*)$"  # Matches "1. Text"

    for instruction in recipe.instructions_list:
        # Check if the instruction is a group header
        if 'GroupName' in instruction:
            # Process and format the group name
            group_name = instruction.replace('GroupName :', '').strip()
            if ':' not in group_name:
                group_name += ':'
            # Append group name to the processed list with None as the number
            processed_instructions.append((None, group_name))
        else:
            # Check if the instruction is numbered using regex
            match = re.match(numbered_step_pattern, instruction)
            if match:
                # Extract the number and the text
                number = int(match.group(1))
                text = match.group(2).strip()
                processed_instructions.append((number, text))
            else:
                # If not numbered, assign the next step_number and increment it
                processed_instructions.append((step_number, instruction.strip()))
                step_number += 1

    # Update the recipe.instructions_list with the processed instructions
    recipe.instructions_list = processed_instructions



                
    for ingredient in recipe.ingredients :
        if ingredient.groupName:
            recipe.ingredientsCategories.add(ingredient.groupName)

        
    # recipe.instructions = recipe.instructions.split('\n')
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def recipe_list(request):
    cuisine_name = request.GET.get('cuisine')
    course_name = request.GET.get('course')
    tag_name = request.GET.get('tag')
    ingredient_name = request.GET.get('ingredient')

    recipes = Recipe.objects.all()
    
    filters = Q()  # Start with an empty query filter
    
    title_parts = ['All']


    if cuisine_name:
        filters &= Q(cuisines__name__iexact=cuisine_name)
        title_parts.append(f"{cuisine_name.capitalize()}")
        title_parts.remove('All') if 'All' in title_parts else None
    if course_name:
        filters &= Q(courses__name__iexact=course_name)
        title_parts.append(f"{course_name.capitalize()}")
        title_parts.remove('All') if 'All' in title_parts else None
    title_parts.append('Recipes')
    if tag_name:
        filters &= Q(tags__name__iexact=tag_name)
        title_parts.append(f'tagged with "{tag_name}"')
        
    if ingredient_name:
        filters &= Q(recipe_ingredients__ingredient__name__iexact=ingredient_name)
        
        title_parts.append(f'that contains "{ingredient_name}"')
 
            
    title = '  '.join(title_parts)
    
    recipes = recipes.filter(filters).distinct()

    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Rebuild the query string excluding 'page'
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()

    context = {
        'recipes': page_obj,
        'title': title,
        'query_string': query_string,
    }
    return render(request, 'recipes/recipe_list.html', context)





def home(request):
    start = time.perf_counter()
    # Fetch the last 5 recipes ordered by the activate_date
    recipes = Recipe.objects.all().order_by('-created')[:8]
    ingredients = (
        RecipeIngredient.objects.values('ingredient__name')
        .annotate(count=Count('ingredient'))
        .order_by('-count')[:8]  # Get the top 8 most common ingredients
    )
    ingredients = [ingredient['ingredient__name'] for ingredient in ingredients]

    
    tags = Tag.objects.all()
    cuisines = Cuisine.objects.all()
    courses = Course.objects.all()
    total_recipes = Recipe.objects.count()
    total_ingredients = Ingredient.objects.count()
    
    print(f" total time took {time.perf_counter() - start:.5f} seconds")
    return render(request, 'home.html', {'recipes': recipes,   'cuisines': cuisines, 'tags': tags, 'courses': courses, 'ingredients': ingredients,  'total_recipes': total_recipes, 'total_ingredients': total_ingredients})



## API VIEWS



class RecipeSearchAPIView(views.APIView):
    """
    APIView to retrieve a list of recipes with filtering options.
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')  
        cuisine = request.GET.get('cuisine') 
        course = request.GET.get('course')  
        tag = request.GET.get('tag')  
        limit = min(10,int(request.GET.get('limit', 10)))  # Agregué límite con valor por defecto
        offset = int(request.GET.get('offset', 0))  # Agregué paginación

        recipes = Recipe.objects.all()  

        filters = Q()  

        if cuisine:
            filters &= Q(cuisines__name__iexact=cuisine)

        if course:
            filters &= Q(courses__name__iexact=course)

        if tag:
            filters &= Q(tags__name__iexact=tag)

        if search:
            filters &= Q(title__icontains=search)

        recipes = recipes.filter(filters)[offset:offset + limit]  # Aplicando paginación

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeAPIView(views.APIView):
    """
    APIView to retrieve a list of the last 5 recipes added.
    
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    testeo = "hola"
    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.all().order_by('created')[:5]  # Fetch last 5 recipes
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RecipeDetailAPIView(views.APIView):
    """
    APIView to retrieve a single recipe by ID.
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def get(self, request, id, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=id)  # Fetch recipe by ID
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            raise NotFound("Recipe not found")