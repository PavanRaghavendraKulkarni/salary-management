from pydantic import BaseModel

from app.constants.api_constants import HealthStatus


class HealthResponse(BaseModel):
    status: HealthStatus
