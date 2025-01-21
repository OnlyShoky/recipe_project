from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
    
)

from fractions import Fraction
from ingredients.models import Ingredient, NutritionalTable

class Tag(TimeStampedModel, ActivatorModel):
    """
    Model for tags with 
    """
    class Meta:
        verbose_name_plural = "Tags" 
    name = models.CharField(max_length=255, unique=True)  # Tag name (e.g., 'Dessert', 'Halloween', etc.)

    def __str__(self):
        return self.name
    
class Cuisine(TimeStampedModel, ActivatorModel):
    """
    Model for Cuisines with 
    """
    class Meta:
        verbose_name_plural = "Cuisines" 
    name = models.CharField(max_length=255, unique=True)  # Tag name (e.g., 'Morrocan', 'Japanese', etc.)

    def __str__(self):
        
        """
        Returns a string representation of the object, which is the tag name.
        """
        return self.name
    
class Course(TimeStampedModel, ActivatorModel):
    """
    Model for Courses with 
    """
    class Meta:
        verbose_name_plural = "Courses" 
    name = models.CharField(max_length=255, unique=True)  # Tag name (e.g., 'Dessert', 'Main-dish', etc.)

    def __str__(self):
        return self.name


    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')
    quantity = models.FloatField(blank=True, null=True)  # Quantity of the ingredient (e.g., 2, 1.5, etc.)
    unit = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'cup', 'tbsp', 'grams'
    notes = models.CharField(max_length=100, blank=True, null=True)
    groupName = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        try:
            return f"{str(Fraction(self.quantity).limit_denominator(10))} {self.unit} of {self.ingredient.name}"
        except TypeError:
            return f"{self.unit} of {self.ingredient.name}"

    class Meta:
        verbose_name_plural = "RecipeIngredients"

class Recipe(TimeStampedModel, 
    ActivatorModel,
    TitleDescriptionModel,
    Model
    ):
    class Meta:
        verbose_name_plural = "Recipes"
        

    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes_images/feature/', blank=True, null=True)  # Add ImageField
    image_card = models.ImageField(upload_to='recipes_images/card/', blank=True, null=True)  # Add ImageField

    
    ## V2
    # course = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)  # This is the foreign key
    # cuisine = models.ForeignKey(Tag, on_delete=models.CASCADE,null=True, blank=True, related_name='cuisine_recipes')
    # Many-to-Many Relationships
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)
    cuisines = models.ManyToManyField(Cuisine, related_name='recipes', blank=True)
    courses = models.ManyToManyField(Course, related_name='recipes', blank=True)
    
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
    
    nutrition = models.OneToOneField(
        NutritionalTable, on_delete=models.CASCADE, blank=True, null=True
    )  # Link to the nutritional table

    
    # fields for ratings
    rating = models.DecimalField(
        max_digits=4,  # Allows values like 9.99
        decimal_places=2,  # Two decimal places for average rating
        null=True,
        blank=True,
        default=None,
    )
    number_of_ratings = models.IntegerField(
        blank=True,
        null=True,
        default=None,
        help_text="The number of user ratings for this recipe.",
    )

    @property
    def ingredients(self):
        """
        Property to get all RecipeIngredient instances related to this Recipe.
        """
        return self.recipe_ingredients.all()
    
    # @property
    # def tags(self):
    #     """
    #     Property to get all tags instances related to this Recipe.
    #     """
    #     return self.tags.all()
    
    # @property
    # def courses(self):
    #     """
    #     Property to get all courses instances related to this Recipe.
    #     """
    #     return self.courses.all()
    
    # @property
    # def cuisines(self):
    #     """
    #     Property to get all cuisines instances related to this Recipe.
    #     """
    #     return self.cuisines.all()

    def __str__(self):
        return self.title