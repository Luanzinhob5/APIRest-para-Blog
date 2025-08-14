import pytest
from app import criar_app, db
from app.config import TestConfig

@pytest.fixture(scope='module')
def app():
    app = criar_app(TestConfig)

    yield app

@pytest.fixture(scope='function')
def client(app):
    with app.app_context():

        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()