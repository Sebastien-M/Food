import datetime
import calendar
import graphene
from django.utils.timezone import utc
from graphene_django import DjangoObjectType
from food_api.models import Recipe, DailyRecipe
from food_api.schemas.users.schema import UserType
from django.contrib.auth.models import User
from django.db.models import Q


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
        filter_fields = ['id']


class DailyRecipeType(DjangoObjectType):
    class Meta:
        model = DailyRecipe


class AddRecipe(graphene.Mutation):
    daily_recipe = graphene.Field(DailyRecipeType)

    class Arguments:
        recipe_id = graphene.String(required=True)
        user_email = graphene.String(required=True)

    def mutate(self, info, recipe_id, user_email):
        recipe = Recipe.objects.get(id=recipe_id)
        user = User.objects.get(email=user_email)

        existing = DailyRecipe.objects.filter(user=user, day=datetime.datetime.now().date()).exists()
        if existing:
            raise Exception('DailyRecipe already existing for this day')
        daily_recipe = DailyRecipe(
            recipe=recipe,
            user=user
        )
        daily_recipe.save()
        return AddRecipe(daily_recipe=daily_recipe)


class Query(graphene.ObjectType):
    recipe = graphene.Field(RecipeType, id=graphene.Int())
    week_menu = graphene.List(DailyRecipeType)
    todays_recipe = graphene.Field(RecipeType)

    def resolve_todays_recipe(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        todays_recipe = DailyRecipe.objects.get(user_id=user, day=datetime.datetime.now().date())
        return todays_recipe.recipe

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

    def resolve_recipe(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        return Recipe.objects.get(id=kwargs['id'])


class Mutation(graphene.ObjectType):
    add_recipe = AddRecipe.Field()
