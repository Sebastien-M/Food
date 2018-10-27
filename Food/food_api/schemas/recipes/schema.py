import graphene
from graphene_django import DjangoObjectType

from food_api.models import Recipe


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
        # filter_fields = ['id']


class Query(graphene.ObjectType):
    all_recipes = graphene.List(RecipeType)

    def resolve_all_recipes(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        return Recipe.objects.all()
