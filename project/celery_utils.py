import functools

from celery import current_app as current_celery_app, Celery, shared_task
from celery.result import AsyncResult
from project.config import setting
from celery.utils.time import get_exponential_backoff_interval


def create_celery() -> Celery:
    celery_app = current_celery_app
    celery_app.config_from_object(setting, namespace='CELERY')
    return celery_app


def get_task_info(task_id):
    """
    return task info according to the task_id
    """
    task = AsyncResult(task_id)
    state = task.state

    if state == "FAILURE":
        error = str(task.result)
        response = {
            "state": task.state,
            "error": error,
        }
    else:
        response = {
            "state": task.state,
        }
    return response


class custom_celery_task:
    EXCEPTION_BLOCK_LIST = (
        IndexError,
        KeyError,
        TypeError,
        UnicodeDecodeError,
        ValueError,
    )

    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except self.EXCEPTION_BLOCK_LIST:
                raise
            except Exception as e:
                countdown = self._get_retry_countdown(task_func)
                raise task_func.retry(exc=e, countdown=countdown)

        task_func = shared_task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func

    def _get_retry_countdown(self, task_func):
        retry_backoff = int(self.task_kwargs.get('retry_backoff', True))
        retry_backoff_max = int(self.task_kwargs.get('retry_backoff', 600))
        retry_jitter = self.task_kwargs.get('retry_jitter', True)

        countdown = get_exponential_backoff_interval(
            factor=retry_backoff,
            retries=task_func.request.retries,
            maximum=retry_backoff_max,
            full_jitter=retry_jitter
        )
        return countdown
