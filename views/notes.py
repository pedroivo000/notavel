from flask import request, Response
from database.models import Note
import json


def get_notes(project_id=None, user_id=None):
    notes = Note.objects().to_json()

    return Response(notes, mimetype="application/json", status=200)


def create_note():
    body = request.get_json()
    note = Note(**body).save()
    id = note.id
    return {"id": str(id)}, 200


def update_note(**kwargs):
    pass


def get_note(note_id):
    pass


def delete_note(note_id):
    pass
