from app.constants.message_constants import (
    DUPLICATE_EMAIL_MESSAGE,
    EMPLOYEE_NOT_FOUND_MESSAGE,
    ErrorCode,
)


class DomainError(Exception):
    """Base for business-rule failures; carries a stable code so handlers stay generic."""

    code: ErrorCode

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class EmployeeNotFoundError(DomainError):
    code = ErrorCode.NOT_FOUND

    def __init__(self, employee_id: int) -> None:
        super().__init__(EMPLOYEE_NOT_FOUND_MESSAGE.format(employee_id=employee_id))


class DuplicateEmailError(DomainError):
    code = ErrorCode.DUPLICATE_EMAIL

    def __init__(self, email: str) -> None:
        super().__init__(DUPLICATE_EMAIL_MESSAGE.format(email=email))


class DomainValidationError(DomainError):
    code = ErrorCode.VALIDATION_ERROR
