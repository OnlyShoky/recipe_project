from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
    
)

from ingredients.models import Ingredient



class Recipe(TimeStampedModel, 
    ActivatorModel,
    TitleDescriptionModel,
    Model
    ):
    class Meta:
        verbose_name_plural = "Recipes"
    
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', related_name='recipes')
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes_images/', blank=True, null=True)  # Add ImageField
    
    ## V2
    course = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True, blank=True, related_name='course_recipes')
    cuisine = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True, blank=True, related_name='cuisine_recipes')
    
    prep_time = models.DurationField(null=True, blank=True)
    cook_time = models.DurationField(null=True, blank=True)
    cool_time = models.DurationField(null=True, blank=True)
    total_time = models.DurationField(null=True, blank=True)
    
    servings = models.IntegerField(blank=True, null=True)
    difficulty = models.CharField(max_length=50, blank=True, null=True)
    instructions = models.TextField()
    
    author = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='recipe_ingredients')
    quantity = models.FloatField()  # Quantity of the ingredient (e.g., 2, 1.5, etc.)
    unit = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'cup', 'tbsp', 'grams'

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name}"


