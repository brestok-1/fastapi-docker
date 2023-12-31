from unittest import mock

import pytest

from project.celery_utils import custom_celery_task
from project.database import db_context
from project.users.factories import UserFactory
from project.users.models import User


@custom_celery_task()
def successful_task(user_id):
    with db_context() as session:
        user = session.get(User, user_id)
        user.username = 'test'
        session.commit()


@custom_celery_task()
def throwing_no_retry_task():
    raise TypeError


@custom_celery_task()
def throwing_retry_task():
    raise Exception


def test_custom_celery_task(db_session, settings, monkeypatch):
    user = UserFactory.create()

    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)
    successful_task.delay(user.id)

    assert db_session.get(User, user.id).username == 'test'


def test_throwing_no_retry_task(settings, monkeypatch):
    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)
    monkeypatch.setattr(settings, "CELERY_TASK_EAGER_PROPAGATES", True, raising=False)

    with mock.patch('celery.app.task.Task.retry') as mock_retry:
        with pytest.raises(TypeError):
            throwing_no_retry_task.delay()

        mock_retry.assert_not_called()


def test_throwing_retry_task(settings, monkeypatch):
    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)
    monkeypatch.setattr(settings, "CELERY_TASK_EAGER_PROPAGATES", True, raising=False)
    with mock.patch("celery.app.task.Task.retry") as mock_retry:
        with pytest.raises(Exception):
            throwing_retry_task.delay()
        mock_retry.assert_called()
        assert "countdown" in mock_retry.call_args[1]
