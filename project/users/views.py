import logging
import random
from string import ascii_lowercase

import requests

from celery.result import AsyncResult

from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from . import users_router
from .models import User
from .schemas import UserBody
from .tasks import sample_task, task_process_notification, task_send_welcome_email, task_add_subscribe
from ..database import get_db_session

logger = logging.getLogger(__name__)
template = Jinja2Templates(directory='project/users/templates')


def random_username():
    username = "".join([random.choice(ascii_lowercase) for i in range(5)])
    return username


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


@users_router.get('/task-status/')
def task_status(task_id: str):
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


@users_router.get('/form-ws/')
def form_ws_example(request: Request):
    return template.TemplateResponse("form_ws.html", {'request': request})


@users_router.get('/form-socketio/')
def form_socketio_example(request: Request):
    return template.TemplateResponse('form_socketio.html', {'request': request})


@users_router.get('/transaction-celery/')
def transaction_celery(session: Session = Depends(get_db_session)):
    try:
        username = random_username()
        user = User(
            username=username,
            email=f'{username}@test.com'
        )
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    logger.info(f'user {user.id} {user.username} is persisted now')
    task_send_welcome_email.delay(user.id)
    return {'message': 'done'}


@users_router.post("/user_subscribe/")
def user_subscribe(user_body: UserBody, session: Session = Depends(get_db_session)):
    try:
        user = session.query(User).filter_by(username=user_body.username).first()
        if user:
            user_id = user.id
        else:
            user = User(
                username=user_body.username,
                email=user_body.email,
            )
            session.add(user)
            session.commit()
            user_id = user.id
    except Exception as e:
        session.rollback()
        raise
    task_add_subscribe.delay(user_id)
    return {"message": "send task to Celery successfully"}


@users_router.post('/user_subscribe/')
def user_subscribe(user_body: UserBody, session: Session = Depends(get_db_session)):
    try:
        user = session.query(User).filter_by(username=user_body.username).first()
        if user:
            user_id = user.id
        else:
            user = User(
                username=user_body.username,
                email=user_body.email
            )
            session.add(user)
            session.commit()
            user_id = user.id
    except Exception as e:
        session.rollback()
        raise
    task_add_subscribe.delay(user_id)
    return {'message': 'send task to Celery successfully'}
