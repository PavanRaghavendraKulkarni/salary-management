from datetime import date

import pytest
from sqlalchemy.orm import Session

from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.views.employee_view import EmployeeCreate
from scripts.seed import build_employee_records, seed_employees

FIXED_TODAY = date(2026, 1, 15)
SMALL_COUNT = 40
RANDOM_SEED = 7
OTHER_RANDOM_SEED = 8
SMALL_BATCH_SIZE = 15


@pytest.fixture
def repository(session: Session) -> EmployeeRepository:
    return EmployeeRepository(session)


def test_build_employee_records_creates_the_requested_number_of_rows() -> None:
    records = build_employee_records(SMALL_COUNT, RANDOM_SEED, FIXED_TODAY)

    assert len(records) == SMALL_COUNT


def test_build_employee_records_is_identical_for_the_same_seed() -> None:
    first = build_employee_records(SMALL_COUNT, RANDOM_SEED, FIXED_TODAY)
    second = build_employee_records(SMALL_COUNT, RANDOM_SEED, FIXED_TODAY)

    assert first == second


def test_build_employee_records_differs_for_a_different_seed() -> None:
    first = build_employee_records(SMALL_COUNT, RANDOM_SEED, FIXED_TODAY)
    second = build_employee_records(SMALL_COUNT, OTHER_RANDOM_SEED, FIXED_TODAY)

    assert first != second


def test_build_employee_records_generates_unique_emails() -> None:
    records = build_employee_records(SMALL_COUNT, RANDOM_SEED, FIXED_TODAY)

    assert len({record["email"] for record in records}) == SMALL_COUNT


def test_every_seeded_record_passes_the_same_validation_as_the_api(
    repository: EmployeeRepository,
) -> None:
    service = EmployeeService(repository, today_provider=lambda: FIXED_TODAY)

    for record in build_employee_records(SMALL_COUNT, RANDOM_SEED, FIXED_TODAY):
        service.create_employee(EmployeeCreate.model_validate(record))

    assert repository.count_all() == SMALL_COUNT


def test_seed_employees_inserts_rows_in_batches_into_an_empty_database(
    repository: EmployeeRepository,
) -> None:
    inserted = seed_employees(
        repository,
        count=SMALL_COUNT,
        random_seed=RANDOM_SEED,
        today=FIXED_TODAY,
        batch_size=SMALL_BATCH_SIZE,
        reset=False,
    )

    assert inserted == SMALL_COUNT
    assert repository.count_all() == SMALL_COUNT


def test_seed_employees_skips_when_data_already_exists(repository: EmployeeRepository) -> None:
    seed_employees(
        repository,
        count=SMALL_COUNT,
        random_seed=RANDOM_SEED,
        today=FIXED_TODAY,
        batch_size=SMALL_BATCH_SIZE,
        reset=False,
    )

    inserted = seed_employees(
        repository,
        count=SMALL_COUNT,
        random_seed=OTHER_RANDOM_SEED,
        today=FIXED_TODAY,
        batch_size=SMALL_BATCH_SIZE,
        reset=False,
    )

    assert inserted == 0
    assert repository.count_all() == SMALL_COUNT


def test_seed_employees_with_reset_replaces_existing_data(
    repository: EmployeeRepository,
) -> None:
    seed_employees(
        repository,
        count=SMALL_COUNT,
        random_seed=RANDOM_SEED,
        today=FIXED_TODAY,
        batch_size=SMALL_BATCH_SIZE,
        reset=False,
    )

    inserted = seed_employees(
        repository,
        count=SMALL_COUNT // 2,
        random_seed=OTHER_RANDOM_SEED,
        today=FIXED_TODAY,
        batch_size=SMALL_BATCH_SIZE,
        reset=True,
    )

    assert inserted == SMALL_COUNT // 2
    assert repository.count_all() == SMALL_COUNT // 2
