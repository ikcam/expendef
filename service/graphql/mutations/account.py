from flask_jwt_extended import current_user, jwt_required
import graphene

from app import db
from ..object import UserType


class AccountUpdateInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)


class AccountUpdateMutation(graphene.Mutation):
    """
    # Update Account
    mutation ($txa: AccountUpdateInput!) {
        updateAccount(categoryInput: $txa) {
            user {
                id
                firstName
                lastName
            }
        }
    }

    # Parameters
    {
        "txa": {
            "firstName": "John",
            "lastName": "Smith",
        }
    }
    """

    user = graphene.Field(UserType)

    class Arguments:
        userInput = AccountUpdateInput(required=True)

    @jwt_required()
    def mutate(root, info, userInput):
        user = UserType.get_query(info).get(current_user.id)
        user.first_name = userInput.get('first_name')
        user.last_name = userInput.get('last_name')
        db.session.commit()

        return AccountUpdateMutation(user=user)


class AccountPasswordChangeInput(graphene.InputObjectType):
    old_password = graphene.String(required=True)
    new_password1 = graphene.String(required=True)
    new_password2 = graphene.String(required=True)


class AccountPasswordChangeMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        passwordInput = AccountPasswordChangeInput(required=True)

    @jwt_required()
    def mutate(root, info, passwordInput):
        user = UserType.get_query(info).get(current_user.id)
        old_password = passwordInput.get('old_password')
        new_password1 = passwordInput.get('new_password1')
        new_password2 = passwordInput.get('new_password2')

        if new_password1 != new_password2:
            raise Exception("Passwords do not match.")
        elif not user.check_password(old_password):
            raise Exception("Old password is incorrect.")

        user.set_password(new_password2)
        db.session.commit()
        return AccountPasswordChangeMutation(success=True)
