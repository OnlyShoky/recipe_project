from . import models
from rest_framework import serializers
from ingredients.serializers import IngredientSerializer
from ingredients.models import Ingredient



  
# class RecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Recipe
#         fields = '__all__'
        
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'type']  # Adjust to your specific needs
        
class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()  # Use the IngredientSerializer to handle the 'ingredient' field
 
    class Meta:
        model = models.RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']  # Ensure the correct fields are used


        

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    course = TagSerializer(read_only=True)  # Using TagSerializer to represent the course tag
    cuisine = TagSerializer(read_only=True)  # Using TagSerializer to represent the cuisine tag
    prep_time = serializers.DurationField()  # Handling the DurationField as it is
    cook_time = serializers.DurationField()  # Handling the DurationField as it is
    cool_time = serializers.DurationField()  # Handling the DurationField as it is
    total_time = serializers.DurationField()  # Handling the DurationField as it is
    
    class Meta:
        model = models.Recipe
        fields = '__all__'
