from http.client import CONFLICT, NO_CONTENT, UNPROCESSABLE_ENTITY

from flask.testing import FlaskClient


def test_create_account(client: FlaskClient):

    post_response = client.post(
        "/api/register",
        json={"email": "test@test.com", "password": "abcd1234"},
    )
    assert post_response.status_code == NO_CONTENT


def test_create_wrong_email_account(client: FlaskClient):

    post_response = client.post(
        "/api/register",
        json={"email": "tssft'']]asd", "password": "abcd1234"},
    )
    assert post_response.status_code == UNPROCESSABLE_ENTITY


def test_create_short_email_account(client: FlaskClient):

    post_response = client.post(
        "/api/register",
        json={"email": "a@a", "password": "abcd1234"},
    )
    assert post_response.status_code == UNPROCESSABLE_ENTITY


def test_create_short_password_account(client: FlaskClient):

    post_response = client.post(
        "/api/register",
        json={"email": "test@test.com", "password": "abcd"},
    )
    assert post_response.status_code == UNPROCESSABLE_ENTITY


def test_create_existing_account(client: FlaskClient):

    post_response = client.post(
        "/api/register",
        json={"email": "test@test.com", "password": "abcd1234"},
    )
    assert post_response.status_code == NO_CONTENT
    post_response = client.post(
        "/api/register",
        json={"email": "test@test.com", "password": "1234abcd"},
    )
    assert post_response.status_code == CONFLICT
