from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Ingredient
from .serializers import IngredientSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class IngredientAPIView(views.APIView):
    """
    APIView to retrieve a list of all ingredients.
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        ingredients = Ingredient.objects.all()  # Fetch all ingredients
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientDetailAPIView(views.APIView):
    """
    APIView to retrieve a single ingredient by ID.
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, id, *args, **kwargs):
        try:
            ingredient = Ingredient.objects.get(id=id)  # Fetch ingredient by ID
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ingredient.DoesNotExist:
            raise NotFound("Ingredient not found")
