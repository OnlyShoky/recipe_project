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
        fields = ['name', 'nutrition']

    # You can override the create and update methods if necessary.
    def create(self, validated_data):
        nutrition_data = validated_data.pop('nutrition')
        nutritional_table = NutritionalTable.objects.create(**nutrition_data)
        ingredient = Ingredient.objects.create(nutrition=nutritional_table, **validated_data)
        return ingredient

    def update(self, instance, validated_data):
        nutrition_data = validated_data.pop('nutrition')
        instance.name = validated_data.get('name', instance.name)
        # Update nutritional table data
        for attr, value in nutrition_data.items():
            setattr(instance.nutrition, attr, value)
        instance.nutrition.save()
        instance.save()
        return instance
