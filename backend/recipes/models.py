from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
    
)

from ingredients.models import Ingredient

class Tag(TimeStampedModel, ActivatorModel):
    """
    Model for tags with a type (e.g., Cuisine, Course, Other) to categorize them.
    """
    class Meta:
        verbose_name_plural = "Tags"
    
    TAG_TYPES = [
        ('Cuisine', 'Cuisine'),  # E.g., Italian, Mexican
        ('Course', 'Course'),    # E.g., Main Course, Dessert
        ('Other', 'Other'),      # E.g., Vegan, Gluten-Free, Pasta
    ]
    
    name = models.CharField(max_length=255, unique=True)  # Tag name (e.g., 'Italian', 'Main Course')
    type = models.CharField(
        max_length=50,
        choices=TAG_TYPES,
        default='Other',
    )  # The type of tag (e.g., Cuisine, Course, Other)

    def __str__(self):
        return self.name


    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')
    quantity = models.FloatField()  # Quantity of the ingredient (e.g., 2, 1.5, etc.)
    unit = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'cup', 'tbsp', 'grams'

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name}"

    class Meta:
        verbose_name_plural = "RecipeIngredients"

class Recipe(TimeStampedModel, 
    ActivatorModel,
    TitleDescriptionModel,
    Model
    ):
    class Meta:
        verbose_name_plural = "Recipes"
        
    # ingredients = models.ManyToManyField(Ingredient, related_name='recipes')  # Now we link to RecipeIngredient
    # ingredients = models.ManyToManyField(RecipeIngredient, related_name='recipes')  # Now we link to RecipeIngredient
    # ingredients = models.ForeignKey(RecipeIngredient, on_delete=models.DO_NOTHING, null=True, blank=True)  # This is the foreign key

    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes_images/', blank=True, null=True)  # Add ImageField
    
    ## V2
    course = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)  # This is the foreign key
    cuisine = models.ForeignKey(Tag, on_delete=models.CASCADE,null=True, blank=True, related_name='cuisine_recipes')
    
    prep_time = models.DurationField(null=True, blank=True)
    cook_time = models.DurationField(null=True, blank=True)
    cool_time = models.DurationField(null=True, blank=True)
    total_time = models.DurationField(null=True, blank=True)
    

    
    servings = models.IntegerField(blank=True, null=True)
    difficulty = models.CharField(max_length=50, blank=True, null=True)
    instructions = models.TextField()
    
    equipment = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    
    author = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def ingredients(self):
        """
        Property to get all RecipeIngredient instances related to this Recipe.
        """
        return self.recipe_ingredients.all()

