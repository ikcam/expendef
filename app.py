from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from graphql_server.flask import GraphQLView
from sqlalchemy import true


cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.settings')

    cors.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from service.models import Category, Transaction, User  # NOQA

    # CLI Commands
    from service.cli import user_cli

    app.cli.add_command(user_cli)

    @jwt.user_identity_loader
    def user_identity_lookup(user):  # NOQA
        return user.id if isinstance(user, User) else user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):  # NOQA
        identity = jwt_data["sub"]
        return User.query.filter(
            User.id == identity,
            User.is_active == true()
        ).first()

    # GraphQL
    from service import views
    from service.graphql.schema import schema

    app.add_url_rule(
        '/account/login/',
        view_func=views.login,
        methods=['POST']
    )
    app.add_url_rule(
        '/account/refresh/',
        view_func=views.refresh,
        methods=['POST']
    )

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema.graphql_schema,
            graphiql=True,
        )
    )

    return app
