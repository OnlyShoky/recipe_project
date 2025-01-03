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
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def recipe_list(request):
    # Fetch the last 5 recipes ordered by the activate_date
    recipes = Recipe.objects.all().order_by('created')[:6]
    return render(request, 'recipe_list.html', {'recipes': recipes})

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