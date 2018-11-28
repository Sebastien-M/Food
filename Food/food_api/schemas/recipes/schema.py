import datetime
import calendar
import graphene
from django.utils.timezone import utc
from graphene_django import DjangoObjectType

import food_api
from food_api.models import Recipe, DailyRecipe, ShoppingListItem, IngredientRecipe
from food_api.schemas.users.schema import UserType
from django.contrib.auth.models import User
from django.db.models import Q
import random


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
        filter_fields = ['id']


class IngredientRecipeType(DjangoObjectType):
    class Meta:
        model = IngredientRecipe
        filter_fields = ['recipe', 'id']


class DailyRecipeType(DjangoObjectType):
    class Meta:
        model = DailyRecipe


class ShoppingListItemType(DjangoObjectType):
    class Meta:
        model = ShoppingListItem


class AddRecipe(graphene.Mutation):
    daily_recipe = graphene.Field(DailyRecipeType)

    class Arguments:
        recipe_id = graphene.String(required=True)
        user_email = graphene.String(required=True)
        date = graphene.Date()

    def mutate(self, info, recipe_id, user_email, date):
        recipe = Recipe.objects.get(id=recipe_id)
        user = User.objects.get(email=user_email)

        existing = DailyRecipe.objects.filter(user=user, day=date).exists()
        if existing:
            daily_recipe = DailyRecipe.objects.filter(user=user, day=date).get()
            daily_recipe.recipe = recipe
        else:
            daily_recipe = DailyRecipe(
                recipe=recipe,
                user=user,
                day=date
            )
        daily_recipe.save()
        # shopping_list_item = ShoppingListItem(user=user, ingredients=)
        return AddRecipe(daily_recipe=daily_recipe)


class DeleteShoppingListItem(graphene.Mutation):
    result = graphene.String()

    class Arguments:
        item_id = graphene.Int(required=True)

    def mutate(self, info, item_id):
        item = ShoppingListItem.objects.get(id=item_id)
        item.delete()
        return DeleteShoppingListItem(result='done')


class Query(graphene.ObjectType):
    recipe = graphene.Field(RecipeType, id=graphene.Int())
    week_menu = graphene.List(DailyRecipeType)
    todays_recipe = graphene.List(IngredientRecipeType)
    random_recipe = graphene.Field(RecipeType)
    set_initial_shoppingList = graphene.String()
    shopping_list = graphene.List(ShoppingListItemType)

    def resolve_todays_recipe(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        todays_recipe = DailyRecipe.objects.get(user_id=user, day=datetime.datetime.now().date()).recipe
        ingredient_recipe = IngredientRecipe.objects.filter(recipe=todays_recipe)
        return ingredient_recipe

    def resolve_week_menu(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        first_day_of_week = datetime.datetime.today() - datetime.timedelta(
            days=datetime.datetime.today().isoweekday() - 1 % 7)
        menu = DailyRecipe.objects.filter(Q(day__gte=first_day_of_week), Q(user=user))[:7]
        if len(menu) < 7:
            raise Exception("Menu not defined for this week")
        return menu

    def resolve_random_recipe(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        number_of_recipes = Recipe.objects.all().count()
        random_id = random.randint(1, number_of_recipes)
        tries = 0
        while tries <= 20:
            try:
                recipe = Recipe.objects.get(id=random_id)
                break
            except food_api.models.Recipe.DoesNotExist:
                tries += 1
                if tries == 20:
                    return Exception('An error occurred while trying to find a recipe')
        return recipe

    def resolve_recipe(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        return Recipe.objects.get(id=kwargs['id'])

    def resolve_set_initial_shoppingList(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        ShoppingListItem.objects.filter(user=user).delete()
        first_day_of_week = datetime.datetime.today() - datetime.timedelta(
            days=datetime.datetime.today().isoweekday() - 1 % 7)
        menu = DailyRecipe.objects.filter(Q(day__gte=first_day_of_week), Q(user=user))[:7]
        ingredient_dict = {}
        for daily_recipe in menu:
            todays_recipe = daily_recipe.recipe
            ingredient_recipe = IngredientRecipe.objects.filter(recipe=todays_recipe)

            for ingredient_recipe_item in ingredient_recipe:
                if ingredient_recipe_item.ingredient.name in ingredient_dict:
                    if ingredient_recipe_item.quantity is not None:
                        ingredient_dict[ingredient_recipe_item.ingredient.name] += ingredient_recipe_item.quantity
                else:
                    ingredient_dict[ingredient_recipe_item.ingredient.name] = ingredient_recipe_item.quantity
        for ingredient, quantity in ingredient_dict.items():
            if 'sel' not in ingredient.lower() and 'poivre' not in ingredient.lower():
                shopping_list_item = ShoppingListItem(user=user)
                shopping_list_item.ingredient = ingredient
                if quantity is not None:
                    shopping_list_item.quantity = round(quantity, 3)
                shopping_list_item.save()
        return 'Done'

    def resolve_shopping_list(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        return ShoppingListItem.objects.filter(user=user)


class Mutation(graphene.ObjectType):
    add_recipe = AddRecipe.Field()
    remove_shopping_list_item = DeleteShoppingListItem.Field()
