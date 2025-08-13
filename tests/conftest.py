import pytest
from app import criar_app, db

@pytest.fixture(scope='module')
def app():
    app = criar_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    yield app

@pytest.fixture(scope='function')
def client(app):
    with app.app_context():

        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()