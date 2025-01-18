from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Course, Cuisine, Recipe, RecipeIngredient, Tag
from .serializers import RecipeSerializer
from ingredients.models import Ingredient

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from collections import Counter

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    
    recipe.notes_list = recipe.notes.split('\n') if recipe.notes else []
    recipe.equipment_list = recipe.equipment.split('\n') if recipe.equipment else []
    recipe.instructions_list = recipe.instructions.split('\n') if recipe.instructions else []
    
    recipe.ingredientsCategories = set()
    
                
    for i,instruction in enumerate(recipe.instructions_list) :
        if 'GroupName' in instruction :
            recipe.instructions_list[i] = recipe.instructions_list[i].replace('GroupName :', '')
            if ':' not in instruction :
                recipe.instructions_list[i] += ':'
                
    for ingredient in recipe.ingredients :
        recipe.ingredientsCategories.add(ingredient.groupName)

        
    # recipe.instructions = recipe.instructions.split('\n')
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def recipe_list(request):
    cuisine_name = request.GET.get('cuisine')
    course_name = request.GET.get('course')
    tag_name = request.GET.get('tag')
    ingredient_name = request.GET.get('ingredient')

    recipes = Recipe.objects.all()
    
    title_parts = ['All']

    if cuisine_name:
        cuisine_name = cuisine_name.replace('-', ' ')
        recipes = recipes.filter(cuisines__name__iexact=cuisine_name)
        title_parts.append(f"{cuisine_name.capitalize()}")
        title_parts.remove('All') if 'All' in title_parts else None
    if course_name:
        course_name = course_name.replace('-', ' ')
        recipes = recipes.filter(courses__name__iexact=course_name)
        title_parts.append(f"{course_name.capitalize()}")
        title_parts.remove('All') if 'All' in title_parts else None
    title_parts.append('Recipes')
    if tag_name:
        tag_name = tag_name.replace('-', ' ')
        recipes = recipes.filter(tags__name__iexact=tag_name)
        title_parts.append(f'tagged with "{tag_name}"')
        
    if ingredient_name:
        ingredient_name = ingredient_name.replace('-', ' ')
        recipesCopy = recipes.filter(recipe_ingredients__ingredient__name__iexact=ingredient_name).distinct()
        
        # if no recipes were found in cases like 'all-purpose flour'
        if not recipesCopy :
            allIngredients = Ingredient.objects.all()
            for i in allIngredients :
                if i.name.replace('-', ' ') == ingredient_name :
                    recipesCopy = recipes.filter(recipe_ingredients__ingredient__name__iexact=i.name).distinct()
                    ingredient_name = i.name
                    break
            
        recipes = recipesCopy
        title_parts.append(f'that contains "{ingredient_name}"')
 
            
    title = '  '.join(title_parts)

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
    # Fetch the last 5 recipes ordered by the activate_date
    recipes = Recipe.objects.all().order_by('-created')[:6]
    ingredients = Ingredient.objects.all().order_by('-created')[:6]
        
    ingredients = [recipeIngredient.ingredient for recipeIngredient in RecipeIngredient.objects.all()]
    ingredients = [ingredient[0] for ingredient in Counter(ingredients).most_common(6)]
    
    cuisines = Cuisine.objects.all().order_by('-created')
    tags = Tag.objects.all().order_by('-created')
    courses = Course.objects.all().order_by('-created')
    total_recipes = Recipe.objects.count()
    total_ingredients = Ingredient.objects.count()
    return render(request, 'home.html', {'recipes': recipes,   'cuisines': cuisines, 'tags': tags, 'courses': courses, 'ingredients': ingredients,  'total_recipes': total_recipes, 'total_ingredients': total_ingredients})



## API VIEWS

class RecipeAPIView(views.APIView):
    """
    APIView to retrieve a list of the last 5 recipes added.
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
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