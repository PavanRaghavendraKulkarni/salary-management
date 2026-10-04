"""Generate a deterministic set of realistic ACME employees.

Run from the backend folder: ``uv run python -m scripts.seed [--reset] [--count N]``.
"""

import argparse
import logging
import random
import unicodedata
from collections.abc import Sequence
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from itertools import batched
from typing import Any

from faker import Faker

from app.config.database import SessionFactory, create_tables, engine
from app.constants.employee_constants import (
    COUNTRY_CURRENCY,
    SALARY_QUANTUM,
    Country,
    JobTitle,
)
from app.constants.seed_constants import (
    COUNTRY_BASE_SALARY_BAND,
    COUNTRY_HEADCOUNT_WEIGHT,
    COUNTRY_NAME_LOCALE,
    JOB_TITLE_DEPARTMENT,
    JOB_TITLE_HEADCOUNT_WEIGHT,
    JOB_TITLE_SALARY_MULTIPLIER,
    SEED_BATCH_SIZE,
    SEED_EMAIL_DOMAIN,
    SEED_EMAIL_FALLBACK_NAME,
    SEED_EMPLOYEE_COUNT,
    SEED_MAX_TENURE_DAYS,
    SEED_RANDOM_SEED,
    SEED_SALARY_ROUNDING,
)
from app.repositories.employee_repository import EmployeeRepository

logger = logging.getLogger(__name__)


class EmployeeRecordGenerator:
    """Builds employee rows from one seeded random source so every run yields the same data."""

    def __init__(self, random_seed: int, today: date) -> None:
        self._random = random.Random(random_seed)
        self._today = today
        self._fakers: dict[str, Faker] = {}
        for locale in sorted(set(COUNTRY_NAME_LOCALE.values())):
            faker = Faker(locale)
            faker.seed_instance(random_seed)
            self._fakers[locale] = faker

    def build(self, sequence_number: int) -> dict[str, Any]:
        country = self._pick_weighted(COUNTRY_HEADCOUNT_WEIGHT)
        job_title = self._pick_weighted(JOB_TITLE_HEADCOUNT_WEIGHT)
        full_name = self._full_name(country)
        return {
            "full_name": full_name,
            "email": self._email(full_name, sequence_number),
            "job_title": job_title.value,
            "department": JOB_TITLE_DEPARTMENT[job_title].value,
            "country": country.value,
            "currency": COUNTRY_CURRENCY[country].value,
            "annual_salary": self._annual_salary(country, job_title),
            "hire_date": self._today
            - timedelta(days=self._random.randint(0, SEED_MAX_TENURE_DAYS)),
        }

    def _pick_weighted[ChoiceT](self, weights: dict[ChoiceT, int]) -> ChoiceT:
        return self._random.choices(list(weights), weights=list(weights.values()))[0]

    def _full_name(self, country: Country) -> str:
        faker = self._fakers[COUNTRY_NAME_LOCALE[country]]
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def _email(full_name: str, sequence_number: int) -> str:
        ascii_name = unicodedata.normalize("NFKD", full_name).encode("ascii", "ignore").decode()
        local_part = ".".join(ascii_name.lower().split()) or SEED_EMAIL_FALLBACK_NAME
        cleaned = "".join(
            character for character in local_part if character.isalnum() or character == "."
        )
        return f"{cleaned or SEED_EMAIL_FALLBACK_NAME}.{sequence_number}@{SEED_EMAIL_DOMAIN}"

    def _annual_salary(self, country: Country, job_title: JobTitle) -> Decimal:
        low, high = COUNTRY_BASE_SALARY_BAND[country]
        base = Decimal(str(self._random.uniform(float(low), float(high))))
        salary = base * JOB_TITLE_SALARY_MULTIPLIER[job_title]
        rounded = (salary / SEED_SALARY_ROUNDING).to_integral_value(ROUND_HALF_UP)
        return (rounded * SEED_SALARY_ROUNDING).quantize(SALARY_QUANTUM)


def build_employee_records(count: int, random_seed: int, today: date) -> list[dict[str, Any]]:
    generator = EmployeeRecordGenerator(random_seed, today)
    return [generator.build(sequence_number) for sequence_number in range(1, count + 1)]


def seed_employees(
    repository: EmployeeRepository,
    *,
    count: int,
    random_seed: int,
    today: date,
    batch_size: int,
    reset: bool,
) -> int:
    """Insert employees unless data exists, so restarting the app never duplicates the seed."""
    if reset:
        repository.delete_all()
    elif repository.count_all() > 0:
        return 0
    records = build_employee_records(count, random_seed, today)
    for batch in batched(records, batch_size):
        repository.bulk_create(batch)
    return len(records)


def parse_arguments(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the database with ACME employees.")
    parser.add_argument("--reset", action="store_true", help="delete existing employees first")
    parser.add_argument("--count", type=int, default=SEED_EMPLOYEE_COUNT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    arguments = parse_arguments(argv)
    create_tables(engine)
    with SessionFactory() as session:
        inserted = seed_employees(
            EmployeeRepository(session),
            count=arguments.count,
            random_seed=SEED_RANDOM_SEED,
            today=date.today(),
            batch_size=SEED_BATCH_SIZE,
            reset=arguments.reset,
        )
    if inserted:
        logger.info("Seeded %d employees.", inserted)
    else:
        logger.info("Employees already exist; skipped seeding (use --reset to replace them).")


if __name__ == "__main__":
    main()
