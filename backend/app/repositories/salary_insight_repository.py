from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from sqlalchemy import ColumnElement, Numeric, case, func, select, type_coerce
from sqlalchemy.orm import InstrumentedAttribute, Session

from app.constants.employee_constants import SALARY_PRECISION, SALARY_SCALE, Currency
from app.models.employee_model import Employee

UsdRates = Mapping[Currency, Decimal]


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


class SalaryInsightRepository:
    """Salary aggregations, kept apart from employee CRUD; every statistic is computed in SQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

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
