import random

import celery
import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger

from project.database import db_context

logger = get_task_logger('__name__')


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception,)
    retry_backoff = 5
    retry_jitter = True
    retry_kwargs = {'max_retries': 7, 'countdown': 5}


@shared_task
def divide(x: int, y: int) -> int | float:
    import time
    time.sleep(5)
    return x / y * 2


@shared_task
def sample_task(email: str):
    from project.users.views import api_call
    api_call(email)


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification(self):
    if not random.choice([1, 0]):
        raise Exception
    requests.post('https://httpbin.org/delay/5')


@shared_task(name='task_scheduled_work')
def task_scheduled_work():
    logger.info('task_scheduled_work run')


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.ws.views import update_celery_task_status
    async_to_sync(update_celery_task_status)(task_id)

    from project.ws.views import update_celery_task_status_socketio
    update_celery_task_status_socketio(task_id)


@shared_task(name="default:dynamic_example_one")
def dynamic_example_one():
    logger.info("Example One")


@shared_task(name="low_priority:dynamic_example_two")
def dynamic_example_two():
    logger.info("Example Two")


@shared_task(name="high_priority:dynamic_example_three")
def dynamic_example_three():
    logger.info("Example Three")


