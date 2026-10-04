from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.constants.employee_constants import Country, Currency, Department, JobTitle
from app.models.employee_model import Employee
from app.views.employee_view import EmployeeCreate, EmployeeUpdate

DEFAULT_EMPLOYEE_FIELDS: dict[str, Any] = {
    "full_name": "Asha Rao",
    "email": "asha.rao@acme.com",
    "job_title": JobTitle.SOFTWARE_ENGINEER.value,
    "department": Department.ENGINEERING.value,
    "country": Country.INDIA.value,
    "currency": Currency.INR.value,
    "annual_salary": "1500000.00",
    "hire_date": "2022-04-01",
}


def build_employee_payload(**overrides: Any) -> dict[str, Any]:
    """JSON-ready request body for the employee endpoints."""
    return {**DEFAULT_EMPLOYEE_FIELDS, **overrides}


def build_employee_create(**overrides: Any) -> EmployeeCreate:
    """Validated create schema for calling the service directly."""
    return EmployeeCreate.model_validate(build_employee_payload(**overrides))


def build_employee_update(**overrides: Any) -> EmployeeUpdate:
    """Validated update schema for calling the service directly."""
    return EmployeeUpdate.model_validate(build_employee_payload(**overrides))


def build_employee_record(**overrides: Any) -> dict[str, Any]:
    """Typed column values for inserting rows straight into the database."""
    fields = build_employee_payload(**overrides)
    return {
        **fields,
        "annual_salary": Decimal(str(fields["annual_salary"])),
        "hire_date": date.fromisoformat(str(fields["hire_date"])),
    }


def insert_employees(session: Session, records: list[dict[str, Any]]) -> list[Employee]:
    """Insert hand-built rows directly, bypassing the API, to arrange test data quickly."""
    employees = [Employee(**record) for record in records]
    session.add_all(employees)
    session.commit()
    return employees


def build_numbered_records(count: int, **overrides: Any) -> list[dict[str, Any]]:
    """Distinct, predictable rows: 'Employee 01', 'employee01@acme.com', and so on."""
    return [
        build_employee_record(
            full_name=f"Employee {number:02d}",
            email=f"employee{number:02d}@acme.com",
            **overrides,
        )
        for number in range(1, count + 1)
    ]
