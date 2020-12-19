from notavel.models import Project


def test_create_project(database):
    record = {"name": "test"}

    project = Project(**record)
    database.session.add(project)
    database.session.commit()

    assert Project.query.one()


def test_parent_project(database, test_project):
    record = {"name": "test", "parent_id": 1}

    project = Project(**record)
    database.session.add(project)
    database.session.commit()

    obj = database.session.query(Project).order_by(Project.id.desc()).first()
    assert obj.parent_id == 1

