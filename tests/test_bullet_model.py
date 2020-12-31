import json
from notavel.models import Bullet


def test_create_bullet(database, test_note):
    record = {"content": "test", "order": 1, "type": "bullet", "note_id": 1}

    bullet = Bullet(**record)
    database.session.add(bullet)
    database.session.commit()

    # bullet = Bullet.query.first()
    assert Bullet.query.one()
    # assert bullet.content == content


def test_delete_bullet(database, test_bullet):

    bullet = Bullet.query.first()
    database.session.delete(bullet)
    database.session.commit()

    assert not Bullet.query.first()
