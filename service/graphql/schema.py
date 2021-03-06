import graphene

from ..graphql.mutation import Mutation
from ..graphql.query import Query


schema = graphene.Schema(query=Query, mutation=Mutation)
