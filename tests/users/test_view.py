from unittest import mock

import requests

from project.users import users_router
from project.users.models import User


def test_pytest_setup(client, db_session):
    response = client.get(users_router.url_path_for('form_example_get'))
    assert response.status_code == 200

    user = User(username='test', email='test@gmail.com')
    db_session.add(user)
    db_session.commit()
    assert user.id


def test_view_with_eager_mode(client, db_session, settings, monkeypatch):
    mock_request_post = mock.MagicMock()
    monkeypatch.setattr(requests, 'post', mock_request_post)

    monkeypatch.setattr(settings, 'CELERY_TASK_ALWAYS_EAGER', True, raising=False)

    username = 'testuser'
    email = 'test@mail.com'
    response = client.post(
        users_router.url_path_for('user_subscribe'),
        json={
            'email': email,
            'username': username
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'message': 'send task to Celery successfully'
    }

    mock_request_post.assert_called_with(
        'https://httpbin.org/delay/5',
        data={'email': email}
    )
