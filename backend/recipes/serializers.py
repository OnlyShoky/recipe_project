from . import models
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField



  
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipe
        fields = '__all__'