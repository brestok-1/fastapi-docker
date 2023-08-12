import os

from celery import Celery
from project import create_app

app = create_app()

celery = Celery(
    __name__,
    broker=os.getenv('CELERY_BROKER_URL'),
    backend=os.getenv('CELERY_RESULT_BACKEND')
)


@celery.task
def divide(x: int, y: int) -> float | int:
    import time
    time.sleep(5)
    return x / y
