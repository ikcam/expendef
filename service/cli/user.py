import click
from flask.cli import AppGroup
from sqlalchemy import func

from service.models import User
from app import db


user_cli = AppGroup('user')


@user_cli.command('create')
@click.argument('email')
@click.argument('password')
@click.argument('first_name')
@click.argument('last_name')
def create_user(email, password, first_name, last_name):
    user = User.query.filter(
        func.lower(User.email) == func.lower(email)
    ).first()

    if user:
        click.echo('Email already exists.')
        return

    user = User(
        email=email,
        password='-',
        is_superuser=True,
        first_name=first_name,
        last_name=last_name
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    click.echo('User created with email "{}"'.format(user.email))
