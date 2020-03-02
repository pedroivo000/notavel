from flask import request
from database.models import Note, NoteSchema

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


def get_notes(project_id=None, user_id=None):
    # notes = Note.objects().to_json()
    notes = Note.objects()
    # notes_schema = NoteSchema(many=True)
    # print(note_schema.dump(notes))
    # return note_schema.dump(notes)
    return notes_schema.dump(notes), 200


def create_note():
    body = request.get_json()
    note = Note(**body).save()
    id = note.id
    return {"id": str(id)}, 200


def update_note(**kwargs):
    pass


def get_note(note_id):
    note = Note.objects.get(id=note_id)

    return note_schema.dump(note), 200


def delete_note(note_id):
    pass
