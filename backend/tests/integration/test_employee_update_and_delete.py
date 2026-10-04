from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient

from app.constants.api_constants import API_V1_PREFIX, EMPLOYEES_PATH
from app.constants.employee_constants import Country, Currency
from app.constants.message_constants import ErrorCode
from tests.factories import build_employee_payload

EMPLOYEES_URL = f"{API_V1_PREFIX}{EMPLOYEES_PATH}"
UNKNOWN_EMPLOYEE_ID = 999


def create_employee(client: TestClient, **overrides: str) -> dict[str, str]:
    response = client.post(EMPLOYEES_URL, json=build_employee_payload(**overrides))
    assert response.status_code == status.HTTP_201_CREATED
    body: dict[str, str] = response.json()
    return body


def test_update_employee_changes_fields_and_refreshes_updated_at(client: TestClient) -> None:
    created = create_employee(client)
    changes = build_employee_payload(
        full_name="Asha Rao-Menon",
        country=Country.GERMANY.value,
        currency=Currency.EUR.value,
        annual_salary="72000.00",
    )

    response = client.put(f"{EMPLOYEES_URL}/{created['id']}", json=changes)

    assert response.status_code == status.HTTP_200_OK
    updated = response.json()
    assert updated["full_name"] == "Asha Rao-Menon"
    assert updated["country"] == Country.GERMANY.value
    assert updated["currency"] == Currency.EUR.value
    assert updated["annual_salary"] == "72000.00"
    assert updated["created_at"] == created["created_at"]
    assert datetime.fromisoformat(updated["updated_at"]) > datetime.fromisoformat(
        created["updated_at"]
    )


def test_update_employee_rejects_duplicate_email(client: TestClient) -> None:
    create_employee(client, email="first@acme.com")
    second = create_employee(client, email="second@acme.com")

    response = client.put(
        f"{EMPLOYEES_URL}/{second['id']}", json=build_employee_payload(email="first@acme.com")
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["error"]["code"] == ErrorCode.DUPLICATE_EMAIL


def test_update_employee_rejects_invalid_salary(client: TestClient) -> None:
    created = create_employee(client)

    response = client.put(
        f"{EMPLOYEES_URL}/{created['id']}", json=build_employee_payload(annual_salary="0")
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_update_employee_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.put(f"{EMPLOYEES_URL}/{UNKNOWN_EMPLOYEE_ID}", json=build_employee_payload())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["error"]["code"] == ErrorCode.NOT_FOUND


def test_delete_employee_returns_204(client: TestClient) -> None:
    created = create_employee(client)

    response = client.delete(f"{EMPLOYEES_URL}/{created['id']}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


def test_deleted_employee_can_no_longer_be_fetched(client: TestClient) -> None:
    created = create_employee(client)
    client.delete(f"{EMPLOYEES_URL}/{created['id']}")

    response = client.get(f"{EMPLOYEES_URL}/{created['id']}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_employee_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.delete(f"{EMPLOYEES_URL}/{UNKNOWN_EMPLOYEE_ID}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
