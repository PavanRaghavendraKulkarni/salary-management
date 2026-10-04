from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import SessionFactory
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService


def get_session() -> Iterator[Session]:
    with SessionFactory() as session:
        yield session


def get_employee_repository(
    session: Annotated[Session, Depends(get_session)],
) -> EmployeeRepository:
    return EmployeeRepository(session)


def get_employee_service(
    repository: Annotated[EmployeeRepository, Depends(get_employee_repository)],
) -> EmployeeService:
    return EmployeeService(repository)
