import os
from django.core.management.base import BaseCommand
from recipes.models import Recipe, Tag, RecipeIngredient
from ingredients.models import Ingredient, NutritionalTable

from django.conf import settings



class Command(BaseCommand):
    help = 'Delete all the recipes and tags'

    def handle(self, *args, **kwargs):
        # Delete all existing recipes before adding new ones
        RecipeIngredient.objects.all().delete()
        Tag.objects.all().delete()
        
        
        Ingredient.objects.all().delete()
        NutritionalTable.objects.all().delete()
        Recipe.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Successfully deleted all recipes, tags, and ingredients'))


    
        media_root = settings.MEDIA_ROOT

        # Make sure the media folder exists
        if not os.path.exists(media_root):
            self.stdout.write(self.style.ERROR(f"Media folder '{media_root}' does not exist."))
            return

        # Loop through all files in the media directory
        deleted_files = []
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):  # Add more image extensions if needed
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    deleted_files.append(file_path)

        if deleted_files:
            self.stdout.write(self.style.SUCCESS(f"Successfully deleted {len(deleted_files)} image(s)."))
        else:
            self.stdout.write(self.style.WARNING("No images found in the media folder."))
            

