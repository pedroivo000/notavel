from flask import request
from database.models import BulletPoint, Note, BulletPointSchema

bullet_schema = BulletPointSchema()
bullets_schema = BulletPointSchema(many=True)


def get_bullets(note_id=None, type=None, project_id=None):
    bullets = BulletPoint.objects()

    return bullets_schema.dump(bullets), 200


def create_bullet():
    body = request.get_json()
    bullet = BulletPoint(**body).save()

    for note_id in body["parent_note_id"]:
        print(note_id)
        Note.objects(id=note_id).update_one(push__content=bullet)

    id = bullet.id

    return {"id": str(id)}, 200


def get_bullet(bullet_point_id):
    bullet = BulletPoint.objects.get(id=bullet_point_id)

    return bullet_schema.dump(bullet), 200


def delete_bullet(bullet_point_id):
    pass


def update_bullet():
    pass
