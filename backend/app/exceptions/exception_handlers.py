from collections.abc import Sequence
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.constants.message_constants import (
    FIELD_ERROR_SEPARATOR,
    VALIDATION_ERROR_MESSAGE,
    ErrorCode,
)
from app.exceptions.domain_exceptions import DomainError
from app.views.error_view import ErrorDetail, ErrorResponse

HTTP_STATUS_BY_ERROR_CODE: dict[ErrorCode, int] = {
    ErrorCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorCode.DUPLICATE_EMAIL: status.HTTP_409_CONFLICT,
    ErrorCode.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_CONTENT,
}
REQUEST_LOCATION_PREFIXES = {"body", "query", "path"}


def build_error_response(code: ErrorCode, message: str) -> JSONResponse:
    body = ErrorResponse(error=ErrorDetail(code=code, message=message))
    return JSONResponse(status_code=HTTP_STATUS_BY_ERROR_CODE[code], content=body.model_dump())


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


def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(DomainError, handle_domain_error)
    application.add_exception_handler(RequestValidationError, handle_request_validation_error)
