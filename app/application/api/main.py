from fastapi import FastAPI


def init_api_v1() -> FastAPI:
    app = FastAPI(
        title='Workouts',
        description='App where you can post your training schemas for other people.',
        version='1.0.0',
        debug=True
    )

    return app
