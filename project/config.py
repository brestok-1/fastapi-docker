import os
import pathlib
from functools import lru_cache
from kombu import Queue


def route_task(name: str, args, kwargs, options, task=None, **kw):
    if ':' in name:
        queue, _ = name.split(':')
        return {'queue': queue}
    return {'queue': 'default'}


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    DATABASE_URL = (f'postgresql://'
                    f'{os.getenv("POSTGRES_USER")}:'
                    f'{os.getenv("POSTGRES_PASSWORD")}@'
                    f'{os.getenv("POSTGRES_HOST")}:'
                    f'{os.getenv("POSTGRES_PORT")}/'
                    f'{os.getenv("POSTGRES_DB")}')
    DATABASE_CONNECT_DICT: dict = {}

    CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND: str = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_BEAT_SCHEDULE = {
        # 'task-scheduled-work': {
        #     'task': 'task_scheduled_work',
        #     'schedule': 5,
        # }
    }
    CELERY_TASK_DEFAULT_QUEUE = 'default'
    # Force all queues to be explicitly listed in `CELERY_TASK_QUEUES` to help prevent typos
    CELERY_TASK_CREATE_MISSING_QUEUES = False
    CELERY_TASK_QUEUES = (
        # need to define default queue here or exception would be raised
        Queue('default'),

        Queue('high_priority'),
        Queue('low_priority'),
    )

    CELERY_TASK_ROUTER = (route_task,)
    # {
    # 'project.users.tasks.*': {
    #     'queue': 'high_priority'
    # }
    # }

    WS_MESSAGE_QUEUE = os.getenv('WS_MESSAGE_QUEUE')


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    DATABASE_URL = "sqlite:///./test.db"
    DATABASE_CONNECT_DICT = {'check_same_thread': False}


@lru_cache()
def get_settings() -> DevelopmentConfig | ProductionConfig | TestConfig:
    config_cls_dict = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestConfig
    }
    config_name = os.getenv('FASTAPI_CONFIG', default='development')
    config_cls = config_cls_dict[config_name]
    return config_cls()


setting = get_settings()
