from django.core.management.base import BaseCommand
from recipes.models import Recipe, Tag, RecipeIngredient
from ingredients.models import Ingredient

from data_generation.generate_recipes import generate_recipes_from_json
import json

class Command(BaseCommand):
    help = 'Generate random recipes and populate the database'

    def handle(self, *args, **kwargs):
        # Delete all existing recipes before adding new ones
        # Recipe.objects.all().delete()
        # Tag.objects.all().delete()
        # Ingredient.objects.all().delete()

        # Load the JSON data from the file
        with open('data_generation/recipe.json', 'r', encoding='utf-8') as file:
            recipe_data = json.load(file)
            
        generate_recipes_from_json(recipe_data)

        self.stdout.write(self.style.SUCCESS('Successfully imported recipes'))
