from flask import request
from database.models import BulletPoint, Note, BulletPointSchema

bullet_schema = BulletPointSchema()
bullets_schema = BulletPointSchema(many=True)


def get_bullets(note_id=None, type=None, project_id=None):
    bullets = BulletPoint.objects()
    print([i for i in bullets])

    return bullets_schema.dump(bullets), 200


def create_bullet():
    body = request.get_json()
    bullet = BulletPoint(**body).save()
    note = bullet.parent_note_id
    Note.objects(id=note.id).update_one(push__content=bullet)
    # print(note_schema.dump(note))
    # note = Note.objects.get(id=bullet.parent_note_id)
    # note.update_one(push__content=bullet)
    # note.save()
    id = bullet.id

    return {"id": str(id)}, 200


def get_bullet(bullet_id):
    pass


def delete_bullet(bullet_id):
    pass


def update_bullet():
    pass
