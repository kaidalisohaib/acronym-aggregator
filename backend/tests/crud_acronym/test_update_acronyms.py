from http.client import BAD_REQUEST, CONFLICT, OK

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


def test_update_acronym(client: FlaskClient, authorization_header: str):
    acronym_1 = client.get("/api/acronyms/1").json
    acronym_1["data"]["attributes"]["acronym"] = "new acronym"
    post_response = client.patch(
        "/api/acronyms/1",
        json=acronym_1,
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == OK
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": post_response.json["data"]["attributes"][
                    "last_modified_at"
                ],
                "acronym": "new acronym",
                "company": "my company1",
                "created_by": test_email,
                "comment": "a comment1",
                "meaning": "also known as1",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": test_email,
            },
            "id": 1,
        }
    }


def test_update_same_two_acronym(client: FlaskClient, authorization_header: str):
    acronym_1 = client.get("/api/acronyms/1").json
    acronym_1["data"]["attributes"]["acronym"] = "new acronym"
    acronym_1["data"]["attributes"]["meaning"] = "new meaning"
    acronym_1["data"]["attributes"]["comment"] = "new comment"
    acronym_1["data"]["attributes"]["company"] = "new company"
    acronym_2 = client.get("/api/acronyms/2").json
    acronym_2["data"]["attributes"]["acronym"] = "new acronym"
    acronym_2["data"]["attributes"]["meaning"] = "new meaning"
    acronym_2["data"]["attributes"]["comment"] = "new comment"
    acronym_2["data"]["attributes"]["company"] = "new company"
    post_response = client.patch(
        "/api/acronyms/1",
        json=acronym_1,
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == OK
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": post_response.json["data"]["attributes"][
                    "last_modified_at"
                ],
                "acronym": "new acronym",
                "company": "new company",
                "created_by": test_email,
                "comment": "new comment",
                "meaning": "new meaning",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": test_email,
            },
            "id": 1,
        }
    }
    post_response = client.patch(
        "/api/acronyms/2",
        json=acronym_2,
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CONFLICT


def test_update_no_acronym_acronym(client: FlaskClient, authorization_header: str):
    acronym_1 = client.get("/api/acronyms/1").json
    acronym_1["data"]["attributes"]["acronym"] = None
    post_response = client.patch(
        "/api/acronyms/1",
        json=acronym_1,
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == BAD_REQUEST


def test_update_no_meaning_acronym(client: FlaskClient, authorization_header: str):
    acronym_1 = client.get("/api/acronyms/1").json
    acronym_1["data"]["attributes"]["meaning"] = None
    post_response = client.patch(
        "/api/acronyms/1",
        json=acronym_1,
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == BAD_REQUEST


def test_update_no_comment_acronym(client: FlaskClient, authorization_header: str):
    acronym_1 = client.get("/api/acronyms/1").json
    acronym_1["data"]["attributes"]["comment"] = None
    post_response = client.patch(
        "/api/acronyms/1",
        json=acronym_1,
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == OK

    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": post_response.json["data"]["attributes"][
                    "last_modified_at"
                ],
                "acronym": "aka1",
                "company": "my company1",
                "created_by": test_email,
                "comment": None,
                "meaning": "also known as1",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": test_email,
            },
            "id": 1,
        }
    }


def test_update_no_company_acronym(client: FlaskClient, authorization_header: str):
    acronym_1 = client.get("/api/acronyms/1").json
    acronym_1["data"]["attributes"]["company"] = None
    post_response = client.patch(
        "/api/acronyms/1",
        json=acronym_1,
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == BAD_REQUEST
