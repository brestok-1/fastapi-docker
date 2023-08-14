import logging
import random
import requests

from celery.result import AsyncResult

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from . import users_router
from .schemas import UserBody
from .tasks import sample_task, task_process_notification

logger = logging.getLogger(__name__)
template = Jinja2Templates(directory='project/users/templates')


def api_call(email: str) -> None:
    if random.choice([0, 1]):
        raise Exception('Random processing error')  # used for testing failed call

    requests.post('https://httpbin.org/delay/5')


@users_router.get('/form/')
def form_example_get(request: Request):
    return template.TemplateResponse("form.html", {'request': request})


@users_router.post('/form/')
def form_example_post(user_body: UserBody):
    task: AsyncResult = sample_task.delay(user_body.email)
    return JSONResponse({'task_id': task.task_id})


@users_router.get('/task_status/')
def task_status(task_id: str, *args, **kwargs):
    task = AsyncResult(task_id)
    state = task.state

    if state == "FAILURE":
        error = str(task.result)
        response = {
            'state': state,
            'error': error,
        }
    else:
        response = {
            'state': state,
        }
    return JSONResponse(response)


@users_router.post('/webhook-test/')
def webhook_test():
    if not random.choice([1, 0]):
        raise Exception('Random processing error')
    # blocking process for 5 seconds
    requests.post('https://httpbin.org/delay/5')
    return 'pong'


@users_router.post('/webhook-test-async/')
def webhook_test_async():
    task = task_process_notification.delay()
    print(task.id)
    return "pong"