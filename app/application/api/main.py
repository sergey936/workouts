from application.api.user.handlers import router as UserRouter
from fastapi import FastAPI
from logic.init import get_container
from punq import Container


def init_api_v1() -> FastAPI:
    app = FastAPI(
        title='Workouts',
        description='App where you can post your training schemas for other people.',
        version='1.0.0',
        debug=True,
    )
    app.include_router(router=UserRouter, tags=['users'])
    app.dependency_overrides[Container] = get_container

    return app
