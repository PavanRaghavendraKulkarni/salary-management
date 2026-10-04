from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.constants.employee_constants import (
    FULL_NAME_MAX_LENGTH,
    FULL_NAME_MIN_LENGTH,
    MAX_ANNUAL_SALARY,
    MIN_ANNUAL_SALARY_EXCLUSIVE,
    SALARY_PRECISION,
    SALARY_SCALE,
    Country,
    Currency,
    Department,
    JobTitle,
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
    annual_salary: Decimal = Field(
        gt=MIN_ANNUAL_SALARY_EXCLUSIVE,
        le=MAX_ANNUAL_SALARY,
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
