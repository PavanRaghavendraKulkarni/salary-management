import logging
from collections.abc import Iterator

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.constants.api_constants import API_V1_PREFIX, EMPLOYEES_PATH
from app.constants.message_constants import INTERNAL_ERROR_MESSAGE, ErrorCode
from app.dependencies.providers import get_employee_service
from app.exceptions import exception_handlers

EMPLOYEES_URL = f"{API_V1_PREFIX}{EMPLOYEES_PATH}"
FAILURE_DETAIL = "connection to the database was lost"


def fail_unexpectedly() -> None:
    raise RuntimeError(FAILURE_DETAIL)


@pytest.fixture
def failing_client(app: FastAPI) -> Iterator[TestClient]:
    """A dependency fails like a bug would; server errors become responses, not test errors."""
    app.dependency_overrides[get_employee_service] = fail_unexpectedly
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


def test_unexpected_error_returns_500_with_the_standard_error_shape(
    failing_client: TestClient,
) -> None:
    response = failing_client.get(EMPLOYEES_URL)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "error": {"code": ErrorCode.INTERNAL_ERROR, "message": INTERNAL_ERROR_MESSAGE}
    }


def test_unexpected_error_does_not_leak_internal_details(failing_client: TestClient) -> None:
    assert FAILURE_DETAIL not in failing_client.get(EMPLOYEES_URL).text


def test_unexpected_error_is_logged_with_its_traceback(
    failing_client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.ERROR, logger=exception_handlers.__name__):
        failing_client.get(EMPLOYEES_URL)

    [record] = [entry for entry in caplog.records if entry.name == exception_handlers.__name__]
    assert record.exc_info is not None
    assert isinstance(record.exc_info[1], RuntimeError)
    assert EMPLOYEES_URL in record.getMessage()
