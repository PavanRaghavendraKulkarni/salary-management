from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.constants.api_constants import EMPLOYEE_ID_PATH, EMPLOYEES_PATH, EMPLOYEES_TAG
from app.dependencies.providers import get_employee_service
from app.services.employee_service import EmployeeService
from app.views.employee_view import EmployeeCreate, EmployeeResponse
from app.views.error_view import ErrorResponse

router = APIRouter(prefix=EMPLOYEES_PATH, tags=[EMPLOYEES_TAG])
EmployeeServiceDependency = Annotated[EmployeeService, Depends(get_employee_service)]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {"model": ErrorResponse}},
)
def create_employee(
    payload: EmployeeCreate, service: EmployeeServiceDependency
) -> EmployeeResponse:
    return service.create_employee(payload)


@router.get(EMPLOYEE_ID_PATH, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}})
def get_employee(employee_id: int, service: EmployeeServiceDependency) -> EmployeeResponse:
    return service.get_employee(employee_id)
