from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.exceptions import NotFound
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle



from django.shortcuts import render, get_object_or_404
from recipes.models import Recipe

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
    # Fetch the last 5 recipes ordered by the activate_date
    recipes = Recipe.objects.all().order_by('-created',)[:6]
    return render(request, 'recipe_list.html', {'recipes': recipes})

def home(request):
    # Fetch the last 5 recipes ordered by the activate_date
    recipes = Recipe.objects.all().order_by('-created')[:6]
    return render(request, 'home.html', {'recipes': recipes})

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