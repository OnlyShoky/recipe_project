from django.core.management.base import BaseCommand

from data_generation.generate_recipes import create_and_assign_nutrition_tables

class Command(BaseCommand):
    help = 'Generate random nuitritional tables and populate the ingredients'

    def handle(self, *args, **kwargs):

        # Populate the ingredients with random Nutritional Tables
        create_and_assign_nutrition_tables()

        self.stdout.write(self.style.SUCCESS('Successfully populated the ingredients with random Nutritional Tables'))
