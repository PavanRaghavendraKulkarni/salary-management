from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    ColumnElement,
    Numeric,
    Select,
    case,
    delete,
    func,
    insert,
    or_,
    select,
    type_coerce,
)
from sqlalchemy.orm import InstrumentedAttribute, Session

from app.constants.employee_constants import (
    SALARY_PRECISION,
    SALARY_SCALE,
    Currency,
    EmployeeSortField,
)
from app.constants.pagination_constants import SortOrder
from app.models.employee_model import Employee

UsdRates = Mapping[Currency, Decimal]

SORTABLE_COLUMNS: dict[EmployeeSortField, InstrumentedAttribute[Any]] = {
    EmployeeSortField.FULL_NAME: Employee.full_name,
    EmployeeSortField.EMAIL: Employee.email,
    EmployeeSortField.JOB_TITLE: Employee.job_title,
    EmployeeSortField.DEPARTMENT: Employee.department,
    EmployeeSortField.COUNTRY: Employee.country,
    EmployeeSortField.ANNUAL_GROSS_SALARY: Employee.annual_gross_salary,
    EmployeeSortField.HIRE_DATE: Employee.hire_date,
}


@dataclass(frozen=True)
class UsdAggregate:
    """Unrounded USD statistics, so the service rounds only once, at the final output."""

    min_salary: Decimal
    max_salary: Decimal
    average_salary: Decimal


@dataclass(frozen=True)
class SalaryAggregate:
    """Salary statistics for one group (a country, job title or department)."""

    group: str
    currency: str
    headcount: int
    min_salary: Decimal
    max_salary: Decimal
    average_salary: Decimal
    usd: UsdAggregate


@dataclass(frozen=True)
class OrganizationAggregate:
    headcount: int
    usd: UsdAggregate | None


class EmployeeRepository:
    """All employee persistence lives here so services never build SQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, values: Mapping[str, Any]) -> Employee:
        employee = Employee(**values)
        self._session.add(employee)
        self._session.commit()
        self._session.refresh(employee)
        return employee

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self._session.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return self._session.scalars(select(Employee).where(Employee.email == email)).first()

    def update(self, employee: Employee, values: Mapping[str, Any]) -> Employee:
        for field, value in values.items():
            setattr(employee, field, value)
        self._session.commit()
        self._session.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self._session.delete(employee)
        self._session.commit()

    def find_page(
        self,
        *,
        search: str | None,
        country: str | None,
        department: str | None,
        job_title: str | None,
        sort_by: EmployeeSortField,
        sort_order: SortOrder,
        offset: int,
        limit: int,
    ) -> tuple[list[Employee], int]:
        """Filter, count, sort and slice in SQL so only one page of rows is ever loaded."""
        conditions = self._filter_conditions(search, country, department, job_title)
        total = self._session.scalar(select(func.count(Employee.id)).where(*conditions)) or 0
        statement = self._ordered(select(Employee).where(*conditions), sort_by, sort_order)
        employees = self._session.scalars(statement.offset(offset).limit(limit)).all()
        return list(employees), total

    def distinct_countries(self) -> list[str]:
        return self._distinct_values(Employee.country)

    def distinct_departments(self) -> list[str]:
        return self._distinct_values(Employee.department)

    def distinct_job_titles(self) -> list[str]:
        return self._distinct_values(Employee.job_title)

    def _distinct_values(self, column: InstrumentedAttribute[str]) -> list[str]:
        return list(self._session.scalars(select(column).distinct().order_by(column)).all())

    @staticmethod
    def _filter_conditions(
        search: str | None, country: str | None, department: str | None, job_title: str | None
    ) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []
        if search:
            conditions.append(
                or_(
                    Employee.full_name.icontains(search, autoescape=True),
                    Employee.email.icontains(search, autoescape=True),
                )
            )
        if country:
            conditions.append(Employee.country == country)
        if department:
            conditions.append(Employee.department == department)
        if job_title:
            conditions.append(Employee.job_title == job_title)
        return conditions

    @staticmethod
    def _ordered(
        statement: Select[Employee], sort_by: EmployeeSortField, sort_order: SortOrder
    ) -> Select[Employee]:
        column = SORTABLE_COLUMNS[sort_by]
        primary = column.desc() if sort_order == SortOrder.DESC else column.asc()
        return statement.order_by(primary, Employee.id.asc())

    def count_all(self) -> int:
        return self._session.scalar(select(func.count(Employee.id))) or 0

    def bulk_create(self, rows: Sequence[Mapping[str, Any]]) -> None:
        """One multi-row INSERT per call; far faster than adding ORM objects one by one."""
        self._session.execute(insert(Employee), list(rows))
        self._session.commit()

    def delete_all(self) -> None:
        self._session.execute(delete(Employee))
        self._session.commit()

    def salary_stats_by_country(self, usd_rates: UsdRates) -> list[SalaryAggregate]:
        """Aggregate in SQL with GROUP BY so 10,000 rows never reach Python."""
        return self._grouped_salary_stats(Employee.country, usd_rates)

    def salary_stats_by_job_title(self, country: str, usd_rates: UsdRates) -> list[SalaryAggregate]:
        return self._grouped_salary_stats(
            Employee.job_title, usd_rates, Employee.country == country
        )

    def salary_stats_by_department(
        self, country: str, usd_rates: UsdRates
    ) -> list[SalaryAggregate]:
        return self._grouped_salary_stats(
            Employee.department, usd_rates, Employee.country == country
        )

    def organization_salary_stats(self, usd_rates: UsdRates) -> OrganizationAggregate:
        """Convert every salary before aggregating, so each employee weighs the same."""
        headcount, *usd = self._session.execute(
            select(func.count(Employee.id), *_usd_statistics(usd_rates))
        ).one()
        return OrganizationAggregate(headcount, UsdAggregate(*usd) if headcount else None)

    def _grouped_salary_stats(
        self,
        group_column: InstrumentedAttribute[str],
        usd_rates: UsdRates,
        *conditions: ColumnElement[bool],
    ) -> list[SalaryAggregate]:
        average = type_coerce(
            func.round(func.avg(Employee.annual_gross_salary), SALARY_SCALE),
            Numeric(SALARY_PRECISION, SALARY_SCALE),
        )
        statement = (
            select(
                group_column,
                Employee.currency,
                func.count(Employee.id),
                func.min(Employee.annual_gross_salary),
                func.max(Employee.annual_gross_salary),
                average,
                *_usd_statistics(usd_rates),
            )
            .where(*conditions)
            .group_by(group_column, Employee.currency)
            .order_by(group_column)
        )
        return [_to_salary_aggregate(row) for row in self._session.execute(statement).all()]


def _to_salary_aggregate(row: Sequence[Any]) -> SalaryAggregate:
    group, currency, headcount, minimum, maximum, average, *usd = row
    return SalaryAggregate(
        group, currency, headcount, minimum, maximum, average, UsdAggregate(*usd)
    )


def _usd_statistics(usd_rates: UsdRates) -> list[ColumnElement[Decimal]]:
    """MIN, MAX and AVG of salary x rate, unrounded; the rate is picked per row by currency."""
    usd_salary = Employee.annual_gross_salary * case(dict(usd_rates), value=Employee.currency)
    return [
        type_coerce(aggregate(usd_salary), Numeric())
        for aggregate in (func.min, func.max, func.avg)
    ]
