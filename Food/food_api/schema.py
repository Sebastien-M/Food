import graphene
from food_api.schemas.users import schema as user_schema
from food_api.schemas.ingredients import schema as ingredient_schema
from food_api.schemas.recipes import schema as recipe_schema


# class IngredientRecipeType(DjangoObjectType):
#     class Meta:
#         model = IngredientRecipe

class Query(ingredient_schema.Query,
            recipe_schema.Query,
            graphene.ObjectType):
    pass


class Mutation(user_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

"""
Query example : 
    query{
      allRecipes{
        id,
        name,
        steps,
        ingredientQuantity{
          quantity,
          ingredient{
            name
          }
        }
      }
    }
    
Wrap request inside 'query key' for json
"""