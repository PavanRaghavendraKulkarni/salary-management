import asyncio
import json

from fastapi import Request, status

from app.constants.message_constants import INTERNAL_ERROR_MESSAGE, ErrorCode
from app.exceptions.exception_handlers import handle_http_exception


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


def test_http_exception_handler_treats_any_other_error_as_an_internal_error() -> None:
    """An explicit check, unlike an assert, still holds under `python -O`."""
    response = asyncio.run(handle_http_exception(build_request(), ValueError("not HTTP")))

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert json.loads(response.body) == {
        "error": {"code": ErrorCode.INTERNAL_ERROR, "message": INTERNAL_ERROR_MESSAGE}
    }
