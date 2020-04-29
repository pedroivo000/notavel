from notavel import db
from flask import request
from flask.views import MethodView
from notavel.models import Bullet, BulletSchema
from notavel.models import Task, TaskSchema

bullet_schema = BulletSchema()
bullets_schema = BulletSchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class BaseView(MethodView):
    def search(self, **kwargs):
        return "[{hello}]", 200

    def get(self, id):
        pass

    def post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class BulletsView(BaseView):
    def search(self, **kwargs):
        bullets = Bullet.query.all()
        return bullets_schema.dump(bullets), 200

    def post(self):
        body = request.json
        new_bullet = bullet_schema.load(body, session=db.session)
        db.session.add(new_bullet)
        db.session.commit()

        data = bullet_schema.dump(new_bullet)
        return data, 200


class TasksView(BaseView):
    def search(self, **kwargs):
        bullets = Task.query.all()
        return tasks_schema.dump(bullets), 200

    def post(self):
        body = request.json

        # TODO: figure out why marshamallow returns missing 'id' parameter for .load()
        new_task = Task(**body)

        db.session.add(new_task)
        db.session.commit()

        data = task_schema.dump(new_task)
        return data, 200


class ProjectsView(BaseView):
    pass


class NotesView(BaseView):
    pass


def search(**kwargs):
    return "{hello}", 200
