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
        fields = ['name']  # Adjust to your specific needs

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['name']  # Adjust to your specific needs

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cuisine
        fields = ['name']  # Adjust to your specific needs
               
class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()  # Use the IngredientSerializer to handle the 'ingredient' field
 
    class Meta:
        model = models.RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit', 'notes', 'groupName']  # Ensure the correct fields are used


        

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    courses = CourseSerializer(many=True,read_only=True)  # Using TagSerializer to represent the course tag
    cuisines = CuisineSerializer(many=True,read_only=True)  # Using TagSerializer to represent the cuisine tag
    tags = TagSerializer(many=True, read_only=True)
    prep_time = serializers.DurationField()  # Handling the DurationField as it is
    cook_time = serializers.DurationField()  # Handling the DurationField as it is
    cool_time = serializers.DurationField()  # Handling the DurationField as it is
    total_time = serializers.DurationField()  # Handling the DurationField as it is
    
    class Meta:
        model = models.Recipe
        fields = [
            'title', 
            'description', 
            'courses', 
            'cuisines', 
            'tags',
            'prep_time', 
            'cook_time', 
            'cool_time', 
            'total_time', 
            'servings', 
            'ingredients', 
            'difficulty', 
            'instructions', 
            'author', 
            'source', 
            'video_url', 
            'image'
        ]
