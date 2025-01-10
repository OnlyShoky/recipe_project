from django.contrib import admin
from .models import *

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0  # Number of empty forms to display for adding new ingredients
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'description', 'created','id',)
    inlines = [RecipeIngredientInline]  # Add the inline admin
    
@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ( 'name','id')
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ( 'name','id')
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ( 'name','id')
    
    
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ( 'recipe', 'ingredient', 'quantity', 'groupName')