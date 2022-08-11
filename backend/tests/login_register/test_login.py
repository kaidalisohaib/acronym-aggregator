from http.client import NOT_FOUND, OK, UNAUTHORIZED

import pytest
from flask.testing import FlaskClient


@pytest.fixture(autouse=True)
def create_account(client: FlaskClient):
    client.post(
        "/api/register",
        json={"email": "test@test.com", "password": "abcd1234"},
    )


def test_login(client: FlaskClient):

    post_response = client.post(
        "/api/login",
        json={"email": "test@test.com", "password": "abcd1234"},
    )
    assert post_response.status_code == OK
    assert "access_token" in post_response.json


def test_login_inexistent_user(client: FlaskClient):

    post_response = client.post(
        "/api/login",
        json={"email": "user@user.com", "password": "abcd1234"},
    )
    assert post_response.status_code == NOT_FOUND


def test_login_bad_password(client: FlaskClient):

    post_response = client.post(
        "/api/login",
        json={"email": "test@test.com", "password": "1234abcd"},
    )
    assert post_response.status_code == UNAUTHORIZED
