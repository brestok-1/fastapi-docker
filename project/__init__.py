# from broadcaster import Broadcast
from fastapi import FastAPI
from project.config import setting

# broadcast = Broadcast(setting.WS_MESSAGE_QUEUE)


def create_app() -> FastAPI:
    app = FastAPI()

    from project.celery_utils import create_celery
    app.celery_app = create_celery()

    from project.users import users_router
    app.include_router(users_router)

    @app.get('/')
    async def root() -> dict[str, str]:
        return {'message': 'Hello world!'}

    return app
