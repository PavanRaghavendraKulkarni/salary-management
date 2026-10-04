from fastapi import status
from fastapi.testclient import TestClient

from app.constants.api_constants import API_V1_PREFIX, HEALTH_PATH, HealthStatus


def test_health_check_reports_service_is_ok(client: TestClient) -> None:
    response = client.get(f"{API_V1_PREFIX}{HEALTH_PATH}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": HealthStatus.OK.value}
