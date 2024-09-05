from application.api.auth.handlers import router as AuthRouter
from application.api.user.handlers import router as UserRouter
from application.api.workout.handlers import router as WokroutRouter
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
    app.dependency_overrides[Container] = get_container

    app.include_router(router=UserRouter, prefix='/user', tags=['Users'])
    app.include_router(router=AuthRouter, prefix='/auth', tags=['Auth'])
    app.include_router(router=WokroutRouter, prefix='/Workout', tags=['Workout'])

    return app
