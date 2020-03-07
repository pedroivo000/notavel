from datetime import datetime
import marshmallow_mongoengine as ma
from .db import db

# pylint: disable=E1101


class BaseDocument(db.Document):
    meta = {"abstract": True}

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()
    is_deleted = db.BooleanField(default=False)


class BulletPoint(BaseDocument):
    parent_note_id = db.ReferenceField("Note")
    content = db.StringField()
    type = db.StringField()


class Note(db.Document):
    title = db.StringField()
    created_at = db.DateTimeField()
    project = db.StringField()
    content = db.ListField(db.ReferenceField(BulletPoint))
    is_deleted = db.BooleanField(default=False)

    @property
    def creation_date(self):
        return self.id.generation_time if self.id else None

    def clean(self):
        if not self.created_at:
            self.created_at = datetime.now()


class BulletPointSchema(ma.ModelSchema):
    class Meta:
        model = BulletPoint


class NoteSchema(ma.ModelSchema):
    class Meta:
        model = Note

    content = ma.fields.List(ma.fields.Nested(BulletPointSchema))

