from datetime import datetime
from notavel import db, ma


class BaseDocument(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return str(self.__dict__)


class BaseBullet(BaseDocument):
    __abstract__ = True
    content = db.Column(db.String)


class Bullet(BaseBullet):
    __tablename__ = "bullet"
    id = db.Column(db.Integer, primary_key=True)


class Task(BaseBullet):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    due_at = db.Column(db.DateTime)
    priority = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)


class BulletSchema(ma.ModelSchema):
    class Meta:
        model = Bullet
        sqla_session = db.session


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = Task
        sqla_session = db.session


class Note(BaseDocument):
    id = db.Column(db.Integer, primary_key=True)