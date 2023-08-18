import os.path

from PIL import Image

from celery import shared_task

from project import setting
from project.database import db_context
from project.tdd.models import Member


@shared_task(name='generate_avatar_thumbnail')
def generate_avatar_thumbnail(member_id):
    with db_context() as session:
        member = session.get(Member, member_id)

        full_path = os.path.join(
            setting.UPLOADS_DEFAULT_DEST,
            member.avatar
        )

        thumbnail_path = f'{member.id}-avatar-thumbnail.jpg'
        thumbnail_full_path = os.path.join(setting.UPLOADS_DEFAULT_DEST, thumbnail_path)

        im = Image.open(full_path)
        size = (100, 100)
        im.thumbnail(size)
        im.save(thumbnail_full_path, 'JPEG')

        member.avatar_thumbnail = thumbnail_path
        session.add(member)
        session.commit()
