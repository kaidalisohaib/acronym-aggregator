import pytest
from app import app, db
from flask.testing import FlaskClient


@pytest.fixture
def client() -> FlaskClient:
    db.drop_all()
    db.create_all()
    db.session.commit()

    with app.test_client() as client:
        yield client

    db.drop_all()
    db.session.commit()
