from django.contrib.auth.models import User
from django.db import models
import datetime


class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    steps = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
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


class DailyRecipe(models.Model):
    class Meta:
        unique_together = (('user', 'day'),)
    user = models.ForeignKey(User, related_name='daily_recipe', on_delete='cascade')
    day = models.DateField(default=datetime.datetime.now(), db_index=True)
    recipe = models.ForeignKey(Recipe, on_delete='cascade', related_name='daily_recipe', unique=False, blank=True, null=True)

    # def __str__(self):
    #     return self.day
