from http.client import NO_CONTENT, NOT_FOUND

import pytest
from flask.testing import FlaskClient

from . import test_email


@pytest.fixture(autouse=True)
def create_10_acronym(client: FlaskClient, authorization_header: str):
    for index in range(10):
        index += 1
        client.post(
            "/api/acronyms",
            json={
                "data": {
                    "type": "acronyms",
                    "attributes": {
                        "acronym": f"aka{index}",
                        "meaning": f"also known as{index}",
                        "comment": f"a comment{index}",
                        "company": f"my company{index}",
                    },
                }
            },
            headers={"Authorization": authorization_header},
        )


def test_delete_single_acronym(client: FlaskClient, authorization_header: str):
    get_response = client.get("/api/acronyms")
    assert get_response.json["meta"]["item_count"] == 10
    delete_response = client.delete(
        "/api/acronyms/1", headers={"Authorization": authorization_header}
    )
    assert delete_response.status_code == NO_CONTENT
    get_response = client.get("/api/acronyms/1")
    assert get_response.status_code == NOT_FOUND
    get_response = client.get("/api/acronyms")
    assert get_response.json["meta"]["item_count"] == 9


def test_delete_two_acronym(client: FlaskClient, authorization_header: str):
    get_response = client.get("/api/acronyms")
    assert get_response.json["meta"]["item_count"] == 10
    delete_response = client.delete(
        "/api/acronyms/1", headers={"Authorization": authorization_header}
    )
    assert delete_response.status_code == NO_CONTENT
    get_response = client.get("/api/acronyms/1")
    assert get_response.status_code == NOT_FOUND
    get_response = client.get("/api/acronyms")
    assert get_response.json["meta"]["item_count"] == 9

    delete_response = client.delete(
        "/api/acronyms/2", headers={"Authorization": authorization_header}
    )
    assert delete_response.status_code == NO_CONTENT
    get_response = client.get("/api/acronyms/2")
    assert get_response.status_code == NOT_FOUND
    get_response = client.get("/api/acronyms")
    assert get_response.json["meta"]["item_count"] == 8


def test_delete_inexistent_acronym(client: FlaskClient, authorization_header: str):
    get_response = client.get("/api/acronyms")
    assert get_response.json["meta"]["item_count"] == 10
    delete_response = client.delete(
        "/api/acronyms/1", headers={"Authorization": authorization_header}
    )
    assert delete_response.status_code == NO_CONTENT
    get_response = client.get("/api/acronyms/1")
    assert get_response.status_code == NOT_FOUND
    get_response = client.get("/api/acronyms")
    assert get_response.json["meta"]["item_count"] == 9
    delete_response = client.delete(
        "/api/acronyms/1", headers={"Authorization": authorization_header}
    )
    assert delete_response.status_code == NOT_FOUND
    get_response = client.get("/api/acronyms/1")
    assert get_response.status_code == NOT_FOUND
    get_response = client.get("/api/acronyms")
    assert get_response.json["meta"]["item_count"] == 9
