from unittest import mock

import pytest
from celery.exceptions import Retry

import requests

from project.users.factories import UserFactory
from project.users.tasks import task_add_subscribe


def test_post_successed(db_session, monkeypatch):
    user = UserFactory.create()

    mock_request_post = mock.MagicMock()
    monkeypatch.setattr(requests, 'post', mock_request_post)

    task_add_subscribe(user.id)

    mock_request_post.assert_called_with(
        "https://httpbin.org/delay/5",
        data={'email': user.email}
    )


def test_exception(db_session, monkeypatch):
    user = UserFactory.build()

    mock_request_post = mock.MagicMock()
    monkeypatch.setattr(requests, 'post', mock_request_post)

    mock_task_add_subscribe_retry = mock.MagicMock()
    monkeypatch.setattr(task_add_subscribe, 'retry', mock_task_add_subscribe_retry)

    mock_task_add_subscribe_retry.side_effect = Retry()
    mock_request_post.side_effect = Exception()

    with pytest.raises(Retry):
        task_add_subscribe(user.id)
