import requests
from bs4 import BeautifulSoup
from fractions import Fraction


class Recipe:
    def __init__(self, recipe_link):
        self.recipe_link = recipe_link
        self.recipe_html_content = requests.get(recipe_link).content
        self.recipe_object = BeautifulSoup(self.recipe_html_content, 'html.parser')

    def get_recipe_name(self):
        """
        Returns the name of the recipe

        :return: str
        """
        return self.recipe_object.title.text.rsplit(':')[0][:-1]

    def get_nb_person(self):
        """
        Returns the number of people the recipe is made for

        :return: list
        """
        return self.recipe_object.find('div', {'class': 'recipe-ingredients__qt-counter'}).input['value']

    def get_ingredients(self):
        """
        Returns a list of all the ingredients

        :return: list
        """
        ingredients = self.recipe_object.find_all('li', 'recipe-ingredients__list__item')
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_quantity = ingredient.find('span').text
            if ingredient_quantity:
                # ingredient_quantity = Fraction(round(int(ingredient_quantity) / int(self.get_nb_person()), 3))
                try:
                    ingredient_quantity = round(float(ingredient_quantity) / int(self.get_nb_person()), 3)
                except ValueError:
                    ingredient_quantity = ingredient_quantity.replace('/', '.')
                    ingredient_quantity = round(float(ingredient_quantity) / int(self.get_nb_person()), 3)
            else:
                ingredient_quantity = None
            ingredient_name = ingredient.find('span', 'ingredient').text
            ingredients_list.append({'ingredient_name': ingredient_name,
                                     'ingredient_quantity': ingredient_quantity})
        return ingredients_list

    def get_recipe_steps(self):
        """
        Returns all the steps of the recipe

        :return: str
        """
        recipe_steps = []
        steps = self.recipe_object.find_all('li', 'recipe-preparation__list__item')
        for step in steps:
            recipe_steps.append(step.text.split('\t\t\t')[1].split('\t\t')[0])
        return recipe_steps
