from typing import Annotated

from fastapi import APIRouter, Depends

from app.constants.api_constants import (
    META_FILTERS_PATH,
    META_PATH,
    META_REFERENCE_DATA_PATH,
    META_TAG,
)
from app.dependencies.providers import get_employee_service
from app.services.employee_service import EmployeeService
from app.views.meta_view import FilterOptionsResponse, ReferenceDataResponse

router = APIRouter(prefix=META_PATH, tags=[META_TAG])
EmployeeServiceDependency = Annotated[EmployeeService, Depends(get_employee_service)]


@router.get(META_FILTERS_PATH)
def get_filter_options(service: EmployeeServiceDependency) -> FilterOptionsResponse:
    return service.get_filter_options()


@router.get(META_REFERENCE_DATA_PATH)
def get_reference_data(service: EmployeeServiceDependency) -> ReferenceDataResponse:
    return service.get_reference_data()
