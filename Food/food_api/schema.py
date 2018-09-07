import graphene

from graphene_django.types import DjangoObjectType

from .models import Recipe, Ingredient, IngredientRecipe


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class IngredientRecipeType(DjangoObjectType):
    class Meta:
        model = IngredientRecipe


class QueryMixin(object):
    all_recipes = graphene.List(RecipeType)
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_recipes(self, info, **kwargs):
        return Recipe.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('ingredients').all()


class Query(QueryMixin, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
