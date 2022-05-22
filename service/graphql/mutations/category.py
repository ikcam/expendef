from flask_jwt_extended import current_user, jwt_required
import graphene
from sqlalchemy import func

from app import db
from ..object import CategoryType
from ...models import Category
from ...utils import setallattrs


class CategoryCreateInput(graphene.InputObjectType):
    parent_id = graphene.Int(required=False)
    name = graphene.String(required=True)
    color = graphene.String(required=False)
    description = graphene.String(required=False)


class CategoryCreateMutation(graphene.Mutation):
    """
    # Create Category
    mutation ($txa: CategoryCreateInput!) {
        createCategory(categoryInput: $txa) {
            id
            category {
                parent {
                    id
                    name
                }
                name
                color
                description
            }
        }
    }

    # Parameters
    {
        "txa": {
            "name": "Food",
            "color": "333333",
            "description": "Food expenses"
        }
    }
    """

    category = graphene.Field(CategoryType)

    class Arguments:
        categoryInput = CategoryCreateInput(required=True)

    @jwt_required()
    def mutate(root, info, categoryInput):
        name = categoryInput.get('name')

        other_category = Category.query.filter(
            Category.user_id == current_user.id,
            func.lower(Category.name) == func.lower(name)
        ).first()

        if other_category:
            raise Exception("Category already exists.")

        category = Category(**categoryInput, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()

        return CategoryCreateMutation(category=category)


class CategoryUpdateInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    parent_id = graphene.Int(required=False)
    name = graphene.String(required=True)
    color = graphene.String(required=False)
    description = graphene.String(required=False)


class CategoryUpdateMutation(graphene.Mutation):
    """
    # Update Category
    mutation ($txa: CategoryUpdateInput!) {
        createCategory(categoryInput: $txa) {
            id
            category {
                parent {
                    id
                    name
                }
                name
                color
                description
            }
        }
    }

    # Parameters
    {
        "txa": {
            "id": 1,
            "name": "Gas",
            "color": "666666",
            "description": "Gas money"
        }
    }
    """

    category = graphene.Field(CategoryType)

    class Arguments:
        categoryInput = CategoryUpdateInput(required=True)

    @jwt_required()
    def mutate(root, info, categoryInput):
        id_ = categoryInput.pop('id')

        category = CategoryType.get_query(info).filter(
            Category.user_id == current_user.id,
            Category.id == id_
        ).first()

        if not category:
            raise Exception("Category not found.")

        name = categoryInput.get('name')

        other_category = Category.query.filter(
            Category.id != id_,
            Category.user_id == current_user.id,
            func.lower(Category.name) == func.lower(name)
        ).first()

        if other_category:
            raise Exception("Category already exists.")

        setallattrs(category, categoryInput)
        db.session.commit()

        return CategoryUpdateMutation(category=category)


class CategoryDeleteMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        categoryId = graphene.Int(required=True)

    @jwt_required()
    def mutate(root, info, categoryId):
        category = CategoryType.get_query(info).filter(
            Category.user_id == current_user.id,
            Category.id == categoryId
        ).first()

        if not category:
            raise Exception("Category not found.")

        db.session.delete(category)

        return CategoryDeleteMutation(success=True)
