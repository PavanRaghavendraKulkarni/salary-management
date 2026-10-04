from collections.abc import Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee_model import Employee


class EmployeeRepository:
    """All employee persistence lives here so services never build SQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, values: Mapping[str, Any]) -> Employee:
        employee = Employee(**values)
        self._session.add(employee)
        self._session.commit()
        self._session.refresh(employee)
        return employee

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self._session.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return self._session.scalars(select(Employee).where(Employee.email == email)).first()

    def update(self, employee: Employee, values: Mapping[str, Any]) -> Employee:
        for field, value in values.items():
            setattr(employee, field, value)
        self._session.commit()
        self._session.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self._session.delete(employee)
        self._session.commit()
