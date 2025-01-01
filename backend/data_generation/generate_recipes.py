import factory
from faker import Faker
from datetime import timedelta
from recipes.models import Recipe, Tag, RecipeIngredient
from ingredients.models import Ingredient
from django.core.files import File
from PIL import Image
import io
import random

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
        
    for recipe_data in json_data["recipes"]:
        attributes = recipe_data["data"]["attributes"]

        # Create or retrieve the course (Tag of type 'Course')
        course, _ = Tag.objects.get_or_create(
            name=attributes["course"]["name"],
            type="Course"
        )

        # Create or retrieve the cuisine (Tag of type 'Cuisine')
        cuisine, _ = Tag.objects.get_or_create(
            name=attributes["cuisine"]["name"],
            type="Cuisine"
        )

        # Create the Recipe instance
        recipe = Recipe.objects.create(
            title=attributes["title"],
            instructions=attributes["instructions"],
            prep_time=timedelta(
                minutes=int(attributes["prep_time"].split(":")[1])
            ),
            cook_time=timedelta(
                minutes=int(attributes["cook_time"].split(":")[1])
            ),
            cool_time=timedelta(
                minutes=int(attributes["cool_time"].split(":")[1])
            ),
            total_time=timedelta(
                minutes=int(attributes["total_time"].split(":")[1])
            ),
            servings=attributes["servings"],
            difficulty=attributes["difficulty"],
            author=attributes["author"],
            source=attributes["source"],
            video_url=attributes["video_url"],
            image = attributes["image"],
            description = attributes["description"],
            course=course,
            cuisine=cuisine,
        )

        # # Attach the image to the Recipe
        # if attributes["image"]:
        #     image_content = ContentFile(
        #         b"", name=attributes["image"].split("/")[-1]
        #     )  # Placeholder for image data
        #     recipe.image.save(image_content.name, image_content, save=True)

        # Add ingredients to the Recipe
        for ingredient_data in attributes["ingredients"]:
            ingredient_name = ingredient_data["ingredient"]["name"]
            quantity = ingredient_data["quantity"]
            unit = ingredient_data["unit"]

            # Create or retrieve the Ingredient instance
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)

            # Create the RecipeIngredient instance
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity,
                unit=unit
            )

    print("Recipes generated successfully.")

# Example usage
if __name__ == "__main__":
    with open("recipes.json", "r") as file:
        recipe_json = json.load(file)
        generate_recipes_from_json(recipe_json)

