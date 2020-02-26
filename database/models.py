from .db import db


class Note(db.Document):
    title = db.StringField()
    created_at = db.DateTimeField()
    project = db.StringField()

    @property
    def id(self):
        return self.id

    @property
    def created_at(self):
        return self.id.generation_time
