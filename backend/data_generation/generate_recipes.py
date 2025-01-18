import factory
from faker import Faker
from datetime import timedelta
from recipes.models import *
from ingredients.models import Ingredient,NutritionalTable
from django.core.files import File
from PIL import Image
import io
import random
from tqdm import tqdm  # Import tqdm for the progress bar


fake = Faker()

# TagFactory to generate Tag instances
class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.LazyAttribute(lambda _: fake.word())  # Random tag name
    type = factory.LazyAttribute(lambda _: random.choice(['Course', 'Cuisine']))  # Random tag type

# IngredientFactory to generate Ingredient instances
class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = factory.LazyAttribute(lambda _: fake.word())  # Random ingredient name

# RecipeFactory to generate Recipe instances
class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    # Recipe fields
    title = factory.LazyAttribute(lambda _: fake.word())  # Random word as title
    instructions = factory.LazyAttribute(lambda _: fake.sentence())  # Random sentence for instructions
    prep_time = factory.LazyAttribute(lambda _: timedelta(minutes=random.randint(5, 15)))  # Random prep time
    cook_time = factory.LazyAttribute(lambda _: timedelta(minutes=random.randint(10, 60)))  # Random cook time
    cool_time = factory.LazyAttribute(lambda _: timedelta(minutes=random.randint(5, 15)))  # Random cool time
    total_time = factory.LazyAttribute(lambda o: o.prep_time + o.cook_time + o.cool_time)  # Total time = prep + cook + cool time
    servings = factory.LazyAttribute(lambda _: random.randint(2, 6))  # Random number of servings
    difficulty = factory.LazyAttribute(lambda _: random.choice(['Easy', 'Medium', 'Hard']))  # Random difficulty
    author = factory.LazyAttribute(lambda _: fake.name())  # Random author name
    source = factory.LazyAttribute(lambda _: fake.company())  # Random source company
    video_url = factory.LazyAttribute(lambda _: fake.url())  # Random video URL

    # Use TagFactory to generate tags
    course = factory.SubFactory(TagFactory, type='Course')
    cuisine = factory.SubFactory(TagFactory, type='Cuisine')

    # Generate a random image for the Recipe model
    @factory.lazy_attribute
    def image(self):
        # Create a random image using Pillow
        img = Image.new('RGB', (100, 100), color=(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ))

        # Save the image to a BytesIO object to simulate a file
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)

        # Return the image as a Django File
        return File(img_io, name=f'{self.title}_image.jpg')

    # Add ingredients via the through model (RecipeIngredient)
    @factory.post_generation
    def ingredients(self, create, extracted, **kwargs):
        # Create 20 random ingredients
        ingredients = [IngredientFactory.create(name=fake.word() + str(random.randint(1,999))) for _ in range(5)]

        # Randomly select 5 ingredients to add to this recipe
        selected_ingredients = random.sample(ingredients, 5)

        for ingredient in selected_ingredients:
            # Create RecipeIngredient objects for the selected ingredients
            quantity = random.randint(1, 5)
            unit = random.choice(['g', 'ml', 'cup', 'tbsp', 'oz'])
            RecipeIngredient.objects.create(
                recipe=self,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )
            
            
import json
from django.core.files.base import ContentFile


def generate_recipes_from_json(json_data):
    """
    Generate Recipe, Tag, and RecipeIngredient instances from JSON data.
    """
    # Ensure we are working with a parsed dictionary (or list of dictionaries)
    if isinstance(json_data, str):
        json_data = json.loads(json_data)  # Parse the JSON string if it's not already a dictionary
        
    print("Starting import")
        
    for recipe_data in tqdm(json_data["recipes"]):
        attributes = recipe_data["data"]["attributes"]

        
        
        prep_time = timedelta(minutes=int(attributes["prep_time"].split(":")[1])) if attributes["prep_time"] else None
        cook_time = timedelta(minutes=int(attributes["cook_time"].split(":")[1])) if attributes["cook_time"] else None
        cool_time = timedelta(minutes=int(attributes["cool_time"].split(":")[1])) if attributes["cool_time"] else None
        total_time = timedelta(minutes=int(attributes["total_time"].split(":")[1])) if attributes["total_time"] else None

        # Create the Recipe instance
        recipe = Recipe.objects.create(
            title=attributes["title"],
            instructions=attributes["instructions"],
            prep_time=prep_time,
            cook_time=cook_time,
            cool_time=cool_time,
            total_time=total_time,
            servings=attributes["servings"],
            difficulty=attributes["difficulty"],
            author=attributes["author"],
            source=attributes["source"],
            video_url=attributes["video_url"],
            image = attributes["image"],
            image_card = attributes["image_card"],
            description = attributes["description"],
            rating = attributes["rating"]["average"],
            number_of_ratings = attributes["rating"]["count"],
        )
        
        # Create or retrieve tags and addthem 
        for cuisine in attributes["cuisines"]:
            cuisine, _ = Cuisine.objects.get_or_create(name=cuisine)
            recipe.cuisines.add(cuisine)
            
        for course in attributes["courses"]:
            course, _ = Course.objects.get_or_create(name=course)
            recipe.courses.add(course)
            
        for tag in attributes["tags"]:
            tag, _ = Tag.objects.get_or_create(name=tag)
            recipe.tags.add(tag)
            
        # Add ingredients to the Recipe
        for ingredient_data in attributes["ingredients"]:
            ingredient_name = ingredient_data["ingredient"]["name"]
            quantity = ingredient_data["quantity"]
            unit = ingredient_data["unit"]
            notes = ingredient_data["notes"]
            groupName = ingredient_data["groupName"]

            # Create or retrieve the Ingredient instance
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)

            # Create the RecipeIngredient instance
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit,
                notes=notes,
                groupName=groupName
            )

    print("Recipes generated successfully.")

import random
from ingredients.models import Ingredient, NutritionalTable

def create_and_assign_nutrition_tables():
    """
    Create a random NutritionalTable for each Ingredient that doesn't have one,
    and assign it to the ingredient.
    """
    for ingredient in Ingredient.objects.all():
        # Check if the ingredient already has a NutritionalTable
        if not hasattr(ingredient, 'nutrition') or ingredient.nutrition is None:
            # Create a new NutritionalTable with random values
            nutritional_table = NutritionalTable.objects.create(
                calories=random.uniform(50, 500),
                carbohydrates=random.uniform(0, 100),
                protein=random.uniform(0, 50),
                fat=random.uniform(0, 50),
                saturated_fat=random.uniform(0, 20),
                trans_fat=random.uniform(0, 5),
                fiber=random.uniform(0, 30),
                sugar=random.uniform(0, 50),
                sodium=random.uniform(0, 5000),
                cholesterol=random.uniform(0, 300),
                potassium=random.uniform(0, 3500),
                vitamin_a=random.uniform(0, 10000),
                vitamin_c=random.uniform(0, 100),
                calcium=random.uniform(0, 1300),
                iron=random.uniform(0, 18),
            )

            # Assign the new nutritional table to the ingredient
            ingredient.nutrition = nutritional_table
            ingredient.save()

            print(f"Created and assigned nutrition table to ingredient '{ingredient.name}'")
        else:
            print(f"Ingredient '{ingredient.name}' already has a nutrition table")

    print("Completed assigning nutritional tables to all ingredients.")

# Example usage
if __name__ == "__main__":
    create_and_assign_nutrition_tables()


# Example usage
if __name__ == "__main__":
    with open("recipes.json", "r") as file:
        recipe_json = json.load(file)
        generate_recipes_from_json(recipe_json)

