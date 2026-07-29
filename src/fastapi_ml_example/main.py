from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_ml_example.api import health, predict
from fastapi_ml_example.core.exceptions import exception_handlers
from fastapi_ml_example.core.logging import configure_logging
from fastapi_ml_example.ml.model import load_model

# no-op when started via `uvicorn ... --log-config=log_config.json`
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    "Resource management."
    app.state.model = load_model()
    yield


def create_app() -> FastAPI:
    "Create and configure a FastAPI app instance."
    app = FastAPI(
        title="FastAPI ML Example", lifespan=lifespan,
        exception_handlers=exception_handlers,
    )
    app.include_router(health.router)
    app.include_router(predict.router)
    return app

app = create_app()


def main() -> None:
    "Запуск приложения в Uvicorn (`uv run fastapi-ml-example`)."
    import uvicorn  # noqa: PLC0415
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    main()
