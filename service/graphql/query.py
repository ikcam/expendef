from flask_jwt_extended import current_user, jwt_required
import graphene
from graphene import relay

from .object import CategoryType, TransactionType, UserType
from ..models import Category, Transaction


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    categories = graphene.List(
        CategoryType,
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    transactions = graphene.List(
        TransactionType,
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    users = graphene.List(
        UserType,
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    @jwt_required()
    def resolve_categories(self, info, first=None, skip=None):
        query = CategoryType.get_query(info).filter(
            Category.user_id == current_user.id
        )

        if skip:
            query = query[skip:]

        if first:
            query = query[:first]

        return query

    @jwt_required()
    def resolve_transactions(self, info, first=None, skip=None):
        query = TransactionType.get_query(info).filter(
            Transaction.user_id == current_user.id
        )

        if skip:
            query = query[skip:]

        if first:
            query = query[:first]

        return query

    @jwt_required()
    def resolve_users(self, info, first=None, skip=None):
        if not current_user.is_superuser:
            raise Exception('You are not allowed to access this data')

        query = UserType.get_query(info)

        if skip:
            query = query[skip:]

        if first:
            query = query[:first]

        return query
