from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from app.constants.api_constants import EMPLOYEE_ID_PATH, EMPLOYEES_PATH, EMPLOYEES_TAG
from app.dependencies.providers import get_employee_service
from app.services.employee_service import EmployeeService
from app.views.employee_view import (
    EmployeeCreate,
    EmployeeListQuery,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.views.error_view import ErrorResponse
from app.views.pagination_view import PaginatedResponse

router = APIRouter(prefix=EMPLOYEES_PATH, tags=[EMPLOYEES_TAG])
EmployeeServiceDependency = Annotated[EmployeeService, Depends(get_employee_service)]


@router.get("")
def list_employees(
    query: Annotated[EmployeeListQuery, Query()], service: EmployeeServiceDependency
) -> PaginatedResponse[EmployeeResponse]:
    return service.list_employees(query)


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


@router.put(
    EMPLOYEE_ID_PATH,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse},
    },
)
def update_employee(
    employee_id: int, payload: EmployeeUpdate, service: EmployeeServiceDependency
) -> EmployeeResponse:
    return service.update_employee(employee_id, payload)


@router.delete(
    EMPLOYEE_ID_PATH,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}},
)
def delete_employee(employee_id: int, service: EmployeeServiceDependency) -> Response:
    service.delete_employee(employee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
