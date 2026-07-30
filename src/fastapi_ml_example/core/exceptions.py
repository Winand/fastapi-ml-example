import logging
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from fastapi_ml_example.schemas.predict import EMPTY_RESPONSE

JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

logger = logging.getLogger(__name__)


class UnhandledError(Exception):
    "Error raised by `ExceptionCatchingRoute` on unhandled app exception."

    def __init__(self, request_body: JSON) -> None:
        "request_json - parsed request object."
        self.body = request_body
        super().__init__()


async def internal_error_handler(_: Request, exc: UnhandledError) -> JSONResponse:
    "Log unhandled errors and return default response."
    logger.error(exc.body, exc_info=exc.__cause__)
    return JSONResponse(EMPTY_RESPONSE.model_dump(),
                        status.HTTP_500_INTERNAL_SERVER_ERROR)


async def validation_exception_handler(
    _: Request, exc: RequestValidationError,
) -> JSONResponse:
    "Log validation errors and return default response."
    logger.error(exc.body, exc_info=exc)
    return JSONResponse(EMPTY_RESPONSE.model_dump(),
                        status.HTTP_422_UNPROCESSABLE_ENTITY)


# Handlers should be registered in app like this:
# app = FastAPI(..., exception_handlers=exception_handlers)
AsyncExceptionHandler = Callable[[Request, Any], Coroutine[Any, Any, Response]]
exception_handlers: dict[int | type[Exception], AsyncExceptionHandler] = {
    RequestValidationError: validation_exception_handler,
    UnhandledError: internal_error_handler,
}
