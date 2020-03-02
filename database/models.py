from datetime import datetime
import marshmallow_mongoengine as ma
from .db import db

# pylint: disable=E1101


class Note(db.Document):
    title = db.StringField()
    created_at = db.DateTimeField()
    project = db.StringField()
    is_deleted = db.BooleanField(default=False)

    @property
    def creation_date(self):
        return self.id.generation_time if self.id else None

    def clean(self):
        if not self.created_at:
            self.created_at = datetime.now()


class NoteSchema(ma.ModelSchema):
    class Meta:
        model = Note
