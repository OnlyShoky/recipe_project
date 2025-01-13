from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Course, Cuisine, Recipe, Tag
from .serializers import RecipeSerializer
from ingredients.models import Ingredient

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

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
    # Get all recipes, ordered by activation date
    recipes = Recipe.objects.order_by('-created')
    
    # Set up pagination: 6 recipes per page
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the current page of recipes

    context = {
        'recipes': page_obj,  # Pass the page object to the template
        'title': 'All Recipes',  # Dynamic title for the page
    }
    return render(request, 'recipes/recipe_list.html', context)

def recipe_cuisine(request, cuisine_name):
    # Filter recipes by the given cuisine name
    cuisine = get_object_or_404(Cuisine, name=cuisine_name)
    recipes = Recipe.objects.filter(cuisines=cuisine).order_by('-created')
    # Set up pagination: 6 recipes per page
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the current page of recipes
    title = f"{cuisine_name} Recipes"

    context = {
        'recipes': page_obj,  # Pass the page object to the template
        'cuisine_name': cuisine_name,  # Pass the selected cuisine name
        'title': title,  # Dynamic title for the page
    }
    return render(request, 'recipes/recipe_cuisine.html', context)

def home(request):
    # Fetch the last 5 recipes ordered by the activate_date
    recipes = Recipe.objects.all().order_by('-created')[:6]
    ingredients = Ingredient.objects.all().order_by('-created')[:6]
    cuisines = Cuisine.objects.all().order_by('-created')
    tags = Tag.objects.all().order_by('-created')
    courses = Course.objects.all().order_by('-created')
    total_recipes = Recipe.objects.count()
    total_ingredients = Ingredient.objects.count()
    return render(request, 'home.html', {'recipes': recipes, 'cuisines': cuisines, 'tags': tags, 'courses': courses, 'ingredients': ingredients,  'total_recipes': total_recipes, 'total_ingredients': total_ingredients})



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