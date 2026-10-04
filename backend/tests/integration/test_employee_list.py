from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.constants.api_constants import API_V1_PREFIX, EMPLOYEES_PATH
from app.constants.employee_constants import Country, Currency, Department, JobTitle
from app.constants.message_constants import ErrorCode
from app.constants.pagination_constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from tests.factories import build_employee_record, build_numbered_records, insert_employees

EMPLOYEES_URL = f"{API_V1_PREFIX}{EMPLOYEES_PATH}"


def list_employees(client: TestClient, **params: Any) -> dict[str, Any]:
    response = client.get(EMPLOYEES_URL, params=params)
    assert response.status_code == status.HTTP_200_OK, response.text
    body: dict[str, Any] = response.json()
    return body


def names_of(body: dict[str, Any]) -> list[str]:
    return [item["full_name"] for item in body["items"]]


@pytest.fixture
def mixed_employees(session: Session) -> None:
    insert_employees(
        session,
        [
            build_employee_record(
                full_name="Priya Shah",
                email="priya.shah@acme.com",
                country=Country.INDIA.value,
                currency=Currency.INR.value,
                department=Department.ENGINEERING.value,
                job_title=JobTitle.SOFTWARE_ENGINEER.value,
                annual_salary="1800000.00",
            ),
            build_employee_record(
                full_name="Ravi Kumar",
                email="ravi.kumar@acme.com",
                country=Country.INDIA.value,
                currency=Currency.INR.value,
                department=Department.SALES.value,
                job_title=JobTitle.SALES_REPRESENTATIVE.value,
                annual_salary="900000.00",
            ),
            build_employee_record(
                full_name="Hannah Weber",
                email="hannah.weber@acme.com",
                country=Country.GERMANY.value,
                currency=Currency.EUR.value,
                department=Department.ENGINEERING.value,
                job_title=JobTitle.SOFTWARE_ENGINEER.value,
                annual_salary="70000.00",
            ),
            build_employee_record(
                full_name="John Smith",
                email="j.smith@acme.com",
                country=Country.UNITED_STATES.value,
                currency=Currency.USD.value,
                department=Department.FINANCE.value,
                job_title=JobTitle.ACCOUNTANT.value,
                annual_salary="95000.00",
            ),
        ],
    )


def test_list_employees_returns_first_page_with_defaults(
    client: TestClient, mixed_employees: None
) -> None:
    body = list_employees(client)

    assert body["total"] == 4
    assert body["page"] == 1
    assert body["page_size"] == DEFAULT_PAGE_SIZE
    assert len(body["items"]) == 4


def test_list_employees_sorts_by_full_name_ascending_by_default(
    client: TestClient, mixed_employees: None
) -> None:
    body = list_employees(client)

    assert names_of(body) == ["Hannah Weber", "John Smith", "Priya Shah", "Ravi Kumar"]


def test_list_employees_filters_by_country(client: TestClient, mixed_employees: None) -> None:
    body = list_employees(client, country=Country.INDIA.value)

    assert body["total"] == 2
    assert {item["country"] for item in body["items"]} == {Country.INDIA.value}


def test_list_employees_combines_department_and_job_title_filters(
    client: TestClient, mixed_employees: None
) -> None:
    body = list_employees(
        client,
        department=Department.ENGINEERING.value,
        job_title=JobTitle.SOFTWARE_ENGINEER.value,
    )

    assert names_of(body) == ["Hannah Weber", "Priya Shah"]


def test_list_employees_search_by_name_is_case_insensitive(
    client: TestClient, mixed_employees: None
) -> None:
    body = list_employees(client, search="pRiYa")

    assert names_of(body) == ["Priya Shah"]


def test_list_employees_search_matches_email(client: TestClient, mixed_employees: None) -> None:
    body = list_employees(client, search="J.SMITH@")

    assert names_of(body) == ["John Smith"]


def test_list_employees_search_treats_wildcards_literally(
    client: TestClient, mixed_employees: None
) -> None:
    body = list_employees(client, search="%")

    assert body["total"] == 0


def test_list_employees_search_combines_with_filters(
    client: TestClient, mixed_employees: None
) -> None:
    body = list_employees(client, search="a", country=Country.GERMANY.value)

    assert names_of(body) == ["Hannah Weber"]


def test_list_employees_paginates_with_correct_total_and_page(
    client: TestClient, session: Session
) -> None:
    insert_employees(session, build_numbered_records(25))

    second_page = list_employees(client, page=2, page_size=10)
    last_page = list_employees(client, page=3, page_size=10)

    assert second_page["total"] == 25
    assert second_page["page"] == 2
    assert names_of(second_page) == [f"Employee {number:02d}" for number in range(11, 21)]
    assert names_of(last_page) == [f"Employee {number:02d}" for number in range(21, 26)]


def test_list_employees_returns_empty_items_past_the_last_page(
    client: TestClient, session: Session
) -> None:
    insert_employees(session, build_numbered_records(3))

    body = list_employees(client, page=5, page_size=10)

    assert body["items"] == []
    assert body["total"] == 3


@pytest.mark.parametrize(
    "params",
    [
        {"page_size": MAX_PAGE_SIZE + 1},
        {"page_size": 0},
        {"page": 0},
        {"sort_by": "salary_secret"},
        {"sort_order": "sideways"},
        {"country": "Atlantis"},
    ],
)
def test_list_employees_rejects_invalid_query_parameters(
    client: TestClient, params: dict[str, Any]
) -> None:
    response = client.get(EMPLOYEES_URL, params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR


def test_list_employees_accepts_the_maximum_page_size(client: TestClient) -> None:
    body = list_employees(client, page_size=MAX_PAGE_SIZE)

    assert body["page_size"] == MAX_PAGE_SIZE


def test_list_employees_sorts_by_salary_ascending(
    client: TestClient, mixed_employees: None
) -> None:
    body = list_employees(
        client, country=Country.INDIA.value, sort_by="annual_salary", sort_order="asc"
    )

    assert names_of(body) == ["Ravi Kumar", "Priya Shah"]


def test_list_employees_sorts_by_salary_descending(
    client: TestClient, mixed_employees: None
) -> None:
    body = list_employees(
        client, country=Country.INDIA.value, sort_by="annual_salary", sort_order="desc"
    )

    assert names_of(body) == ["Priya Shah", "Ravi Kumar"]


def test_list_employees_sorts_by_name_descending(client: TestClient, mixed_employees: None) -> None:
    body = list_employees(client, sort_by="full_name", sort_order="desc")

    assert names_of(body) == ["Ravi Kumar", "Priya Shah", "John Smith", "Hannah Weber"]
