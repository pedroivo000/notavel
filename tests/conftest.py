import pytest
from notavel.config import TestConfig
from notavel import create_app
from notavel import db
import notavel.models


@pytest.fixture
def test_data():
    data = {
        "Project": [{"name": "test-project-1"}, {"name": "test-project-2"}],
        "Note": [
            {"title": "test1", "project_id": 1},
            {"title": "test2", "project_id": 1},
            {"title": "test3"},
        ],
        "Bullet": [
            {
                "content": "test1",
                "order": 1,
                "type": "bullet",
                "note_id": 1,
                "priority": 1,
            },
            {
                "content": "test2",
                "order": 2,
                "type": "bullet",
                "note_id": 1,
                "priority": 1,
            },
            {
                "content": "test3",
                "order": 1,
                "type": "bullet",
                "note_id": 3,
                "priority": 1,
            },
            {
                "content": "test4",
                "order": 1,
                "type": "bullet",
                "note_id": 3,
                "priority": 1,
                "parent_id": 1,
            },
        ],
    }

    return data


@pytest.fixture
def test_notes():
    notes = [
        {
            "title": "test1",
            "content": [
                {
                    "content": "test1",
                    "order": 1,
                    "type": "bullet",
                    "note_id": 1,
                    "priority": 1,
                },
                {
                    "content": "test2",
                    "order": 2,
                    "type": "bullet",
                    "note_id": 1,
                    "priority": 1,
                },
            ],
        },
        {"title": "test2", "content": []},
        {
            "title": "test3",
            "content": [
                {
                    "content": "test3",
                    "order": 1,
                    "type": "bullet",
                    "note_id": 3,
                    "priority": 1,
                },
                {
                    "content": "test4",
                    "order": 1,
                    "type": "bullet",
                    "note_id": 3,
                    "priority": 1,
                    "parent_id": 1,
                },
            ],
        },
    ]

    return notes


@pytest.fixture
def test_app(test_data):
    app = create_app(TestConfig)

    # Code from: https://testdriven.io/blog/flask-pytest/
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        # Establish an application context
        with app.app_context():
            db.drop_all()
            db.create_all()

            # Use this for test_data fixture
            for k, v in test_data.items():
                # print(k, v)
                for obj in v:
                    record = getattr(notavel.models, k)(**obj)
                    db.session.add(record)
                    db.session.commit()

            # use this for test_notes fixture
            # as dicts are ordered on python 3.7+, we don't need to worry about
            # the order that records are created, as long as the order of test_data
            # is correct:
            # for note in test_notes:
            #     # create Note object
            #     n = notavel.models.Note(title=note["title"])

            #     for bullet in note["content"]:
            #         n.content.append(notavel.models.Bullet(**bullet))
            #     db.session.add(n)
            #     db.session.commit()

            # this is where the testing happens!
            yield test_client
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope="function")
def database(test_app):
    db.drop_all()
    db.create_all()

    yield db


@pytest.fixture
def test_project(database):
    name = "test"

    project = notavel.models.Project(name=name)
    database.session.add(project)
    database.session.commit()


@pytest.fixture
def test_note(database):
    title = "test"

    note = notavel.models.Note(title=title)
    database.session.add(note)
    database.session.commit()


@pytest.fixture
def test_bullet(database, test_note):
    content = "test"
    order = 1
    type = "bullet"
    note_id = 1

    bullet = notavel.models.Bullet(
        content=content, order=order, type=type, note_id=note_id
    )
    database.session.add(bullet)
    database.session.commit()
