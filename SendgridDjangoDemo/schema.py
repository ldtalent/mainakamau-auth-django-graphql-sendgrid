# SendgridDjangoDemo/schema.py
import graphene
from SendgridDjangoDemo.authentication.schema import Mutation as AuthMutation


class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation)
