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
