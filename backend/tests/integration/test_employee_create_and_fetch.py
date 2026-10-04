from datetime import date, timedelta

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.constants.api_constants import API_V1_PREFIX, EMPLOYEES_PATH
from app.constants.employee_constants import Country, Currency
from app.constants.message_constants import ErrorCode
from tests.factories import build_employee_payload

EMPLOYEES_URL = f"{API_V1_PREFIX}{EMPLOYEES_PATH}"
UNKNOWN_EMPLOYEE_ID = 999


def test_create_employee_returns_201_with_the_employee(client: TestClient) -> None:
    payload = build_employee_payload()

    response = client.post(EMPLOYEES_URL, json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["id"] > 0
    assert body["email"] == payload["email"]
    assert body["annual_salary"] == payload["annual_salary"]
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_create_employee_rejects_duplicate_email(client: TestClient) -> None:
    client.post(EMPLOYEES_URL, json=build_employee_payload())

    response = client.post(EMPLOYEES_URL, json=build_employee_payload(full_name="Someone Else"))

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["error"]["code"] == ErrorCode.DUPLICATE_EMAIL


@pytest.mark.parametrize("salary", ["0", "-1", "-5000.50"])
def test_create_employee_rejects_salary_of_zero_or_below(client: TestClient, salary: str) -> None:
    response = client.post(EMPLOYEES_URL, json=build_employee_payload(annual_salary=salary))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR


def test_create_employee_rejects_currency_that_does_not_match_country(
    client: TestClient,
) -> None:
    payload = build_employee_payload(country=Country.GERMANY.value, currency=Currency.USD.value)

    response = client.post(EMPLOYEES_URL, json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR


def test_create_employee_rejects_hire_date_in_the_future(client: TestClient) -> None:
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    response = client.post(EMPLOYEES_URL, json=build_employee_payload(hire_date=tomorrow))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["error"]["code"] == ErrorCode.VALIDATION_ERROR


@pytest.mark.parametrize(
    "overrides",
    [
        {"full_name": "A"},
        {"full_name": "A" * 101},
        {"email": "not-an-email"},
        {"job_title": "Astronaut"},
        {"department": "Space"},
        {"country": "Atlantis"},
    ],
)
def test_create_employee_rejects_invalid_fields(
    client: TestClient, overrides: dict[str, str]
) -> None:
    response = client.post(EMPLOYEES_URL, json=build_employee_payload(**overrides))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    error = response.json()["error"]
    assert error["code"] == ErrorCode.VALIDATION_ERROR
    assert error["message"]


def test_get_employee_returns_the_created_employee(client: TestClient) -> None:
    created = client.post(EMPLOYEES_URL, json=build_employee_payload()).json()

    response = client.get(f"{EMPLOYEES_URL}/{created['id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == created


def test_get_employee_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get(f"{EMPLOYEES_URL}/{UNKNOWN_EMPLOYEE_ID}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "error": {
            "code": ErrorCode.NOT_FOUND,
            "message": f"Employee with id {UNKNOWN_EMPLOYEE_ID} was not found.",
        }
    }
