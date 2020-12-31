import notavel
from notavel.models import Note, Bullet


def test_create_note(database):
    title = "test"

    note = Note(title=title)
    database.session.add(note)
    database.session.commit()

    note = Note.query.first()
    assert note.title == title


def test_update_note_without_unarchiving_bullet(database):

    note = Note(title="test note, not archived")
    bullet1 = Bullet(
        content="test bullet, archived",
        note_id=1,
        archived=True,
        order=1,
        type="bullet",
    )
    database.session.add_all([note, bullet1])
    database.session.commit()

    assert bullet1.archived

    note.title = "modified title, still not archived"
    database.session.commit()

    assert bullet1.archived


def test_archive_note(database, test_bullet):
    note = Note.query.first()
    note.archived = True
    database.session.commit()

    assert note.archived
    bullet = note.content[0]

    assert bullet.archived  # test if bullet is also archived


def test_unarchive_note(database, test_archived_note):

    note = Note.query.first()
    note.archived = False
    database.session.commit()

    bullet = note.content[0]

    assert not bullet.archived  # test if bullet is not archived

