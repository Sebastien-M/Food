from django.core.management.base import BaseCommand
from django.db import IntegrityError

from food_api.management.commands.web_scraper.scraper import MarmiScrap
from food_api.models import Recipe, Ingredient, IngredientRecipe


class Command(BaseCommand):
    help = 'Get recipes from marmiton website and fill local database with them'

    def add_arguments(self, parser):
        parser.add_argument('ingredients', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Take ingredient(s) as argument and find recipes associated
        """
        added_recipes = 0
        for ingredient in options['ingredients']:
            scraper = MarmiScrap(ingredient)
            recipe_data = scraper.extract_recipes_data()
            for recipe in recipe_data:
                recipe_name = recipe['recipe_name']
                ingredients = recipe['ingredients']
                steps = recipe['steps']
                added_recipes += self.save_data(recipe_name, ingredients, steps)
            print('{} recipes added'.format(added_recipes))

    def save_data(self, recipe_name, ingredients, steps):
        """
        Saves a recipe and its associated ingredient

        :param recipe_name: name of the recipe
        :param ingredients: list of ingredients
        :param steps: steps of the recipe
        :type ingredients:list[dict]
        """
        counter = 0
        recipe = self.add_recipe_to_db(recipe_name, steps)
        if recipe:
            self.add_ingredient_to_db(ingredients, recipe)
            counter += 1
            return counter
        return counter

    def add_recipe_to_db(self, recipe_name, steps):
        combined_steps = ''
        if Recipe.objects.filter(name=recipe_name).exists():
            return 0
        else:
            for step in steps:
                combined_steps += step + ';'
            try:
                recipe = Recipe(name=recipe_name, steps=combined_steps)
                recipe.save()
                return recipe
            except IntegrityError:
                pass

    def add_ingredient_to_db(self, ingredients, recipe_instance):
        for ingredient in ingredients:
            if Ingredient.objects.filter(name=ingredient['ingredient_name']).exists():
                pass
                # self.stdout.write(self.style.ERROR(
                #     'Ingredient \'{}\' is already existing'.format(ingredient['ingredient_name'])))
            else:
                ingredient_instance = Ingredient(name=ingredient['ingredient_name'])
                ingredient_instance.save()
                ingredient_recipe = IngredientRecipe(ingredient=ingredient_instance, recipe=recipe_instance,
                                                     quantity=ingredient['ingredient_quantity'])
                ingredient_recipe.save()

