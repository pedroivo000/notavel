from flask import request
from database.models import Note


def get_notes(**kwargs):
    pass


def create_note(**kwargs):
    body = request.get_json()
    note = Note(**kwargs).save()
    id = note.id
    return {"id": str(id)}, 200


def update_note(**kwargs):
    pass


def get_note(note_id):
    pass


def delete_note(note_id):
    pass
