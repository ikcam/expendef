import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from service.models import Category, Transaction, User


class CategoryType(SQLAlchemyObjectType):
    parent = graphene.Field(lambda: CategoryType)
    user = graphene.Field(lambda: UserType)

    class Meta:
        model = Category

    def resolve_parent(self, info):
        return Category.query.filter(Category.id == self.parent_id).first()

    def resolve_user(self, info):
        return User.query.filter(User.id == self.user_id).first()


class TransactionType(SQLAlchemyObjectType):
    category = graphene.Field(lambda: CategoryType)
    user = graphene.Field(lambda: UserType)

    class Meta:
        model = Transaction

    def resolve_category(self, info):
        return Category.query.filter(Category.id == self.parent_id).first()

    def resolve_user(self, info):
        return User.query.filter(User.id == self.user_id).first()


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        exclude_fields = ('password',)
