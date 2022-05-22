import graphene

from . import mutations


class Mutation(graphene.ObjectType):
    # Account
    account_update = mutations.AccountUpdateMutation.Field()
    account_change_password = mutations.AccountPasswordChangeMutation.Field()
    # Category
    category_create = mutations.CategoryCreateMutation.Field()
    category_update = mutations.CategoryUpdateMutation.Field()
    category_delete = mutations.CategoryDeleteMutation.Field()
    # Transaction
    transaction_create = mutations.TransactionCreateMutation.Field()
    transaction_update = mutations.TransactionUpdateMutation.Field()
    transaction_delete = mutations.TransactionDeleteMutation.Field()
    # User
    user_create = mutations.UserCreateMutation.Field()
    user_delete = mutations.UserDeleteMutation.Field()
    user_set_password = mutations.UserPasswordChangeMutation.Field()
    user_update = mutations.UserUpdateMutation.Field()
