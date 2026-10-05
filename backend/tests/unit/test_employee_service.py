from datetime import date, timedelta

import pytest
from sqlalchemy.orm import Session

from app.constants.employee_constants import Country, Currency
from app.exceptions.domain_exceptions import (
    DomainValidationError,
    DuplicateEmailError,
    EmployeeNotFoundError,
)
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from tests.factories import build_employee_create, build_employee_update

FIXED_TODAY = date(2026, 1, 15)
UNKNOWN_EMPLOYEE_ID = 999


@pytest.fixture
def service(session: Session) -> EmployeeService:
    return EmployeeService(EmployeeRepository(session), today_provider=lambda: FIXED_TODAY)


def test_create_employee_returns_saved_employee_with_id(service: EmployeeService) -> None:
    created = service.create_employee(build_employee_create())

    assert created.id > 0
    assert created.full_name == "Asha Rao"


def test_create_employee_stores_email_in_lowercase(service: EmployeeService) -> None:
    created = service.create_employee(build_employee_create(email="Asha.Rao@ACME.com"))

    assert created.email == "asha.rao@acme.com"


def test_create_employee_rejects_duplicate_email_ignoring_case(
    service: EmployeeService,
) -> None:
    service.create_employee(build_employee_create(email="asha.rao@acme.com"))

    with pytest.raises(DuplicateEmailError):
        service.create_employee(build_employee_create(email="ASHA.RAO@acme.com"))


def test_create_employee_rejects_currency_that_does_not_match_country(
    service: EmployeeService,
) -> None:
    payload = build_employee_create(country=Country.INDIA.value, currency=Currency.USD.value)

    with pytest.raises(DomainValidationError):
        service.create_employee(payload)


def test_create_employee_rejects_hire_date_in_the_future(service: EmployeeService) -> None:
    tomorrow = FIXED_TODAY + timedelta(days=1)

    with pytest.raises(DomainValidationError):
        service.create_employee(build_employee_create(hire_date=tomorrow.isoformat()))


def test_create_employee_accepts_hire_date_of_today(service: EmployeeService) -> None:
    created = service.create_employee(build_employee_create(hire_date=FIXED_TODAY.isoformat()))

    assert created.hire_date == FIXED_TODAY


def test_get_employee_returns_existing_employee(service: EmployeeService) -> None:
    created = service.create_employee(build_employee_create())

    fetched = service.get_employee(created.id)

    assert fetched == created


def test_get_employee_raises_not_found_for_unknown_id(service: EmployeeService) -> None:
    with pytest.raises(EmployeeNotFoundError):
        service.get_employee(UNKNOWN_EMPLOYEE_ID)


def test_update_employee_replaces_editable_fields(service: EmployeeService) -> None:
    created = service.create_employee(build_employee_create())

    updated = service.update_employee(
        created.id,
        build_employee_update(full_name="Asha Rao-Menon", annual_gross_salary="1750000.00"),
    )

    assert updated.full_name == "Asha Rao-Menon"
    assert str(updated.annual_gross_salary) == "1750000.00"
    assert updated.created_at == created.created_at
    assert updated.updated_at > created.updated_at


def test_update_employee_allows_keeping_the_same_email(service: EmployeeService) -> None:
    created = service.create_employee(build_employee_create())

    updated = service.update_employee(created.id, build_employee_update(email=created.email))

    assert updated.email == created.email


def test_update_employee_rejects_email_used_by_another_employee(
    service: EmployeeService,
) -> None:
    service.create_employee(build_employee_create(email="first@acme.com"))
    second = service.create_employee(build_employee_create(email="second@acme.com"))

    with pytest.raises(DuplicateEmailError):
        service.update_employee(second.id, build_employee_update(email="FIRST@acme.com"))


def test_update_employee_applies_the_same_validation_as_create(
    service: EmployeeService,
) -> None:
    created = service.create_employee(build_employee_create())

    with pytest.raises(DomainValidationError):
        service.update_employee(created.id, build_employee_update(currency=Currency.EUR.value))


def test_update_employee_raises_not_found_for_unknown_id(service: EmployeeService) -> None:
    with pytest.raises(EmployeeNotFoundError):
        service.update_employee(UNKNOWN_EMPLOYEE_ID, build_employee_update())


def test_delete_employee_removes_the_employee(service: EmployeeService) -> None:
    created = service.create_employee(build_employee_create())

    service.delete_employee(created.id)

    with pytest.raises(EmployeeNotFoundError):
        service.get_employee(created.id)


def test_delete_employee_raises_not_found_for_unknown_id(service: EmployeeService) -> None:
    with pytest.raises(EmployeeNotFoundError):
        service.delete_employee(UNKNOWN_EMPLOYEE_ID)
