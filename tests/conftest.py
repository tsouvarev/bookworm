import os

from mongoengine import connect
from pytest import fixture
from werkzeug.test import Client

from .factories import BookFactory


@fixture
def book():
    return BookFactory.create()


@fixture
def app():
    from bookworm import create_app  # noqa: PLC0415

    app = create_app(with_csrf=False)
    app.config |= {'TESTING': True}

    return app


@fixture
def client(app):
    return Client(app)


@fixture(autouse=True)
def mongo_transaction():
    connection = connect(host=os.environ['MONGO_URI'])
    yield
    connection.drop_database('test')
