from datetime import datetime
import enum
from marshmallow_enum import EnumField

from notavel import db, ma


class BaseDocument(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    archived = db.Column(db.Boolean, default=False)

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
    order = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(BulletTypeEnum), nullable=False)
    due_at = db.Column(db.DateTime)
    priority = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("bullet.id"))

    # parent = db.relationship("Bullet", remote_side=[id])


class BulletSchema(ma.ModelSchema):
    type = EnumField(BulletTypeEnum, by_value=True)

    class Meta:
        model = Bullet
        sqla_session = db.session
        include_fk = True


class Note(BaseDocument):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.relationship(
        "Bullet", backref="note", lazy=True, order_by="Bullet.order"
    )
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))


# TODO: find generic way to archive child if parent is archived
# archive bullets if note is archived
@db.event.listens_for(Note, "after_update")
def propgate_note_archive(mapper, connection, target):

    if db.inspect(target).attrs.archived.history.has_changes():
        stmt = (
            db.update(Bullet)
            .values(archived=target.archived)
            .where(Bullet.note_id == target.id)
        )
        connection.execute(stmt)
class NoteSchema(ma.ModelSchema):
    content = ma.Nested(BulletSchema, many=True)

    class Meta:
        model = Note
        sqla_session = db.session
        include_fk = True


class Project(BaseDocument):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    notes = db.relationship(
        "Note", backref="project", lazy=True, order_by="Note.updated_at"
    )
# Archive all notes in a project if project is archived
@db.event.listens_for(Project, "after_update")
def propgate_project_archive(mapper, connection, target):

    if db.inspect(target).attrs.archived.history.has_changes():
        stmt = (
            db.update(Note)
            .values(archived=target.archived)
            .where(Note.project_id == target.id)
        )
        connection.execute(stmt)


class ProjectSchema(ma.ModelSchema):
    notes = ma.Nested(NoteSchema, many=True, exclude=("content",))

    class Meta:
        model = Project
        sqla_session = db.session
        include_fk = True
