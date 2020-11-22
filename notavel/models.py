from datetime import datetime
import enum

from sqlalchemy.orm import backref
from notavel import db, ma
from marshmallow_enum import EnumField


class BaseDocument(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return str(self.__dict__)


class BulletTypeEnum(enum.Enum):
    bullet = "bullet"
    task = "task"
    idea = "idea"


class Bullet(BaseDocument):
    __tablename__ = "bullet"
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)
    content = db.Column(db.String)
    type = db.Column(db.Enum(BulletTypeEnum), nullable=False)
    due_at = db.Column(db.DateTime)
    priority = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)


class BulletSchema(ma.ModelSchema):
    type = EnumField(BulletTypeEnum, by_value=True)

    class Meta:
        model = Bullet
        sqla_session = db.session
        include_fk = True


class Note(BaseDocument):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.relationship("Bullet", backref="note", lazy=True)


class NoteSchema(ma.ModelSchema):
    content = ma.Nested(BulletSchema, many=True)

    class Meta:
        model = Note
        sqla_session = db.session
