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
    ingredient = IngredientSerializer()  # Use the Ingredient serializer for nested ingredient data
    
    class Meta:
        model = models.RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']
        
    def to_representation(self, instance):
        # Flattening the nested representation of ingredient for easier access
        data = super().to_representation(instance)
        return {
            'name': data['ingredient']['name'],
            'quantity': data['quantity'],
            'unit': data['unit'],
        }


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)  # Nested serializer for ingredients
    course = TagSerializer(read_only=True)  # Using TagSerializer to represent the course tag
    cuisine = TagSerializer(read_only=True)  # Using TagSerializer to represent the cuisine tag
    prep_time = serializers.DurationField()  # Handling the DurationField as it is
    cook_time = serializers.DurationField()  # Handling the DurationField as it is
    cool_time = serializers.DurationField()  # Handling the DurationField as it is
    total_time = serializers.DurationField()  # Handling the DurationField as it is
    
    class Meta:
        model = models.Recipe
        fields = '__all__'

    def create(self, validated_data):
        """
        Override the create method to handle the ManyToMany and ForeignKey relationships.
        """
        ingredients_data = validated_data.pop('ingredients')
        course_data = validated_data.pop('course', None)
        cuisine_data = validated_data.pop('cuisine', None)
        
        # Create the Recipe instance
        recipe = models.Recipe.objects.create(**validated_data)
        
        # Create and add ingredients
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.create(**ingredient_data)  # Create each ingredient
            recipe.ingredients.add(ingredient)  # Add ingredient to the recipe
            
        # Handle course and cuisine if provided
        if course_data:
            recipe.course = models.Tag.objects.get(id=course_data['id'])
        if cuisine_data:
            recipe.cuisine = models.Tag.objects.get(id=cuisine_data['id'])
        
        recipe.save()
        
        return recipe

    def update(self, instance, validated_data):
        """
        Override the update method to handle the update of related fields.
        """
        ingredients_data = validated_data.pop('ingredients', None)
        course_data = validated_data.pop('course', None)
        cuisine_data = validated_data.pop('cuisine', None)

        # Update recipe instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if ingredients_data:
            # Handle the update of ingredients (this may depend on your use case)
            instance.ingredients.clear()  # Clear existing ingredients
            for ingredient_data in ingredients_data:
                ingredient = Ingredient.objects.create(**ingredient_data)
                instance.ingredients.add(ingredient)

        if course_data:
            instance.course = models.Tag.objects.get(id=course_data['id'])
        if cuisine_data:
            instance.cuisine = models.Tag.objects.get(id=cuisine_data['id'])

        instance.save()
        return instance