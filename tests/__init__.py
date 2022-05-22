import os
import pytest

from app import create_app, db


@pytest.fixture
def app():
    os.environ['ENV'] = 'testing'
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
