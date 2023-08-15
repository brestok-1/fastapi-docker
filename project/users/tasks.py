import random

import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger

logger = get_task_logger('__name__')


@shared_task
def divide(x: int, y: int) -> int | float:
    import time
    time.sleep(5)
    return x / y * 2


@shared_task
def sample_task(email: str):
    from project.users.views import api_call
    api_call(email)


@shared_task(bind=True)  # to use self.retry
def task_process_notification(self):
    try:
        if not random.choice([1, 0]):
            raise Exception('Random processing error')
        requests.post('https://httpbin.org/delay/5')
    except Exception as e:
        logger.error('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc=e, countdown=5)


@shared_task(name='task_scheduled_work')
def task_scheduled_work():
    logger.info('task_scheduled_work run')


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.ws.views import update_celery_task_status
    async_to_sync(update_celery_task_status)(task_id)

    from project.ws.views import update_celery_task_status_socketio
    update_celery_task_status_socketio(task_id)
