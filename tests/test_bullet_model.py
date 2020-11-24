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

