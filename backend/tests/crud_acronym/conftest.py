import pytest
from flask.testing import FlaskClient

from ..crud_acronym import test_email, test_password


@pytest.fixture(autouse=True)
def create_test_user(client: FlaskClient):
    client.post(
        "/api/register",
        json={
            "email": test_email,
            "password": test_password,
        },
    )


@pytest.fixture
def authorization_header(client: FlaskClient) -> str:
    login_response = client.post(
        "/api/login",
        json={
            "email": test_email,
            "password": test_password,
        },
    )
    auth_header = "Bearer " + login_response.json["access_token"]
    return auth_header
