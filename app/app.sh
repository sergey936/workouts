alembic upgrade head
uvicorn --factory application.api.main:init_api_v1 --reload --host 0.0.0.0 --port 8000