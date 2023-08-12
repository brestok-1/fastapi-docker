import os

from celery import Celery
from fastapi import FastAPI

app = FastAPI()

celery = Celery(
    __name__,
    broker=os.getenv('CELERY_BROKER_URL'),
    backend=os.getenv('CELERY_RESULT_BACKEND')
)


@app.get('/')
async def root() -> dict[str:str]:
    return {'message': "Hello world!"}


@celery.task
def divide(x: int, y: int) -> float | int:
    import time
    time.sleep(5)
    return x / y


