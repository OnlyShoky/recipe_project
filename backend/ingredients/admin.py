from django.contrib import admin
from .models import Ingredient, NutritionalTable

class NutritionalTableAdmin(admin.ModelAdmin):
    list_display = ('calories', 'carbohydrates', 'protein', 'fat', 'fiber', 'sugar', 'sodium', 'cholesterol', 'potassium', 'vitamin_a', 'vitamin_c', 'calcium', 'iron')
    search_fields = ('calories', 'carbohydrates', 'protein', 'fat', 'fiber', 'sugar', 'sodium', 'cholesterol', 'potassium', 'vitamin_a', 'vitamin_c', 'calcium', 'iron')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'nutrition')
    search_fields = ('name',)
    list_filter = ('nutrition',)
    raw_id_fields = ('nutrition',)  # Use a raw ID input for selecting related NutritionalTable
    autocomplete_fields = ('nutrition',)  # Use autocomplete for related model

admin.site.register(NutritionalTable, NutritionalTableAdmin)
admin.site.register(Ingredient, IngredientAdmin)
