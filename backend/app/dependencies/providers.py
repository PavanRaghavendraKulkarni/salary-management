from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import SessionFactory
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.salary_insight_repository import SalaryInsightRepository
from app.services.employee_service import EmployeeService
from app.services.insight_service import InsightService


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


def get_salary_insight_repository(
    session: Annotated[Session, Depends(get_session)],
) -> SalaryInsightRepository:
    return SalaryInsightRepository(session)


def get_insight_service(
    repository: Annotated[SalaryInsightRepository, Depends(get_salary_insight_repository)],
) -> InsightService:
    return InsightService(repository)
