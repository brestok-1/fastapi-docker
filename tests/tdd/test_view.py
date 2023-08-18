import os.path
from unittest import mock

from project.tdd import tdd_router
from project.tdd.factories import MemberFactory
from project.tdd.models import Member
from project.tdd.tasks import generate_avatar_thumbnail


def test_post(client, db_session, settings, monkeypatch):
    member = MemberFactory.build()

    mock_generate_avatar_thumbnail_delay = mock.MagicMock(name='generate_thumbnail_avatar')
    monkeypatch.setattr(generate_avatar_thumbnail, 'delay', mock_generate_avatar_thumbnail_delay)

    avatar_full_path = os.path.join(settings.UPLOADS_DEFAULT_DEST, member.avatar)

    files = {'upload_file': open(avatar_full_path, 'rb')}

    data = {
        'username': member.username,
        'email': member.email
    }

    response = client.post(
        tdd_router.url_path_for('member_signup'),
        data=data,
        files=files
    )

    assert response.status_code == 200

    member = db_session.query(Member).filter_by(username=member.username).one_or_none()
    assert member
    assert member.avatar
    mock_generate_avatar_thumbnail_delay.assert_called_with(
        member.id
    )
