import requests
from bs4 import BeautifulSoup
from food_api.management.commands.web_scraper.Recipe import Recipe


class MarmiScrap:
    def __init__(self, recherche):
        """
        Class constructor

        :param recherche: Ingredient name
        """
        self.recherche = recherche
        self.root_url = 'http://www.marmiton.org'
        self.search_url = 'http://www.marmiton.org/recettes/recherche.aspx?aqt=' + recherche

    def get_root_html(self) -> list:
        """
        Returns all html recipes
        """
        html = requests.get(self.search_url)
        html_content = str(html.content)
        soup = BeautifulSoup(html_content, "html.parser")
        all_recipes = soup.find_all('a', 'recipe-card-link')
        return all_recipes

    def extract_recipes_data(self) -> list:
        """
        Returns a dict containing recipe informations
        """
        counter = 0
        recipes = self.get_root_html()
        recipe_data = []
        for recipe_html in recipes:
            recipe_link = self.root_url + recipe_html['href']
            recipe = Recipe(recipe_link)
            recipe.get_recipe_steps()

            recipe_name = recipe.get_recipe_name()
            nb_person = recipe.get_nb_person()
            ingredients = recipe.get_ingredients()
            steps = recipe.get_recipe_steps()
            recipe_data.append({'recipe_name': recipe_name,
                                'ingredients': ingredients,
                                'steps': steps})
            counter += 1
        return recipe_data
