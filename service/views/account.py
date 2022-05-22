from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, jwt_required
)
from sqlalchemy import func

from ..models import User


def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter(
        func.lower(User.email) == func.lower(email)
    ).first()

    if not user or not user.check_password(password):
        return jsonify(detail='Invalid email or password'), 400
    if not user.is_active:
        return jsonify(detail='User is not active'), 403

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    return jsonify(
        access=access_token,
        refresh=refresh_token
    ), 200


@jwt_required(refresh=True, locations='json')
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access=access_token), 200
