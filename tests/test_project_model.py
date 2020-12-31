from notavel.models import Bullet, Project, Note


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


def test_get_child_notes(database, test_project_with_note):

    obj = Project.query.first()
    assert len(obj.notes) == 1


def test_archive_project(database):

    project = Project(name="test project, not archived")
    note = Note(title="test note", project_id=1)

    database.session.add_all([project, note])
    database.session.commit()
    assert not project.archived

    project.archived = True
    database.session.commit()

    assert project.archived
    assert note.archived


def test_unarchive_project(database):

    project = Project(name="test project, archived", archived=True)
    note = Note(title="test note, archived", project_id=1, archived=True)
    database.session.add_all([project, note])
    database.session.commit()
    assert project.archived
    assert note.archived

    project.archived = False
    database.session.commit()
    assert not project.archived
    assert not note.archived


def test_get_project_tasks(database):

    project = Project(name="test project, with task")
    note = Note(title="test note, with task", project_id=1)
    task = Bullet(content="test task", note_id=1, order=1, type="task")

    database.session.add_all([project, note, task])
    database.session.commit()

    obj = database.session.query(Bullet).first()
    assert obj.project_id == 1
    # assert database.session.query(Bullet).filter_by(type="task", project_id=1).one()


def test_create_project_task(database):
    project = Project(name="test project, with task")
    task = Bullet(content="test task", order=1, type="task", project_id=1)

    database.session.add_all([project, task])
    database.session.commit()
    obj = database.session.query(Bullet).first()

    assert obj.project_id == 1
    assert database.session.query(Project).one()

