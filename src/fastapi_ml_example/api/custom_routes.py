"""
Custom route class which raises `UnhandledError` on any unhandled exception.

`UnhandledError` object includes parsed JSON request body in `.body` field.

https://fastapi.tiangolo.com/how-to/custom-request-and-route/?h=apiroute#accessing-the-request-body-in-an-exception-handler
https://stackoverflow.com/questions/69670125/how-to-log-raw-http-request-response-in-python-fastapi
"""

from collections.abc import Callable, Coroutine
from typing import Any, override

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

from fastapi_ml_example.core.exceptions import UnhandledError


class CatchExceptionsWithBodyRoute(APIRoute):
    """Custom route class which raises `UnhandledError` on any unhandled exception.

    `UnhandledError` includes request body in `.body` field and can be catched
    using @app.exception_handler(UnhandledError) as any other exception.

    `RequestValidationError` exceptions are re-raised without modification.
    """
    @override
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError:
                raise
            except Exception as exc:
                request_body = await request.json()
                raise UnhandledError(request_body) from exc
        return custom_route_handler
