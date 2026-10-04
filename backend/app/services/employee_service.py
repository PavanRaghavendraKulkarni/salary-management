from collections.abc import Callable
from datetime import date
from typing import Any

from app.constants.employee_constants import COUNTRY_CURRENCY, Department, JobTitle
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
    EmployeeListQuery,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.views.meta_view import CountryOption, FilterOptionsResponse, ReferenceDataResponse
from app.views.pagination_view import PaginatedResponse


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

    def list_employees(self, query: EmployeeListQuery) -> PaginatedResponse[EmployeeResponse]:
        """Translate page numbers into an offset; the repository does the heavy lifting in SQL."""
        employees, total = self._repository.find_page(
            search=query.search,
            country=query.country,
            department=query.department,
            job_title=query.job_title,
            sort_by=query.sort_by,
            sort_order=query.sort_order,
            offset=(query.page - 1) * query.page_size,
            limit=query.page_size,
        )
        return PaginatedResponse[EmployeeResponse](
            items=[self._to_response(employee) for employee in employees],
            total=total,
            page=query.page,
            page_size=query.page_size,
        )

    def get_filter_options(self) -> FilterOptionsResponse:
        """Offer only values present in the data, so a filter never leads to an empty table."""
        return FilterOptionsResponse(
            countries=self._repository.distinct_countries(),
            departments=self._repository.distinct_departments(),
            job_titles=self._repository.distinct_job_titles(),
        )

    @staticmethod
    def get_reference_data() -> ReferenceDataResponse:
        """Expose backend constants so the UI never keeps its own copy of the allowed values."""
        return ReferenceDataResponse(
            countries=[
                CountryOption(name=country, currency=currency)
                for country, currency in COUNTRY_CURRENCY.items()
            ],
            departments=list(Department),
            job_titles=list(JobTitle),
        )

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
