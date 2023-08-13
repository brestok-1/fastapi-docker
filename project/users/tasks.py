from celery import shared_task


@shared_task
def divide(x: int, y: int) -> int | float:
    import time
    time.sleep(5)
    return x / y * 2


@shared_task
def sample_task(email: str):
    pass