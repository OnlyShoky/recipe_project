from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel,
    
)



class Recipe(TimeStampedModel, 
    ActivatorModel,
    TitleDescriptionModel,
    Model
    ):
    class Meta:
        verbose_name_plural = "Recipes"
    
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes_images/', blank=True, null=True)  # Add ImageField
    # servings = models.IntegerField(blank=True, null=True)
    # prep_time = models.DurationField(blank=True, null=True)
    # cook_time = models.DurationField(blank=True, null=True)
    # difficulty = models.CharField(max_length=50, blank=True, null=True)
    # cuisine_type = models.CharField(max_length=100, blank=True, null=True)
    # author = models.CharField(max_length=100, blank=True, null=True)
    # is_vegetarian = models.BooleanField(default=False)
    # is_gluten_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title
