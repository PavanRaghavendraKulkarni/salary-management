from fastapi import APIRouter

from app.constants.api_constants import HEALTH_PATH, HEALTH_TAG, HealthStatus
from app.views.health_view import HealthResponse

router = APIRouter(tags=[HEALTH_TAG])


@router.get(HEALTH_PATH, response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status=HealthStatus.OK)
