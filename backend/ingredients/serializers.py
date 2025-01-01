from rest_framework import serializers
from .models import Ingredient, NutritionalTable

class NutritionalTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionalTable
        fields = [
            'calories', 'carbohydrates', 'protein', 'fat', 'saturated_fat', 
            'trans_fat', 'fiber', 'sugar', 'sodium', 'cholesterol', 'potassium',
            'vitamin_a', 'vitamin_c', 'calcium', 'iron'
        ]

class IngredientSerializer(serializers.ModelSerializer):
    nutrition = NutritionalTableSerializer()

    class Meta:
        model = Ingredient
        fields = ['name', 'nutrition']  # Include other fields like quantity, unit, etc., if necessary

