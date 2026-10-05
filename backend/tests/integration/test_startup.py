from pathlib import Path

from fastapi import status
from fastapi.testclient import TestClient

from app.constants.api_constants import API_V1_PREFIX, EMPLOYEES_PATH
from app.constants.pagination_constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from app.main import create_app
from tests.factories import build_test_settings


def test_fresh_database_returns_an_empty_employee_list(tmp_path: Path) -> None:
    """No seed has run and no tables exist, so start-up must create them."""
    settings = build_test_settings(database_url=f"sqlite:///{tmp_path / 'fresh.db'}")

    with TestClient(create_app(settings)) as client:
        response = client.get(f"{API_V1_PREFIX}{EMPLOYEES_PATH}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "items": [],
        "total": 0,
        "page": DEFAULT_PAGE,
        "page_size": DEFAULT_PAGE_SIZE,
    }
