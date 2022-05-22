from flask_jwt_extended import current_user, jwt_required
import graphene

from app import db
from ..object import TransactionType
from ...models import Transaction
from ...utils import setallattrs


class TransactionCreateInput(graphene.InputObjectType):
    category_id = graphene.Int(required=False)
    description = graphene.String(required=False)
    is_income = graphene.Boolean(required=False)
    date = graphene.DateTime(required=True)
    amount = graphene.Float(required=True)


class TransactionCreateMutation(graphene.Mutation):
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transactionInput = TransactionCreateInput(required=True)

    @jwt_required()
    def mutate(root, info, transactionInput):
        transaction = Transaction(**transactionInput, user_id=current_user.id)
        db.session.add(transaction)
        db.session.commit()

        return TransactionCreateMutation(transaction=transaction)


class TransactionUpdateInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    category_id = graphene.Int(required=False)
    description = graphene.String(required=False)
    is_income = graphene.Boolean(required=False)
    date = graphene.DateTime(required=True)
    amount = graphene.Float(required=True)


class TransactionUpdateMutation(graphene.Mutation):
    transaction = graphene.Field(TransactionType)

    class Arguments:
        transactionInput = TransactionUpdateInput(required=True)

    @jwt_required()
    def mutate(root, info, transactionInput):
        id_ = transactionInput.pop('id')
        transaction = TransactionType.get_query(info).filter(
            Transaction.id == id_
        ).first()

        if not transaction:
            raise Exception('Transaction not found')

        setallattrs(transaction, transactionInput)
        db.session.commit()

        return TransactionUpdateMutation(transaction=transaction)


class TransactionDeleteMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        transactionId = graphene.Int(required=True)

    @jwt_required()
    def mutate(root, info, transactionId):
        transaction = TransactionType.get_query(info).filter(
            Transaction.id == transactionId
        ).first()

        if not transaction:
            raise Exception('Transaction not found')

        db.session.delete(transaction)

        return TransactionDeleteMutation(success=True)
