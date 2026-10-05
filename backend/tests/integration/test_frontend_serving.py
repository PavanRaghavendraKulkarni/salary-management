from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.constants.api_constants import API_V1_PREFIX
from app.constants.message_constants import ErrorCode
from app.main import create_app
from tests.factories import build_test_settings

INDEX_HTML = "<!doctype html><title>ACME</title>"
SCRIPT_BODY = "console.log('app');"


@pytest.fixture
def frontend_dist(tmp_path: Path) -> Path:
    (tmp_path / "assets").mkdir()
    (tmp_path / "index.html").write_text(INDEX_HTML)
    (tmp_path / "assets" / "app.js").write_text(SCRIPT_BODY)
    (tmp_path / "favicon.svg").write_text("<svg/>")
    return tmp_path


@pytest.fixture
def frontend_client(frontend_dist: Path) -> Iterator[TestClient]:
    application = create_app(build_test_settings(frontend_dist_dir=frontend_dist))
    with TestClient(application) as test_client:
        yield test_client


def test_root_serves_the_react_app(frontend_client: TestClient) -> None:
    response = frontend_client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.text == INDEX_HTML


@pytest.mark.parametrize("path", ["/employees", "/insights", "/some/deep/link"])
def test_client_side_routes_fall_back_to_the_react_app(
    frontend_client: TestClient, path: str
) -> None:
    response = frontend_client.get(path)

    assert response.status_code == status.HTTP_200_OK
    assert response.text == INDEX_HTML


def test_built_assets_are_served_as_files(frontend_client: TestClient) -> None:
    response = frontend_client.get("/assets/app.js")

    assert response.status_code == status.HTTP_200_OK
    assert response.text == SCRIPT_BODY


def test_top_level_static_files_are_served(frontend_client: TestClient) -> None:
    assert frontend_client.get("/favicon.svg").text == "<svg/>"


def test_paths_outside_the_build_folder_are_never_served(frontend_client: TestClient) -> None:
    response = frontend_client.get("/..%2F..%2Fetc%2Fpasswd")

    assert response.text == INDEX_HTML


def test_unknown_api_routes_return_the_json_error_shape(frontend_client: TestClient) -> None:
    response = frontend_client.get(f"{API_V1_PREFIX}/does-not-exist")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["error"]["code"] == ErrorCode.NOT_FOUND


def test_api_still_works_alongside_the_react_app(frontend_client: TestClient) -> None:
    response = frontend_client.get(f"{API_V1_PREFIX}/health")

    assert response.status_code == status.HTTP_200_OK


def test_app_starts_without_a_frontend_build(tmp_path: Path) -> None:
    application = create_app(build_test_settings(frontend_dist_dir=tmp_path / "missing"))

    with TestClient(application) as test_client:
        response = test_client.get("/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["error"]["code"] == ErrorCode.NOT_FOUND
