from datetime import datetime
from notavel import db, ma


class Bullet(db.Model):
    __tablename__ = "bullet"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), index=True)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    __mapper_args__ = {
        "polymorphic_identity": "bullet",
        "polymorphic_on": type,
    }

    def __repr__(self):
        return str(self.__dict__)


class BulletSchema(ma.ModelSchema):
    class Meta:
        model = Bullet
        sqla_session = db.session


class Task(Bullet):
    __tablename__ = "task"
    id = db.Column(db.Integer, db.ForeignKey("bullet.id"), primary_key=True)
    due_at = db.Column(db.DateTime)
    # priority = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    __mapper_args__ = {
        "polymorphic_identity": "task",
    }


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = Task
        sqla_session = db.session


# class BaseDocument(db.Document):
#     meta = {"abstract": True}

#     created_at = db.DateTimeField()
#     updated_at = db.DateTimeField()
#     is_deleted = db.BooleanField(default=False)


# class BulletPoint(BaseDocument):
#     parent_note_id = db.ListField(db.ReferenceField("Note"))
#     content = db.StringField()
#     type = db.StringField()


# class Note(db.Document):
#     title = db.StringField()
#     created_at = db.DateTimeField()
#     project = db.StringField()
#     content = db.ListField(db.ReferenceField(BulletPoint))
#     is_deleted = db.BooleanField(default=False)

#     @property
#     def creation_date(self):
#         return self.id.generation_time if self.id else None

#     def clean(self):
#         if not self.created_at:
#             self.created_at = datetime.now()


# class BulletPointSchema(ma.ModelSchema):
#     class Meta:
#         model = BulletPoint

#     parent_note_id = ma.fields.List(
#         ma.fields.Nested(lambda: NoteSchema(only=("id", "title", "project")))
#     )


# class NoteSchema(ma.ModelSchema):
#     class Meta:
#         model = Note

#     content = ma.fields.List(ma.fields.Nested(BulletPointSchema))
