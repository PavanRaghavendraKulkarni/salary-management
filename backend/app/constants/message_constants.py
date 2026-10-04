from enum import StrEnum


class ErrorCode(StrEnum):
    NOT_FOUND = "NOT_FOUND"
    DUPLICATE_EMAIL = "DUPLICATE_EMAIL"
    VALIDATION_ERROR = "VALIDATION_ERROR"


EMPLOYEE_NOT_FOUND_MESSAGE = "Employee with id {employee_id} was not found."
DUPLICATE_EMAIL_MESSAGE = "An employee with email {email} already exists."
VALIDATION_ERROR_MESSAGE = "The request contains invalid data."
CURRENCY_MISMATCH_MESSAGE = "Currency {currency} does not match country {country}."
FUTURE_HIRE_DATE_MESSAGE = "Hire date cannot be in the future."
