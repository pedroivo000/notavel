from .db import db


class Note(db.Document):
    title = db.StringField()
    created_at = db.DateTimeField()
    project = db.StringField()
