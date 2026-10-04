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


def build_insight_dataset() -> list[dict[str, Any]]:
    """Five employees whose statistics are easy to compute by hand.

    India: 1,000,000 and 1,500,000 (Software Engineer, Engineering) and 700,000 (Sales
    Representative, Sales); average 1,066,666.666... which must round to 1,066,666.67.
    Germany: 60,000.00 (Software Engineer, Engineering) and 50,000.20 (Accountant, Finance).
    """
    india = {"country": Country.INDIA.value, "currency": Currency.INR.value}
    germany = {"country": Country.GERMANY.value, "currency": Currency.EUR.value}
    engineer = {
        "job_title": JobTitle.SOFTWARE_ENGINEER.value,
        "department": Department.ENGINEERING.value,
    }
    return [
        build_employee_record(
            email="in1@acme.com", annual_salary="1000000.00", **india, **engineer
        ),
        build_employee_record(
            email="in2@acme.com", annual_salary="1500000.00", **india, **engineer
        ),
        build_employee_record(
            email="in3@acme.com",
            annual_salary="700000.00",
            job_title=JobTitle.SALES_REPRESENTATIVE.value,
            department=Department.SALES.value,
            **india,
        ),
        build_employee_record(
            email="de1@acme.com", annual_salary="60000.00", **germany, **engineer
        ),
        build_employee_record(
            email="de2@acme.com",
            annual_salary="50000.20",
            job_title=JobTitle.ACCOUNTANT.value,
            department=Department.FINANCE.value,
            **germany,
        ),
    ]
