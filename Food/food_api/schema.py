import graphene
import graphql_jwt
from food_api.schemas.users import schema as user_schema
from food_api.schemas.ingredients import schema as ingredient_schema
from food_api.schemas.recipes import schema as recipe_schema


class Query(ingredient_schema.Query, recipe_schema.Query, user_schema.Query, graphene.ObjectType):
    pass


# class Mutation(user_schema.Mutation, recipe_schema.Mutation, graphene.ObjectType):
class Mutation(user_schema.Mutation, recipe_schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
