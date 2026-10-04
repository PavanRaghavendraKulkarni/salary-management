from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.constants.employee_constants import Country, Currency, JobTitle
from app.repositories.employee_repository import EmployeeRepository
from app.services.insight_service import InsightService
from tests.factories import build_employee_record, build_insight_dataset, insert_employees


@pytest.fixture
def service(session: Session) -> InsightService:
    return InsightService(EmployeeRepository(session))


def test_country_insights_round_average_to_two_decimal_places(
    service: InsightService, session: Session
) -> None:
    insert_employees(session, build_insight_dataset())

    india = next(item for item in service.get_country_insights() if item.country == Country.INDIA)

    assert india.average_salary == Decimal("1066666.67")
    assert india.average_salary.as_tuple().exponent == -2


def test_country_insights_are_ordered_by_country_name(
    service: InsightService, session: Session
) -> None:
    insert_employees(session, build_insight_dataset())

    countries = [item.country for item in service.get_country_insights()]

    assert countries == sorted(countries)


def test_average_of_one_third_cent_values_rounds_half_up(
    service: InsightService, session: Session
) -> None:
    insert_employees(
        session,
        [
            build_employee_record(email="a@acme.com", annual_salary="100.00"),
            build_employee_record(email="b@acme.com", annual_salary="100.00"),
            build_employee_record(email="c@acme.com", annual_salary="100.02"),
        ],
    )

    breakdown = service.get_job_title_insights(Country.INDIA)

    assert breakdown.groups[0].average_salary == Decimal("100.01")


def test_breakdown_uses_the_country_currency_even_without_employees(
    service: InsightService,
) -> None:
    breakdown = service.get_job_title_insights(Country.SINGAPORE)

    assert breakdown.currency == Currency.SGD
    assert breakdown.groups == []


def test_job_title_breakdown_only_counts_the_requested_country(
    service: InsightService, session: Session
) -> None:
    insert_employees(session, build_insight_dataset())

    breakdown = service.get_job_title_insights(Country.GERMANY)

    assert {group.name for group in breakdown.groups} == {
        JobTitle.ACCOUNTANT.value,
        JobTitle.SOFTWARE_ENGINEER.value,
    }
    assert sum(group.headcount for group in breakdown.groups) == 2
