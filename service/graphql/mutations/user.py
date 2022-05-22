import graphene
from sqlalchemy import func
from flask_jwt_extended import current_user, jwt_required

from app import db
from ..object import UserType
from ...models import User
from ...utils import setallattrs


class UserCreateInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password1 = graphene.String(required=True)
    password2 = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    is_active = graphene.Boolean(required=False)
    is_superuser = graphene.Boolean(required=False)


class UserCreateMutation(graphene.Mutation):
    """
    # Create User
    mutation ($txa: UserCreateInput!) {
        createUser(categoryInput: $txa) {
            id
            email
            firstName
            lastName
        }
    }

    # Parameters
    {
        "txa": {
            "email": "jane@test.com",
            "password1": "ThePassword",
            "password2": "ThePassword",
            "firstName": "Jane",
            "lastName": "Doe",
        }
    }
    """

    Output = UserType

    class Arguments:
        userInput = UserCreateInput(required=True)

    @jwt_required()
    def mutate(root, info, userInput):
        email = userInput.get('email')
        password1 = userInput.pop('password1')
        password2 = userInput.pop('password2')

        other_user = User.query.filter(
            func.lower(User.email) == func.lower(email)
        )

        if other_user:
            raise Exception("User already exists.")
        elif password1 != password2:
            raise Exception("Passwords do not match.")

        user = User(**userInput)
        user.set_password(password2)
        db.session.add(user)
        db.session.commit()

        return UserCreateMutation(user=user)


class UserUpdateInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    is_active = graphene.Boolean(required=False)
    is_superuser = graphene.Boolean(required=False)


class UserUpdateMutation(graphene.Mutation):
    """
    # Update User
    mutation ($txa: UserUpdateInput!) {
        createUser(categoryInput: $txa) {
            user {
                id
                email
                firstName
                lastName
            }
        }
    }

    # Parameters
    {
        "txa": {
            "email": "jane@test.com",
            "password1": "ThePassword",
            "password2": "ThePassword",
            "firstName": "Jane",
            "lastName": "Doe",
        }
    }
    """

    Output = UserType

    class Arguments:
        userInput = UserUpdateInput(required=True)

    @jwt_required()
    def mutate(root, info, userInput):
        id_ = userInput.get('id')

        user = UserType.get_query(info).filter(
            User.id == id_
        ).first()

        if not user:
            raise Exception("User not found.")

        setallattrs(user, userInput)
        db.session.commit()

        return UserUpdateMutation(user=user)


class UserPasswordChangeInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    new_password1 = graphene.String(required=True)
    new_password2 = graphene.String(required=True)


class UserPasswordChangeMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        passwordInput = UserPasswordChangeInput(required=True)

    @jwt_required()
    def mutate(root, info, passwordInput):
        if not current_user.is_superuser:
            raise Exception("You are not allowed to change password.")

        id_ = passwordInput.get('id')
        user = UserType.get_query(info).filter(User.id == id_).first()

        if not user:
            raise Exception("User not found.")

        new_password1 = passwordInput.get('new_password1')
        new_password2 = passwordInput.get('new_password2')

        if new_password1 != new_password2:
            raise Exception("Passwords do not match.")

        user.set_password(new_password2)
        db.session.commit()
        return UserPasswordChangeMutation(success=True)


class UserDeleteMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        userId = graphene.Int(required=True)

    @jwt_required()
    def mutate(root, info, userId):
        if not current_user.is_superuser:
            raise Exception("You are not allowed to change password.")

        user = UserType.get_query(info).filter(
            User.id == userId
        ).first()

        if not user:
            raise Exception("User not found.")
        elif user == current_user:
            raise Exception("You cannot delete yourself.")

        db.session.delete(user)
        return UserDeleteMutation(success=True)
