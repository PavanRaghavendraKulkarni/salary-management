from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.constants.employee_constants import Country, Currency, JobTitle
from app.repositories.employee_repository import EmployeeRepository
from app.services.insight_service import InsightService
from tests.factories import (
    TEST_RATES_AS_OF,
    TEST_USD_RATES,
    build_employee_record,
    build_insight_dataset,
    insert_employees,
)

UNITED_STATES = {"country": Country.UNITED_STATES.value, "currency": Currency.USD.value}


@pytest.fixture
def service(session: Session) -> InsightService:
    return InsightService(
        EmployeeRepository(session), usd_rates=TEST_USD_RATES, rates_as_of=TEST_RATES_AS_OF
    )


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


def test_average_with_fractional_cents_rounds_to_the_nearest_cent(
    service: InsightService, session: Session
) -> None:
    insert_employees(
        session,
        [
            build_employee_record(email="a@acme.com", annual_gross_salary="100.00"),
            build_employee_record(email="b@acme.com", annual_gross_salary="100.00"),
            build_employee_record(email="c@acme.com", annual_gross_salary="100.02"),
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


def test_country_insights_convert_to_usd_with_the_rate_and_its_date(
    service: InsightService, session: Session
) -> None:
    insert_employees(session, build_insight_dataset())

    india = next(item for item in service.get_country_insights() if item.country == Country.INDIA)

    assert india.usd_rate == Decimal("0.01")
    assert india.usd.min_salary == Decimal("7000.00")
    assert india.usd.max_salary == Decimal("15000.00")
    assert india.usd.average_salary == Decimal("10666.67")
    assert india.usd.rates_as_of == TEST_RATES_AS_OF


def test_breakdown_groups_include_usd_figures(service: InsightService, session: Session) -> None:
    insert_employees(session, build_insight_dataset())

    breakdown = service.get_department_insights(Country.GERMANY)

    assert breakdown.usd_rate == Decimal("1.5")
    assert [group.usd.average_salary for group in breakdown.groups] == [
        Decimal("90000.00"),
        Decimal("75000.30"),
    ]


def test_organization_average_converts_each_salary_before_averaging(
    service: InsightService, session: Session
) -> None:
    """One US employee at 200 USD and three in India at 100 USD each (10,000 INR).

    Per employee the average is (200 + 3 x 100) / 4 = 125. Averaging the two country
    averages instead would give (200 + 100) / 2 = 150, overweighting the smaller country.
    """
    insert_employees(
        session,
        [
            build_employee_record(
                email="us@acme.com", annual_gross_salary="200.00", **UNITED_STATES
            ),
            *[
                build_employee_record(email=f"in{number}@acme.com", annual_gross_salary="10000.00")
                for number in range(1, 4)
            ],
        ],
    )

    organization = service.get_organization_insight()

    assert organization.headcount == 4
    assert organization.usd is not None
    assert organization.usd.average_salary == Decimal("125.00")
    assert organization.usd.min_salary == Decimal("100.00")
    assert organization.usd.max_salary == Decimal("200.00")
    assert organization.usd.rates_as_of == TEST_RATES_AS_OF


def test_organization_usd_figures_are_rounded_only_after_averaging(
    service: InsightService, session: Session
) -> None:
    """Converted salaries are 1.006, 1.006 and 1.0001 USD; their average 1.00403 rounds to 1.00.

    Rounding each salary to cents first would give 1.01, 1.01 and 1.00, averaging 1.01.
    """
    insert_employees(
        session,
        [
            build_employee_record(email="a@acme.com", annual_gross_salary="100.60"),
            build_employee_record(email="b@acme.com", annual_gross_salary="100.60"),
            build_employee_record(email="c@acme.com", annual_gross_salary="100.01"),
        ],
    )

    organization = service.get_organization_insight()

    assert organization.usd is not None
    assert organization.usd.average_salary == Decimal("1.00")
    assert organization.usd.average_salary.as_tuple().exponent == -2


def test_organization_insight_without_employees_has_no_usd_figures(
    service: InsightService,
) -> None:
    organization = service.get_organization_insight()

    assert organization.headcount == 0
    assert organization.usd is None
