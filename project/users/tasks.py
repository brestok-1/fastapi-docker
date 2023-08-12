from celery import shared_task


@shared_task
def divide(x: int, y: int) -> int | float:
    import time
    time.sleep(5)
    return x / y
