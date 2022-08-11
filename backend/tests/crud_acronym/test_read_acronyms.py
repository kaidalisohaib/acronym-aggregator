from http.client import NOT_FOUND, OK

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


def test_get_existing_acronym(client: FlaskClient):

    get_response = client.get("/api/acronyms/1")
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "aka1",
                "company": "my company1",
                "created_by": test_email,
                "comment": "a comment1",
                "meaning": "also known as1",
                "created_at": get_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 1,
        }
    }


def test_get_non_existing_acronym(client: FlaskClient):

    get_response = client.get("/api/acronyms/11")
    assert get_response.status_code == NOT_FOUND


def test_get_two_existing_acronym(client: FlaskClient):

    get_response = client.get("/api/acronyms/1")
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "aka1",
                "company": "my company1",
                "created_by": test_email,
                "comment": "a comment1",
                "meaning": "also known as1",
                "created_at": get_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 1,
        }
    }
    get_response = client.get("/api/acronyms/2")
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "aka2",
                "company": "my company2",
                "created_by": test_email,
                "comment": "a comment2",
                "meaning": "also known as2",
                "created_at": get_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 2,
        }
    }


def test_get_all_acronyms(client: FlaskClient):

    get_response = client.get("/api/acronyms")
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": [
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka1",
                    "company": "my company1",
                    "created_by": test_email,
                    "comment": "a comment1",
                    "meaning": "also known as1",
                    "created_at": get_response.json["data"][0]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 1,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka2",
                    "company": "my company2",
                    "created_by": test_email,
                    "comment": "a comment2",
                    "meaning": "also known as2",
                    "created_at": get_response.json["data"][1]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 2,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka3",
                    "company": "my company3",
                    "created_by": test_email,
                    "comment": "a comment3",
                    "meaning": "also known as3",
                    "created_at": get_response.json["data"][2]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 3,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka4",
                    "company": "my company4",
                    "created_by": test_email,
                    "comment": "a comment4",
                    "meaning": "also known as4",
                    "created_at": get_response.json["data"][3]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 4,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka5",
                    "company": "my company5",
                    "created_by": test_email,
                    "comment": "a comment5",
                    "meaning": "also known as5",
                    "created_at": get_response.json["data"][4]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 5,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka6",
                    "company": "my company6",
                    "created_by": test_email,
                    "comment": "a comment6",
                    "meaning": "also known as6",
                    "created_at": get_response.json["data"][5]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 6,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka7",
                    "company": "my company7",
                    "created_by": test_email,
                    "comment": "a comment7",
                    "meaning": "also known as7",
                    "created_at": get_response.json["data"][6]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 7,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka8",
                    "company": "my company8",
                    "created_by": test_email,
                    "comment": "a comment8",
                    "meaning": "also known as8",
                    "created_at": get_response.json["data"][7]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 8,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka9",
                    "company": "my company9",
                    "created_by": test_email,
                    "comment": "a comment9",
                    "meaning": "also known as9",
                    "created_at": get_response.json["data"][8]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 9,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka10",
                    "company": "my company10",
                    "created_by": test_email,
                    "comment": "a comment10",
                    "meaning": "also known as10",
                    "created_at": get_response.json["data"][9]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 10,
            },
        ],
        "meta": {"item_count": 10},
    }


def test_get_filter_id_acronym(client: FlaskClient):

    get_response = client.get("/api/acronyms", query_string={"filter[id]": 1})
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": [
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_by": None,
                    "created_at": get_response.json["data"][0]["attributes"][
                        "created_at"
                    ],
                    "comment": "a comment1",
                    "acronym": "aka1",
                    "meaning": "also known as1",
                    "last_modified_at": None,
                    "company": "my company1",
                    "created_by": "test@test.com",
                },
                "id": 1,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_by": None,
                    "created_at": get_response.json["data"][1]["attributes"][
                        "created_at"
                    ],
                    "comment": "a comment10",
                    "acronym": "aka10",
                    "meaning": "also known as10",
                    "last_modified_at": None,
                    "company": "my company10",
                    "created_by": "test@test.com",
                },
                "id": 10,
            },
        ],
        "meta": {"item_count": 2},
    }


def test_get_filter_acronym_acronym(client: FlaskClient):

    get_response = client.get("/api/acronyms", query_string={"filter[acronym]": "a8"})
    print(get_response.json)
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": [
            {
                "type": "acronyms",
                "attributes": {
                    "acronym": "aka8",
                    "created_at": get_response.json["data"][0]["attributes"][
                        "created_at"
                    ],
                    "created_by": "test@test.com",
                    "company": "my company8",
                    "last_modified_at": None,
                    "comment": "a comment8",
                    "meaning": "also known as8",
                    "last_modified_by": None,
                },
                "id": 8,
            }
        ],
        "meta": {"item_count": 1},
    }


def test_get_filter_meaning_acronym(client: FlaskClient):

    get_response = client.get(
        "/api/acronyms", query_string={"filter[meaning]": "known as4"}
    )
    print(get_response.json)
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": [
            {
                "type": "acronyms",
                "attributes": {
                    "acronym": "aka4",
                    "created_at": get_response.json["data"][0]["attributes"][
                        "created_at"
                    ],
                    "created_by": "test@test.com",
                    "company": "my company4",
                    "last_modified_at": None,
                    "comment": "a comment4",
                    "meaning": "also known as4",
                    "last_modified_by": None,
                },
                "id": 4,
            }
        ],
        "meta": {"item_count": 1},
    }


def test_get_filter_comment_acronym(client: FlaskClient):

    get_response = client.get("/api/acronyms", query_string={"filter[comment]": "ent4"})
    print(get_response.json)
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": [
            {
                "type": "acronyms",
                "attributes": {
                    "acronym": "aka4",
                    "created_at": get_response.json["data"][0]["attributes"][
                        "created_at"
                    ],
                    "created_by": "test@test.com",
                    "company": "my company4",
                    "last_modified_at": None,
                    "comment": "a comment4",
                    "meaning": "also known as4",
                    "last_modified_by": None,
                },
                "id": 4,
            }
        ],
        "meta": {"item_count": 1},
    }


def test_get_sorting_all_acronym(client: FlaskClient):

    get_response = client.get(
        "/api/acronyms",
        query_string={"sorting[column]": "acronym", "sorting[ascending]": False},
    )
    print(get_response.json)
    assert get_response.status_code == OK
    assert get_response.json == {
        "data": [
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka9",
                    "company": "my company9",
                    "created_by": test_email,
                    "comment": "a comment9",
                    "meaning": "also known as9",
                    "created_at": get_response.json["data"][0]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 9,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka8",
                    "company": "my company8",
                    "created_by": test_email,
                    "comment": "a comment8",
                    "meaning": "also known as8",
                    "created_at": get_response.json["data"][1]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 8,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka7",
                    "company": "my company7",
                    "created_by": test_email,
                    "comment": "a comment7",
                    "meaning": "also known as7",
                    "created_at": get_response.json["data"][2]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 7,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka6",
                    "company": "my company6",
                    "created_by": test_email,
                    "comment": "a comment6",
                    "meaning": "also known as6",
                    "created_at": get_response.json["data"][3]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 6,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka5",
                    "company": "my company5",
                    "created_by": test_email,
                    "comment": "a comment5",
                    "meaning": "also known as5",
                    "created_at": get_response.json["data"][4]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 5,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka4",
                    "company": "my company4",
                    "created_by": test_email,
                    "comment": "a comment4",
                    "meaning": "also known as4",
                    "created_at": get_response.json["data"][5]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 4,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka3",
                    "company": "my company3",
                    "created_by": test_email,
                    "comment": "a comment3",
                    "meaning": "also known as3",
                    "created_at": get_response.json["data"][6]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 3,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka2",
                    "company": "my company2",
                    "created_by": test_email,
                    "comment": "a comment2",
                    "meaning": "also known as2",
                    "created_at": get_response.json["data"][7]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 2,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka10",
                    "company": "my company10",
                    "created_by": test_email,
                    "comment": "a comment10",
                    "meaning": "also known as10",
                    "created_at": get_response.json["data"][8]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 10,
            },
            {
                "type": "acronyms",
                "attributes": {
                    "last_modified_at": None,
                    "acronym": "aka1",
                    "company": "my company1",
                    "created_by": test_email,
                    "comment": "a comment1",
                    "meaning": "also known as1",
                    "created_at": get_response.json["data"][9]["attributes"][
                        "created_at"
                    ],
                    "last_modified_by": None,
                },
                "id": 1,
            },
        ],
        "meta": {"item_count": 10},
    }
