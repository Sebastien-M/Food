import datetime
import calendar
import graphene
from graphene_django import DjangoObjectType
from food_api.models import Recipe, WeekMenu


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
        filter_fields = ['id']


class WeekMenuType(DjangoObjectType):
    class Meta:
        model = WeekMenu


class TodaysRecipeType(DjangoObjectType):
    class Meta:
        model = Recipe


class Query(graphene.ObjectType):
    recipe = graphene.Field(RecipeType, id=graphene.Int())
    week_menu = graphene.Field(WeekMenuType)
    todays_recipe = graphene.Field(TodaysRecipeType)

    def resolve_todays_recipe(self, info):
        user = info.context.user
        today = datetime.datetime.today().weekday()
        today_name = calendar.day_name[today][:3].lower()
        if user.is_anonymous:
            raise Exception('Not logged!')
        recipe = WeekMenu.objects.get(user_id=user)
        return getattr(recipe, today_name)

    def resolve_week_menu(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        return WeekMenu.objects.get(user_id=user.id)

    def resolve_recipe(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        return Recipe.objects.get(id=kwargs['id'])
