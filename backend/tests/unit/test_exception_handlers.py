import asyncio
import json
from collections.abc import Callable, Coroutine
from typing import Any

import pytest
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.constants.message_constants import INTERNAL_ERROR_MESSAGE, ErrorCode
from app.exceptions.exception_handlers import (
    handle_domain_error,
    handle_http_exception,
    handle_request_validation_error,
)

ExceptionHandler = Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]


def build_request() -> Request:
    return Request(
        {
            "type": "http",
            "method": "GET",
            "scheme": "http",
            "server": ("testserver", 80),
            "path": "/",
            "query_string": b"",
            "headers": [],
        }
    )


@pytest.mark.parametrize(
    "handler",
    [handle_domain_error, handle_request_validation_error, handle_http_exception],
)
def test_handler_treats_an_error_of_another_type_as_an_internal_error(
    handler: ExceptionHandler,
) -> None:
    """An explicit check, unlike an assert, still holds under `python -O`."""
    response = asyncio.run(handler(build_request(), ValueError("unexpected type")))

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert json.loads(bytes(response.body)) == {
        "error": {"code": ErrorCode.INTERNAL_ERROR, "message": INTERNAL_ERROR_MESSAGE}
    }
