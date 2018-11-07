from django.contrib import admin
from food_api.models import Recipe, Ingredient, IngredientRecipe, DailyRecipe

admin.site.site_header = 'Food Administration'
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientRecipe)
admin.site.register(DailyRecipe)
