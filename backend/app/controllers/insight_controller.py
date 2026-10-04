from typing import Annotated

from fastapi import APIRouter, Depends

from app.constants.api_constants import (
    INSIGHTS_COUNTRIES_PATH,
    INSIGHTS_DEPARTMENTS_PATH,
    INSIGHTS_JOB_TITLES_PATH,
    INSIGHTS_PATH,
    INSIGHTS_TAG,
)
from app.constants.employee_constants import Country
from app.dependencies.providers import get_insight_service
from app.services.insight_service import InsightService
from app.views.insight_view import CountryBreakdownResponse, CountryInsight

router = APIRouter(prefix=INSIGHTS_PATH, tags=[INSIGHTS_TAG])
InsightServiceDependency = Annotated[InsightService, Depends(get_insight_service)]


@router.get(INSIGHTS_COUNTRIES_PATH)
def get_country_insights(service: InsightServiceDependency) -> list[CountryInsight]:
    return service.get_country_insights()


@router.get(INSIGHTS_JOB_TITLES_PATH)
def get_job_title_insights(
    country: Country, service: InsightServiceDependency
) -> CountryBreakdownResponse:
    return service.get_job_title_insights(country)


@router.get(INSIGHTS_DEPARTMENTS_PATH)
def get_department_insights(
    country: Country, service: InsightServiceDependency
) -> CountryBreakdownResponse:
    return service.get_department_insights(country)
