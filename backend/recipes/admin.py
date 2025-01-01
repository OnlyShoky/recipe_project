from django.contrib import admin
from .models import Recipe,Tag, RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'description', 'instructions','id',)
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'type', 'description')
    
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ( 'recipe', 'ingredient', 'quantity')