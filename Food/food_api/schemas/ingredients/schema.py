import graphene
from graphene_django import DjangoObjectType

from food_api.models import Ingredient


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        # filter_fields = ['id']


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('ingredients').all()
