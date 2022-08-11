from http.client import BAD_REQUEST, CONFLICT, CREATED

from flask.testing import FlaskClient

from . import test_email


def test_create_single_acronym(client: FlaskClient, authorization_header: str):

    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "aka",
                    "meaning": "also known as",
                    "comment": "a comment",
                    "company": "my company",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CREATED
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "aka",
                "company": "my company",
                "created_by": test_email,
                "comment": "a comment",
                "meaning": "also known as",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 1,
        }
    }


def test_create_two_different_acronym(client: FlaskClient, authorization_header: str):

    # First acronym
    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "abcd",
                    "meaning": "a..b..c..d",
                    "comment": "a comment1",
                    "company": "my company1",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CREATED
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "abcd",
                "company": "my company1",
                "created_by": test_email,
                "comment": "a comment1",
                "meaning": "a..b..c..d",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 1,
        }
    }
    # Second acronym
    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "efgh",
                    "meaning": "e..f..g..h",
                    "comment": "a comment2",
                    "company": "my company2",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CREATED
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "efgh",
                "company": "my company2",
                "created_by": test_email,
                "comment": "a comment2",
                "meaning": "e..f..g..h",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 2,
        }
    }


def test_create_two_same_acronym(client: FlaskClient, authorization_header: str):

    # First acronym
    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "abcd",
                    "meaning": "a..b..c..d",
                    "comment": "a comment",
                    "company": "my company",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CREATED
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "abcd",
                "company": "my company",
                "created_by": test_email,
                "comment": "a comment",
                "meaning": "a..b..c..d",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 1,
        }
    }

    # Second acronym
    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "abcd",
                    "meaning": "a..b..c..d",
                    "comment": "a comment",
                    "company": "my company",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CONFLICT


def test_create_two_similar_acronym(client: FlaskClient, authorization_header: str):

    # First acronym
    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "abcd",
                    "meaning": "a..b..c..d",
                    "comment": "a comment",
                    "company": "my company",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CREATED
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "abcd",
                "company": "my company",
                "created_by": test_email,
                "comment": "a comment",
                "meaning": "a..b..c..d",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 1,
        }
    }

    # Second acronym
    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "abcd",
                    "meaning": "a..b..c..d",
                    "comment": "an extended comment",
                    "company": "my company",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CREATED
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "abcd",
                "company": "my company",
                "created_by": test_email,
                "comment": "an extended comment",
                "meaning": "a..b..c..d",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 2,
        }
    }


def test_create_acronym_no_comment(client: FlaskClient, authorization_header: str):

    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "aka",
                    "meaning": "also known as",
                    "company": "my company",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == CREATED
    assert post_response.json == {
        "data": {
            "type": "acronyms",
            "attributes": {
                "last_modified_at": None,
                "acronym": "aka",
                "company": "my company",
                "created_by": test_email,
                "comment": None,
                "meaning": "also known as",
                "created_at": post_response.json["data"]["attributes"]["created_at"],
                "last_modified_by": None,
            },
            "id": 1,
        }
    }


def test_create_acronym_no_acronym(client: FlaskClient, authorization_header: str):

    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "meaning": "also known as",
                    "comment": "a comment",
                    "company": "my company",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == BAD_REQUEST


def test_create_acronym_no_meaning(client: FlaskClient, authorization_header: str):

    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "aka",
                    "comment": "a comment",
                    "company": "my company",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == BAD_REQUEST


def test_create_acronym_no_company(client: FlaskClient, authorization_header: str):

    post_response = client.post(
        "/api/acronyms",
        json={
            "data": {
                "type": "acronyms",
                "attributes": {
                    "acronym": "aka",
                    "meaning": "also known as",
                    "comment": "a comment",
                },
            }
        },
        headers={"Authorization": authorization_header},
    )
    assert post_response.status_code == BAD_REQUEST
