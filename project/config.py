import os
import pathlib
from functools import lru_cache


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

    WS_MESSAGE_QUEUE = os.getenv('WS_MESSAGE_QUEUE')


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass


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
