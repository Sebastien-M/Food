import graphene
from graphene_django import DjangoObjectType

from food_api.models import Ingredient


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_ingredients(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged!')
        return Ingredient.objects.all()
