from enum import StrEnum

API_TITLE = "ACME Salary Management API"
API_VERSION = "1.0.0"
API_V1_PREFIX = "/api/v1"

HEALTH_PATH = "/health"
EMPLOYEES_PATH = "/employees"
EMPLOYEE_ID_PATH = "/{employee_id}"
META_PATH = "/meta"
INSIGHTS_PATH = "/insights"

HEALTH_TAG = "health"
EMPLOYEES_TAG = "employees"
META_TAG = "meta"
INSIGHTS_TAG = "insights"


class HealthStatus(StrEnum):
    OK = "ok"
