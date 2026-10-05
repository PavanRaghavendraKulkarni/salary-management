import logging
from collections.abc import Sequence
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.constants.message_constants import (
    FIELD_ERROR_SEPARATOR,
    INTERNAL_ERROR_MESSAGE,
    UNEXPECTED_ERROR_LOG_MESSAGE,
    VALIDATION_ERROR_MESSAGE,
    ErrorCode,
)
from app.exceptions.domain_exceptions import DomainError
from app.views.error_view import ErrorDetail, ErrorResponse

HTTP_STATUS_BY_ERROR_CODE: dict[ErrorCode, int] = {
    ErrorCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorCode.DUPLICATE_EMAIL: status.HTTP_409_CONFLICT,
    ErrorCode.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
}
REQUEST_LOCATION_PREFIXES = {"body", "query", "path"}

logger = logging.getLogger(__name__)


def build_error_response(
    code: ErrorCode, message: str, status_code: int | None = None
) -> JSONResponse:
    body = ErrorResponse(error=ErrorDetail(code=code, message=message))
    return JSONResponse(
        status_code=status_code or HTTP_STATUS_BY_ERROR_CODE[code], content=body.model_dump()
    )


def describe_validation_errors(errors: Sequence[Any]) -> str:
    """Turn Pydantic errors into one readable sentence, e.g. 'full_name: String too short'."""
    descriptions = []
    for error in errors:
        location = [str(part) for part in error["loc"] if part not in REQUEST_LOCATION_PREFIXES]
        field = ".".join(location)
        descriptions.append(f"{field}: {error['msg']}" if field else str(error["msg"]))
    return FIELD_ERROR_SEPARATOR.join(descriptions) or VALIDATION_ERROR_MESSAGE


async def handle_domain_error(_: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, DomainError)
    return build_error_response(error.code, error.message)


async def handle_request_validation_error(_: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, RequestValidationError)
    return build_error_response(
        ErrorCode.VALIDATION_ERROR, describe_validation_errors(error.errors())
    )


async def handle_http_exception(request: Request, error: Exception) -> JSONResponse:
    """Framework errors (unknown route, wrong method) use the same shape as domain errors."""
    if not isinstance(error, StarletteHTTPException):
        return await handle_unexpected_error(request, error)
    code = (
        ErrorCode.NOT_FOUND
        if error.status_code == status.HTTP_404_NOT_FOUND
        else ErrorCode.HTTP_ERROR
    )
    return build_error_response(code, str(error.detail), error.status_code)


async def handle_unexpected_error(request: Request, error: Exception) -> JSONResponse:
    """Log the full traceback for us, but give the client a generic message so internals
    such as SQL or file paths never leak into a response."""
    logger.error(UNEXPECTED_ERROR_LOG_MESSAGE, request.method, request.url.path, exc_info=error)
    return build_error_response(ErrorCode.INTERNAL_ERROR, INTERNAL_ERROR_MESSAGE)


def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(DomainError, handle_domain_error)
    application.add_exception_handler(RequestValidationError, handle_request_validation_error)
    application.add_exception_handler(StarletteHTTPException, handle_http_exception)
    application.add_exception_handler(Exception, handle_unexpected_error)
