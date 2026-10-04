from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy import ColumnElement, Select, delete, func, insert, or_, select
from sqlalchemy.orm import InstrumentedAttribute, Session

from app.constants.employee_constants import EmployeeSortField
from app.constants.pagination_constants import SortOrder
from app.models.employee_model import Employee

SORTABLE_COLUMNS: dict[EmployeeSortField, InstrumentedAttribute[Any]] = {
    EmployeeSortField.FULL_NAME: Employee.full_name,
    EmployeeSortField.EMAIL: Employee.email,
    EmployeeSortField.JOB_TITLE: Employee.job_title,
    EmployeeSortField.DEPARTMENT: Employee.department,
    EmployeeSortField.COUNTRY: Employee.country,
    EmployeeSortField.ANNUAL_SALARY: Employee.annual_salary,
    EmployeeSortField.HIRE_DATE: Employee.hire_date,
}


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

    def find_page(
        self,
        *,
        search: str | None,
        country: str | None,
        department: str | None,
        job_title: str | None,
        sort_by: EmployeeSortField,
        sort_order: SortOrder,
        offset: int,
        limit: int,
    ) -> tuple[list[Employee], int]:
        """Filter, count, sort and slice in SQL so only one page of rows is ever loaded."""
        conditions = self._filter_conditions(search, country, department, job_title)
        total = self._session.scalar(select(func.count(Employee.id)).where(*conditions)) or 0
        statement = self._ordered(select(Employee).where(*conditions), sort_by, sort_order)
        employees = self._session.scalars(statement.offset(offset).limit(limit)).all()
        return list(employees), total

    def distinct_countries(self) -> list[str]:
        return self._distinct_values(Employee.country)

    def distinct_departments(self) -> list[str]:
        return self._distinct_values(Employee.department)

    def distinct_job_titles(self) -> list[str]:
        return self._distinct_values(Employee.job_title)

    def _distinct_values(self, column: InstrumentedAttribute[str]) -> list[str]:
        return list(self._session.scalars(select(column).distinct().order_by(column)).all())

    @staticmethod
    def _filter_conditions(
        search: str | None, country: str | None, department: str | None, job_title: str | None
    ) -> list[ColumnElement[bool]]:
        conditions: list[ColumnElement[bool]] = []
        if search:
            conditions.append(
                or_(
                    Employee.full_name.icontains(search, autoescape=True),
                    Employee.email.icontains(search, autoescape=True),
                )
            )
        if country:
            conditions.append(Employee.country == country)
        if department:
            conditions.append(Employee.department == department)
        if job_title:
            conditions.append(Employee.job_title == job_title)
        return conditions

    @staticmethod
    def _ordered(
        statement: Select[Employee], sort_by: EmployeeSortField, sort_order: SortOrder
    ) -> Select[Employee]:
        column = SORTABLE_COLUMNS[sort_by]
        primary = column.desc() if sort_order == SortOrder.DESC else column.asc()
        return statement.order_by(primary, Employee.id.asc())

    def count_all(self) -> int:
        return self._session.scalar(select(func.count(Employee.id))) or 0

    def bulk_create(self, rows: Sequence[Mapping[str, Any]]) -> None:
        """One multi-row INSERT per call; far faster than adding ORM objects one by one."""
        self._session.execute(insert(Employee), list(rows))
        self._session.commit()

    def delete_all(self) -> None:
        self._session.execute(delete(Employee))
        self._session.commit()
