from notavel.models import Note


def test_create_note(database):
    title = "test"

    note = Note(title=title)
    database.session.add(note)
    database.session.commit()

    note = Note.query.first()
    assert note.title == title
