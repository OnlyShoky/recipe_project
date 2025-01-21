from django.db import models
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
    
)

from utils.model_abstracts import Model

class NutritionalTable(models.Model):
    servings = models.FloatField(blank=True, null=True, help_text="Servings per container")
    
    # Basic fields
    calories = models.FloatField(blank=True, null=True, help_text="Calories per serving (kcal)")
    carbohydrates = models.FloatField(blank=True, null=True, help_text="Total carbohydrates (g)")
    protein = models.FloatField(blank=True, null=True, help_text="Protein content (g)")
    fat = models.FloatField(blank=True, null=True, help_text="Total fat (g)")
    saturated_fat = models.FloatField(blank=True, null=True, help_text="Saturated fat (g)")
    trans_fat = models.FloatField(blank=True, null=True, help_text="Trans fat (g)")
    fiber = models.FloatField(blank=True, null=True, help_text="Dietary fiber (g)")
    sugar = models.FloatField(blank=True, null=True, help_text="Total sugars (g)")
    
    # Minerals
    sodium = models.FloatField(blank=True, null=True, help_text="Sodium content (mg)")
    cholesterol = models.FloatField(blank=True, null=True, help_text="Cholesterol (mg)")
    potassium = models.FloatField(blank=True, null=True, help_text="Potassium (mg)")
    
    # Optional vitamins (comment these if not needed)
    vitamin_a = models.FloatField(blank=True, null=True, help_text="Vitamin A (IU)")
    vitamin_c = models.FloatField(blank=True, null=True, help_text="Vitamin C (mg)")
    calcium = models.FloatField(blank=True, null=True, help_text="Calcium (mg)")
    iron = models.FloatField(blank=True, null=True, help_text="Iron (mg)")

    def __str__(self):
        return f"{self.calories} kcal, {self.carbohydrates}g carbs, {self.protein}g protein"


# Create your models here.
class Ingredient(TimeStampedModel, 
    ActivatorModel,
    Model
    ):
    name = models.CharField(max_length=255, unique=True)  # Ingredient name
    nutrition = models.OneToOneField(
        NutritionalTable, on_delete=models.CASCADE, blank=True, null=True
    )  # Link to the nutritional table

    related_recipe = models.ForeignKey(
        'recipes.Recipe',  # Reference to the Recipe model
        on_delete=models.SET_NULL,  # Optional: Recipe can be deleted without deleting the ingredient
        blank=True,
        null=True,
        related_name="used_as_ingredient",  # Reverse relation from Recipe to Ingredient
        help_text="Optional: If this ingredient is a recipe, link the recipe here."
    )
    def __str__(self):
        return self.name
    
