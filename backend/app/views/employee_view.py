from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.constants.employee_constants import (
    DEFAULT_EMPLOYEE_SORT_FIELD,
    FULL_NAME_MAX_LENGTH,
    FULL_NAME_MIN_LENGTH,
    MAX_ANNUAL_GROSS_SALARY,
    MIN_ANNUAL_GROSS_SALARY_EXCLUSIVE,
    SALARY_PRECISION,
    SALARY_SCALE,
    SEARCH_MAX_LENGTH,
    Country,
    Currency,
    Department,
    EmployeeSortField,
    JobTitle,
)
from app.constants.pagination_constants import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    DEFAULT_SORT_ORDER,
    MAX_PAGE_SIZE,
    MIN_PAGE,
    MIN_PAGE_SIZE,
    SortOrder,
)


class EmployeeFields(BaseModel):
    """Editable employee fields with field-level validation shared by create and update."""

    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str = Field(min_length=FULL_NAME_MIN_LENGTH, max_length=FULL_NAME_MAX_LENGTH)
    email: EmailStr
    job_title: JobTitle
    department: Department
    country: Country
    currency: Currency
    annual_gross_salary: Decimal = Field(
        gt=MIN_ANNUAL_GROSS_SALARY_EXCLUSIVE,
        le=MAX_ANNUAL_GROSS_SALARY,
        max_digits=SALARY_PRECISION,
        decimal_places=SALARY_SCALE,
    )
    hire_date: date


class EmployeeCreate(EmployeeFields):
    """Request body for creating an employee."""


class EmployeeUpdate(EmployeeFields):
    """Request body for replacing an employee's editable fields (PUT semantics)."""


class EmployeeResponse(EmployeeFields):
    """An employee as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class EmployeeListQuery(BaseModel):
    """Query parameters for listing employees; bounds stop clients requesting every row."""

    search: str | None = Field(default=None, max_length=SEARCH_MAX_LENGTH)
    country: Country | None = None
    department: Department | None = None
    job_title: JobTitle | None = None
    page: int = Field(default=DEFAULT_PAGE, ge=MIN_PAGE)
    page_size: int = Field(default=DEFAULT_PAGE_SIZE, ge=MIN_PAGE_SIZE, le=MAX_PAGE_SIZE)
    sort_by: EmployeeSortField = DEFAULT_EMPLOYEE_SORT_FIELD
    sort_order: SortOrder = DEFAULT_SORT_ORDER
