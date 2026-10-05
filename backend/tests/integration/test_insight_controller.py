from typing import Any

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.constants.api_constants import API_V1_PREFIX, INSIGHTS_PATH
from app.constants.currency_constants import USD_EXCHANGE_RATES, USD_EXCHANGE_RATES_AS_OF
from app.constants.employee_constants import Country, Currency, Department, JobTitle
from app.constants.message_constants import ErrorCode
from app.dependencies.providers import get_insight_service
from app.repositories.salary_insight_repository import SalaryInsightRepository
from app.services.insight_service import InsightService
from tests.factories import (
    TEST_RATES_AS_OF,
    TEST_USD_RATES,
    build_insight_dataset,
    insert_employees,
)

INSIGHTS_URL = f"{API_V1_PREFIX}{INSIGHTS_PATH}"
RATES_AS_OF = TEST_RATES_AS_OF.isoformat()


@pytest.fixture
def insight_dataset(app: FastAPI, session: Session) -> None:
    """The hand-built dataset, converted with the round test rates."""
    app.dependency_overrides[get_insight_service] = lambda: InsightService(
        SalaryInsightRepository(session), usd_rates=TEST_USD_RATES, rates_as_of=TEST_RATES_AS_OF
    )
    insert_employees(session, build_insight_dataset())


def usd(minimum: str, maximum: str, average: str) -> dict[str, str]:
    return {
        "min_salary": minimum,
        "max_salary": maximum,
        "average_salary": average,
        "rates_as_of": RATES_AS_OF,
    }


def get_json(client: TestClient, path: str, **params: str) -> Any:
    response = client.get(f"{INSIGHTS_URL}{path}", params=params)
    assert response.status_code == status.HTTP_200_OK, response.text
    return response.json()


def test_country_insights_report_exact_stats_per_country(
    client: TestClient, insight_dataset: None
) -> None:
    assert get_json(client, "/countries") == [
        {
            "country": Country.GERMANY.value,
            "currency": Currency.EUR.value,
            "headcount": 2,
            "min_salary": "50000.20",
            "max_salary": "60000.00",
            "average_salary": "55000.10",
            "usd_rate": "1.5",
            "usd": usd("75000.30", "90000.00", "82500.15"),
        },
        {
            "country": Country.INDIA.value,
            "currency": Currency.INR.value,
            "headcount": 3,
            "min_salary": "700000.00",
            "max_salary": "1500000.00",
            "average_salary": "1066666.67",
            "usd_rate": "0.01",
            "usd": usd("7000.00", "15000.00", "10666.67"),
        },
    ]


def test_country_insights_are_empty_without_employees(client: TestClient) -> None:
    assert get_json(client, "/countries") == []


def test_job_title_insights_group_by_job_title_within_a_country(
    client: TestClient, insight_dataset: None
) -> None:
    assert get_json(client, "/job-titles", country=Country.INDIA.value) == {
        "country": Country.INDIA.value,
        "currency": Currency.INR.value,
        "usd_rate": "0.01",
        "groups": [
            {
                "name": JobTitle.SALES_REPRESENTATIVE.value,
                "headcount": 1,
                "min_salary": "700000.00",
                "max_salary": "700000.00",
                "average_salary": "700000.00",
                "usd": usd("7000.00", "7000.00", "7000.00"),
            },
            {
                "name": JobTitle.SOFTWARE_ENGINEER.value,
                "headcount": 2,
                "min_salary": "1000000.00",
                "max_salary": "1500000.00",
                "average_salary": "1250000.00",
                "usd": usd("10000.00", "15000.00", "12500.00"),
            },
        ],
    }


def test_department_insights_group_by_department_within_a_country(
    client: TestClient, insight_dataset: None
) -> None:
    assert get_json(client, "/departments", country=Country.GERMANY.value) == {
        "country": Country.GERMANY.value,
        "currency": Currency.EUR.value,
        "usd_rate": "1.5",
        "groups": [
            {
                "name": Department.ENGINEERING.value,
                "headcount": 1,
                "min_salary": "60000.00",
                "max_salary": "60000.00",
                "average_salary": "60000.00",
                "usd": usd("90000.00", "90000.00", "90000.00"),
            },
            {
                "name": Department.FINANCE.value,
                "headcount": 1,
                "min_salary": "50000.20",
                "max_salary": "50000.20",
                "average_salary": "50000.20",
                "usd": usd("75000.30", "75000.30", "75000.30"),
            },
        ],
    }


@pytest.mark.parametrize("path", ["/job-titles", "/departments"])
def test_breakdown_for_a_country_without_employees_is_empty(
    client: TestClient, insight_dataset: None, path: str
) -> None:
    assert get_json(client, path, country=Country.JAPAN.value) == {
        "country": Country.JAPAN.value,
        "currency": Currency.JPY.value,
        "usd_rate": "1",
        "groups": [],
    }


@pytest.mark.parametrize("path", ["/job-titles", "/departments"])
@pytest.mark.parametrize("params", [{}, {"country": "Atlantis"}])
def test_breakdown_requires_a_valid_country(
    client: TestClient, path: str, params: dict[str, str]
) -> None:
    response = client.get(f"{INSIGHTS_URL}{path}", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR


def test_organization_insight_reports_usd_figures_across_all_countries(
    client: TestClient, insight_dataset: None
) -> None:
    """(10,000 + 15,000 + 7,000 + 90,000 + 75,000.30) / 5 = 39,400.06 USD."""
    assert get_json(client, "/organization") == {
        "headcount": 5,
        "usd": usd("7000.00", "90000.00", "39400.06"),
    }


def test_organization_insight_without_employees_has_no_usd_figures(client: TestClient) -> None:
    assert get_json(client, "/organization") == {"headcount": 0, "usd": None}


def test_insights_use_the_exchange_rates_from_constants_by_default(
    client: TestClient, session: Session
) -> None:
    insert_employees(session, build_insight_dataset())

    india = get_json(client, "/job-titles", country=Country.INDIA.value)

    assert india["usd_rate"] == str(USD_EXCHANGE_RATES[Currency.INR])
    assert india["groups"][0]["usd"]["rates_as_of"] == USD_EXCHANGE_RATES_AS_OF.isoformat()
