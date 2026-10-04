from sqlalchemy import inspect
from sqlalchemy.engine import Engine


def indexed_column_sets(engine: Engine) -> list[tuple[str, ...]]:
    return [tuple(index["column_names"]) for index in inspect(engine).get_indexes("employees")]


def test_employee_table_has_single_column_indexes_for_filters(engine: Engine) -> None:
    indexes = indexed_column_sets(engine)

    assert ("country",) in indexes
    assert ("job_title",) in indexes
    assert ("department",) in indexes


def test_employee_table_has_composite_country_and_job_title_index(engine: Engine) -> None:
    assert ("country", "job_title") in indexed_column_sets(engine)
