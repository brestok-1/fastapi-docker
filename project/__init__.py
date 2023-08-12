from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get('/')
    async def root() -> dict[str:str]:
        return {'message': 'Hello world!'}

    return app
