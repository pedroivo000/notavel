import json
import pytest


def test_get_bullets(test_app):

    response = test_app.get("api/v1/bullets")
    record = response.get_json()

    assert response.status_code == 200
    assert len(record) == 4


@pytest.mark.parametrize("type,expected", [("bullet", 4), ("task", 0), ("idea", 0)])
def test_get_bullet_by_type(test_app, type, expected):

    response = test_app.get("/api/v1/bullets", query_string={"type": type})
    record = response.get_json()
    print(record)
    assert response.status_code == 200
    assert len(record) == expected


def test_get_bullet_by_id(test_app):

    response = test_app.get("api/v1/bullets/1")
    record = response.get_json()

    assert response.status_code == 200
    assert record["id"] == 1
    assert record["note_id"] == 1
    assert record["content"] == "test1"


def test_post_bullet(test_app):
    payload = {"content": "test", "type": "bullet", "note_id": 1, "order": 3}

    response = test_app.post("api/v1/bullets", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["id"] == 5


def test_put_bullet_content(test_app):
    payload = {"content": "new content"}

    response = test_app.put("api/v1/bullets/1", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["id"] == 1
    assert record["content"] == "new content"


def test_put_bullet_parent_id(test_app):
    payload = {"parent_id": 1, "order": 1}

    response = test_app.put("api/v1/bullets/2", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["id"] == 2
    assert record["parent_id"] == 1
    assert record["order"] == 1

