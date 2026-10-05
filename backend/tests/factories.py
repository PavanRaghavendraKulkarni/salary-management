from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.constants.employee_constants import Country, Currency, Department, JobTitle
from app.models.employee_model import Employee
from app.views.employee_view import EmployeeCreate, EmployeeUpdate

# Round USD rates for tests, so converted figures can be worked out by hand and do not
# change when the real rates in constants are updated.
TEST_USD_RATES: dict[Currency, Decimal] = {
    **{currency: Decimal("1") for currency in Currency},
    Currency.INR: Decimal("0.01"),
    Currency.EUR: Decimal("1.5"),
}
TEST_RATES_AS_OF = date(2026, 1, 1)

DEFAULT_EMPLOYEE_FIELDS: dict[str, Any] = {
    "full_name": "Asha Rao",
    "email": "asha.rao@acme.com",
    "job_title": JobTitle.SOFTWARE_ENGINEER.value,
    "department": Department.ENGINEERING.value,
    "country": Country.INDIA.value,
    "currency": Currency.INR.value,
    "annual_gross_salary": "1500000.00",
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
        "annual_gross_salary": Decimal(str(fields["annual_gross_salary"])),
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
    With TEST_USD_RATES (INR 0.01, EUR 1.5) these are 10,000, 15,000 and 7,000 USD for India
    and 90,000 and 75,000.30 USD for Germany.
    """
    india = {"country": Country.INDIA.value, "currency": Currency.INR.value}
    germany = {"country": Country.GERMANY.value, "currency": Currency.EUR.value}
    engineer = {
        "job_title": JobTitle.SOFTWARE_ENGINEER.value,
        "department": Department.ENGINEERING.value,
    }
    return [
        build_employee_record(
            email="in1@acme.com", annual_gross_salary="1000000.00", **india, **engineer
        ),
        build_employee_record(
            email="in2@acme.com", annual_gross_salary="1500000.00", **india, **engineer
        ),
        build_employee_record(
            email="in3@acme.com",
            annual_gross_salary="700000.00",
            job_title=JobTitle.SALES_REPRESENTATIVE.value,
            department=Department.SALES.value,
            **india,
        ),
        build_employee_record(
            email="de1@acme.com", annual_gross_salary="60000.00", **germany, **engineer
        ),
        build_employee_record(
            email="de2@acme.com",
            annual_gross_salary="50000.20",
            job_title=JobTitle.ACCOUNTANT.value,
            department=Department.FINANCE.value,
            **germany,
        ),
    ]
