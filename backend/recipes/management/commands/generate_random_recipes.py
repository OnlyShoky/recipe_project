from django.core.management.base import BaseCommand
from recipes.models import Recipe, Tag, RecipeIngredient

from data_generation.generate_recipes import RecipeFactory

class Command(BaseCommand):
    help = 'Generate random recipes and populate the database'

    def handle(self, *args, **kwargs):
        # Delete all existing recipes before adding new ones
        Recipe.objects.all().delete()
        Tag.objects.all().delete()

        # Create 10 random recipes
        for _ in range(10):
            RecipeFactory.create()

        self.stdout.write(self.style.SUCCESS('Successfully created 10 random recipes'))
