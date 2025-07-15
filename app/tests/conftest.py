import pytest

from app.app import create_app
from app.models import Client, Parking, db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        client = Client(
            name="Test",
            surname="User",
            credit_card="1234567890123456",
            car_number="A123BC",
        )

        parking = Parking(
            address="Test Address",
            opened=True,
            count_places=10,
            count_available_places=5,
        )

        db.session.add(client)
        db.session.add(parking)
        db.session.commit()

        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
