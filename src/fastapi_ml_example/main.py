import logging

from fastapi import FastAPI

from fastapi_ml_example.api import health
from fastapi_ml_example.core.logging import configure_logging

# no-op when started via `uvicorn ... --log-config=log_config.json`
configure_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    "Create and configure a FastAPI app instance."
    app = FastAPI(title="FastAPI ML Example")
    app.include_router(health.router)
    return app

app = create_app()
logger.info("Application created")


def main() -> None:
    "Запуск приложения в Uvicorn (`uv run fastapi-ml-example`)."
    import uvicorn  # noqa: PLC0415
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    main()
