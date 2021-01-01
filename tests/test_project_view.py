def test_get_projects(test_app):

    response = test_app.get("api/v1/projects")
    record = response.get_json()

    assert response.status_code == 200
    assert len(record) == 2


def test_get_project_by_id(test_app):

    response = test_app.get("api/v1/projects/1")
    record = response.get_json()

    assert response.status_code == 200
    assert record["id"] == 1
    assert len(record["notes"]) == 2
    assert not record["archived"]


def test_post_project(test_app):
    payload = {"name": "test"}

    response = test_app.post("api/v1/projects", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["id"] == 3


def test_set_project_parent(test_app):
    payload = {"parent_id": 1}

    response = test_app.put("api/v1/projects/2", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["parent_id"] == 1


def test_archive_project(test_app):
    payload = {"archived": True}

    response = test_app.put("api/v1/projects/1", json=payload)
    record = response.get_json()

    assert response.status_code == 200
    assert record["archived"]
    assert record["notes"][0]["archived"]

    note_response = test_app.get("api/v1/notes/1")
    note_record = note_response.get_json()

    assert note_response.status_code == 200
    # assert if bullets are also archived if project is archived
    assert any(d["archived"] for d in note_record["content"])


def test_delete_project(test_app):

    response = test_app.delete("api/v1/projects/1")
    assert response.status_code == 204

    get_response = test_app.get("api/v1/projects/1")
    assert get_response.status_code == 404

    notes_response = test_app.get("api/v1/notes", query_string={"project_id": "1"})
    assert notes_response.status_code == 200
    assert notes_response.get_json() == []
