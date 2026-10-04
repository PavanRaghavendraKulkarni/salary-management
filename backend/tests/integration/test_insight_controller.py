from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.constants.api_constants import API_V1_PREFIX, INSIGHTS_PATH
from app.constants.employee_constants import Country, Currency, Department, JobTitle
from app.constants.message_constants import ErrorCode
from tests.factories import build_insight_dataset, insert_employees

INSIGHTS_URL = f"{API_V1_PREFIX}{INSIGHTS_PATH}"


@pytest.fixture
def insight_dataset(session: Session) -> None:
    insert_employees(session, build_insight_dataset())


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
        },
        {
            "country": Country.INDIA.value,
            "currency": Currency.INR.value,
            "headcount": 3,
            "min_salary": "700000.00",
            "max_salary": "1500000.00",
            "average_salary": "1066666.67",
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
        "groups": [
            {
                "name": JobTitle.SALES_REPRESENTATIVE.value,
                "headcount": 1,
                "min_salary": "700000.00",
                "max_salary": "700000.00",
                "average_salary": "700000.00",
            },
            {
                "name": JobTitle.SOFTWARE_ENGINEER.value,
                "headcount": 2,
                "min_salary": "1000000.00",
                "max_salary": "1500000.00",
                "average_salary": "1250000.00",
            },
        ],
    }


def test_department_insights_group_by_department_within_a_country(
    client: TestClient, insight_dataset: None
) -> None:
    assert get_json(client, "/departments", country=Country.GERMANY.value) == {
        "country": Country.GERMANY.value,
        "currency": Currency.EUR.value,
        "groups": [
            {
                "name": Department.ENGINEERING.value,
                "headcount": 1,
                "min_salary": "60000.00",
                "max_salary": "60000.00",
                "average_salary": "60000.00",
            },
            {
                "name": Department.FINANCE.value,
                "headcount": 1,
                "min_salary": "50000.20",
                "max_salary": "50000.20",
                "average_salary": "50000.20",
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
