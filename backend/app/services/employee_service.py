from collections.abc import Callable
from datetime import date
from typing import Any

from app.constants.employee_constants import COUNTRY_CURRENCY
from app.constants.message_constants import (
    CURRENCY_MISMATCH_MESSAGE,
    FUTURE_HIRE_DATE_MESSAGE,
)
from app.exceptions.domain_exceptions import (
    DomainValidationError,
    DuplicateEmailError,
    EmployeeNotFoundError,
)
from app.models.employee_model import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.views.employee_view import (
    EmployeeCreate,
    EmployeeFields,
    EmployeeResponse,
    EmployeeUpdate,
)


class EmployeeService:
    """Business rules for employee records that span more than one field or need the database."""

    def __init__(
        self,
        repository: EmployeeRepository,
        today_provider: Callable[[], date] = date.today,
    ) -> None:
        self._repository = repository
        self._today_provider = today_provider

    def create_employee(self, payload: EmployeeCreate) -> EmployeeResponse:
        """Validate cross-field rules before saving, so bad data never reaches the database."""
        values = self._validated_values(payload)
        self._ensure_email_is_available(values["email"])
        return self._to_response(self._repository.create(values))

    def get_employee(self, employee_id: int) -> EmployeeResponse:
        return self._to_response(self._find_employee_or_raise(employee_id))

    def update_employee(self, employee_id: int, payload: EmployeeUpdate) -> EmployeeResponse:
        """Apply the same rules as create; the employee's own email does not count as taken."""
        employee = self._find_employee_or_raise(employee_id)
        values = self._validated_values(payload)
        self._ensure_email_is_available(values["email"], excluding_employee_id=employee_id)
        return self._to_response(self._repository.update(employee, values))

    def delete_employee(self, employee_id: int) -> None:
        self._repository.delete(self._find_employee_or_raise(employee_id))

    def _find_employee_or_raise(self, employee_id: int) -> Employee:
        employee = self._repository.get_by_id(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(employee_id)
        return employee

    def _validated_values(self, payload: EmployeeFields) -> dict[str, Any]:
        self._ensure_currency_matches_country(payload)
        self._ensure_hire_date_is_not_in_future(payload.hire_date)
        values = payload.model_dump()
        values["email"] = payload.email.lower()
        return values

    def _ensure_currency_matches_country(self, payload: EmployeeFields) -> None:
        if COUNTRY_CURRENCY[payload.country] != payload.currency:
            raise DomainValidationError(
                CURRENCY_MISMATCH_MESSAGE.format(
                    currency=payload.currency.value, country=payload.country.value
                )
            )

    def _ensure_hire_date_is_not_in_future(self, hire_date: date) -> None:
        if hire_date > self._today_provider():
            raise DomainValidationError(FUTURE_HIRE_DATE_MESSAGE)

    def _ensure_email_is_available(
        self, email: str, excluding_employee_id: int | None = None
    ) -> None:
        owner = self._repository.get_by_email(email)
        if owner is not None and owner.id != excluding_employee_id:
            raise DuplicateEmailError(email)

    @staticmethod
    def _to_response(employee: Employee) -> EmployeeResponse:
        return EmployeeResponse.model_validate(employee)
