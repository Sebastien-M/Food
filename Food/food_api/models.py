from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    steps = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    notes = models.TextField(null=True, blank=True)
    recipe = models.ManyToManyField(Recipe, related_name='ingredients', through='IngredientRecipe')

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    class Meta:
        db_table = 'food_api_ingredient_recipe'

    def __str__(self):
        return '{} - {}'.format(self.recipe.name, self.ingredient.name)

    ingredient = models.ForeignKey(Ingredient, on_delete='cascade')
    recipe = models.ForeignKey(Recipe, on_delete='cascade', related_name='ingredient_quantity')
    quantity = models.FloatField(blank=True, null=True)


class WeekMenu(models.Model):
    user_id = models.ForeignKey(User, related_name='week_menu', on_delete='cascade')
    mon = models.ForeignKey(Recipe, on_delete='cascade', related_name='mon', unique=False, blank=True, null=True)
    tue = models.ForeignKey(Recipe, on_delete='cascade', related_name='tue', unique=False, blank=True, null=True)
    wed = models.ForeignKey(Recipe, on_delete='cascade', related_name='wed', unique=False, blank=True, null=True)
    thu = models.ForeignKey(Recipe, on_delete='cascade', related_name='thu', unique=False, blank=True, null=True)
    fri = models.ForeignKey(Recipe, on_delete='cascade', related_name='fri', unique=False, blank=True, null=True)
    sat = models.ForeignKey(Recipe, on_delete='cascade', related_name='sat', unique=False, blank=True, null=True)
    sun = models.ForeignKey(Recipe, on_delete='cascade', related_name='sun', unique=False, blank=True, null=True)
