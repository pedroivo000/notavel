import pytest


def test_get_notes(test_app):

    response = test_app.get("api/v1/notes")
    record = response.get_json()

    assert response.status_code == 200
    assert len(record) == 3


def test_get_note_by_id(test_app):

    response = test_app.get("api/v1/notes/1")
    record = response.get_json()

    assert response.status_code == 200
    assert record["title"] == "test1"
    assert not record["archived"]
    assert len(record["content"]) == 2
    assert record["project_id"] == 1
    assert record["content"][0]["content"] == "test1"


@pytest.mark.parametrize("project_id,expected", [(1, 2), (2, 0)])
def test_get_notes_by_project(test_app, project_id, expected):

    response = test_app.get("api/v1/notes", query_string={"project_id": project_id})
    record = response.get_json()

    assert response.status_code == 200
    assert len(record) == expected


@pytest.mark.parametrize("project_id, note_id", [(2, 1), (1, 3)])
def test_move_note_to_project(test_app, project_id, note_id):
    payload = {"project_id": project_id}

    response = test_app.put(f"api/v1/notes/{note_id}", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["project_id"] == project_id


def test_put_note(test_app):
    payload = {"title": "new_title", "project_id": 2}

    response = test_app.put("api/v1/notes/1", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["title"] == "new_title"
    assert record["project_id"] == 2
    assert record["updated_at"] is not None


def test_archive_note(test_app):
    payload = {"archived": True}

    response = test_app.put("api/v1/notes/1", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["archived"]
    assert any(d["archived"] for d in record["content"])


def test_unarchive_note(test_app):

    test_app.put("api/v1/notes/1", json={"archived": True})
    response = test_app.put("api/v1/notes/1", json={"archived": False})
    record = response.get_json()

    assert response.status_code == 200
    assert not record["archived"]
    assert not any(d["archived"] for d in record["content"])
