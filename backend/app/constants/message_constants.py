from enum import StrEnum


class ErrorCode(StrEnum):
    NOT_FOUND = "NOT_FOUND"
    DUPLICATE_EMAIL = "DUPLICATE_EMAIL"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    HTTP_ERROR = "HTTP_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


EMPLOYEE_NOT_FOUND_MESSAGE = "Employee with id {employee_id} was not found."
DUPLICATE_EMAIL_MESSAGE = "An employee with email {email} already exists."
VALIDATION_ERROR_MESSAGE = "The request contains invalid data."
CURRENCY_MISMATCH_MESSAGE = "Currency {currency} does not match country {country}."
ROUTE_NOT_FOUND_MESSAGE = "No route matches /{path}."
FUTURE_HIRE_DATE_MESSAGE = "Hire date cannot be in the future."
FIELD_ERROR_SEPARATOR = "; "
INTERNAL_ERROR_MESSAGE = "Something went wrong on our side. Please try again later."
UNEXPECTED_ERROR_LOG_MESSAGE = "Unexpected error while handling %s %s"
