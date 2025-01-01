from django.test import TestCase
from recipes.models import Recipe, Tag, RecipeIngredient
from ingredients.models import Ingredient
from datetime import timedelta

class RecipeTestCase(TestCase):
    def setUp(self):
        # Create some ingredients
        self.ingredient1 = Ingredient.objects.create(name="Flour")
        self.ingredient2 = Ingredient.objects.create(name="Sugar")

        # Create tags (course and cuisine)
        self.course_tag = Tag.objects.create(name="Main Course", type="Course")
        self.cuisine_tag = Tag.objects.create(name="Italian", type="Cuisine")

        # Create a Recipe
        self.recipe_data = {
            'title': 'Pizza',
            'course': self.course_tag,  # Use the actual Tag instance
            'cuisine': self.cuisine_tag,  # Use the actual Tag instance
            'instructions': "Mix and bake.",
            'prep_time': timedelta(minutes=10),  # Example: 10 minutes
            'cook_time': timedelta(minutes=30),  # Example: 30 minutes
            'cool_time': timedelta(minutes=5),   # Example: 5 minutes
            'total_time': timedelta(minutes=45), # Example: 45 minutes
            'servings': 4,
            'difficulty': 'Medium',
            'author': 'Chef A',
            'source': 'Italian Cookbook',
            'video_url': 'https://example.com/pizza-video'
        }

        # Create the Recipe instance
        self.recipe = Recipe.objects.create(**self.recipe_data)

        # Add ingredients via the through model (RecipeIngredient)
        self.recipe_ingredient1 = RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient1, quantity=2, unit='cups')
        self.recipe_ingredient2 = RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient2, quantity=1, unit='cup')

    def test_recipe_creation(self):
        # Check if the recipe was created correctly
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.title, "Pizza")
        self.assertEqual(recipe.course, self.course_tag)
        self.assertEqual(recipe.cuisine, self.cuisine_tag)
        self.assertEqual(recipe.ingredients.count(), 2)  # Check if the ingredients were correctly linked

    def test_recipe_creation(self):
        # Check if the recipe was created correctly
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.title, "Pizza")
        self.assertEqual(recipe.course, self.course_tag)
        self.assertEqual(recipe.cuisine, self.cuisine_tag)
        self.assertEqual(recipe.ingredients.count(), 2)  # Check if the ingredients were correctly linked
        self.assertEqual(recipe.prep_time, timedelta(minutes=10))
        self.assertEqual(recipe.cook_time, timedelta(minutes=30))
        self.assertEqual(recipe.cool_time, timedelta(minutes=5))
        self.assertEqual(recipe.total_time, timedelta(minutes=45))
        self.assertEqual(recipe.servings, 4)
        self.assertEqual(recipe.difficulty, "Medium")
        self.assertEqual(recipe.author, "Chef A")
        self.assertEqual(recipe.source, "Italian Cookbook")
        self.assertEqual(recipe.video_url, "https://example.com/pizza-video")

    def test_recipe_ingredients(self):
        # Test if ingredients are linked correctly to the recipe
        recipe = Recipe.objects.get(id=self.recipe.id)
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(self.recipe_ingredient1, ingredients)
        self.assertIn(self.recipe_ingredient2, ingredients)

        # Check the quantity and unit of ingredients
        recipe_ingredient_1 = RecipeIngredient.objects.get(recipe=recipe, ingredient=self.ingredient1)
        self.assertEqual(recipe_ingredient_1.ingredient, self.ingredient1)
        self.assertEqual(recipe_ingredient_1.quantity, 2)
        self.assertEqual(recipe_ingredient_1.unit, "cups")

        recipe_ingredient_2 = RecipeIngredient.objects.get(recipe=recipe, ingredient=self.ingredient2)
        self.assertEqual(recipe_ingredient_2.ingredient, self.ingredient2)
        self.assertEqual(recipe_ingredient_2.quantity, 1)
        self.assertEqual(recipe_ingredient_2.unit, "cup")

    def test_recipe_tags(self):
        # Test if the tags are linked correctly to the recipe
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.course, self.course_tag)
        self.assertEqual(recipe.cuisine, self.cuisine_tag)

    def test_recipe_update(self):
        # Test updating a recipe
        self.recipe.title = "New Pizza"
        self.recipe.instructions = "Mix, bake, and serve."
        self.recipe.save()

        updated_recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(updated_recipe.title, "New Pizza")
        self.assertEqual(updated_recipe.instructions, "Mix, bake, and serve.")

    def test_recipe_deletion(self):
        # Test deleting a recipe
        recipe_id = self.recipe.id
        self.recipe.delete()
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe_id)

    def test_recipe_time_fields(self):
        # Test time fields (prep_time, cook_time, etc.)
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.prep_time, timedelta(minutes=10))
        self.assertEqual(recipe.cook_time, timedelta(minutes=30))
        self.assertEqual(recipe.cool_time, timedelta(minutes=5))
        self.assertEqual(recipe.total_time, timedelta(minutes=45))

    def test_recipe_servings_and_difficulty(self):
        # Test servings and difficulty fields
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.servings, 4)
        self.assertEqual(recipe.difficulty, "Medium")

    def test_recipe_video_url(self):
        # Test video URL field
        recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(recipe.video_url, "https://example.com/pizza-video")