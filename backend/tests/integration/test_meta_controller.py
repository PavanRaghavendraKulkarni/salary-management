from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.constants.api_constants import API_V1_PREFIX, META_PATH
from app.constants.employee_constants import (
    COUNTRY_CURRENCY,
    Country,
    Currency,
    Department,
    JobTitle,
)
from tests.factories import build_employee_record, insert_employees

META_URL = f"{API_V1_PREFIX}{META_PATH}"


def test_filters_return_distinct_sorted_values_present_in_the_data(
    client: TestClient, session: Session
) -> None:
    insert_employees(
        session,
        [
            build_employee_record(
                email="a@acme.com",
                country=Country.INDIA.value,
                currency=Currency.INR.value,
                department=Department.SALES.value,
                job_title=JobTitle.SALES_REPRESENTATIVE.value,
            ),
            build_employee_record(
                email="b@acme.com",
                country=Country.INDIA.value,
                currency=Currency.INR.value,
                department=Department.ENGINEERING.value,
                job_title=JobTitle.SOFTWARE_ENGINEER.value,
            ),
            build_employee_record(
                email="c@acme.com",
                country=Country.CANADA.value,
                currency=Currency.CAD.value,
                department=Department.ENGINEERING.value,
                job_title=JobTitle.SOFTWARE_ENGINEER.value,
            ),
        ],
    )

    response = client.get(f"{META_URL}/filters")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "countries": [Country.CANADA.value, Country.INDIA.value],
        "departments": [Department.ENGINEERING.value, Department.SALES.value],
        "job_titles": [JobTitle.SALES_REPRESENTATIVE.value, JobTitle.SOFTWARE_ENGINEER.value],
    }


def test_filters_are_empty_when_there_are_no_employees(client: TestClient) -> None:
    response = client.get(f"{META_URL}/filters")

    assert response.json() == {"countries": [], "departments": [], "job_titles": []}


def test_reference_data_lists_every_allowed_value_and_country_currency(
    client: TestClient,
) -> None:
    response = client.get(f"{META_URL}/reference-data")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["countries"] == [
        {"name": country.value, "currency": currency.value}
        for country, currency in COUNTRY_CURRENCY.items()
    ]
    assert body["departments"] == [department.value for department in Department]
    assert body["job_titles"] == [job_title.value for job_title in JobTitle]
