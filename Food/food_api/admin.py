from django.contrib import admin

# Register your models here.
from food_api.models import Recipe, Ingredient, IngredientRecipe

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientRecipe)
