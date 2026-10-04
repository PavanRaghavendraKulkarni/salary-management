from pydantic import BaseModel

from app.constants.message_constants import ErrorCode


class ErrorDetail(BaseModel):
    code: ErrorCode
    message: str


class ErrorResponse(BaseModel):
    """The single error shape every failed request returns."""

    error: ErrorDetail
