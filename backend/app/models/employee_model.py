from datetime import date
from decimal import Decimal

from sqlalchemy import Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.constants.employee_constants import (
    CATEGORY_MAX_LENGTH,
    CURRENCY_CODE_LENGTH,
    EMAIL_MAX_LENGTH,
    FULL_NAME_MAX_LENGTH,
    SALARY_PRECISION,
    SALARY_SCALE,
)
from app.models.base_model import Base, TimestampMixin


class Employee(TimestampMixin, Base):
    """One employee and their current annual gross base salary in local currency."""

    __tablename__ = "employees"
    __table_args__ = (Index("ix_employees_country_job_title", "country", "job_title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(FULL_NAME_MAX_LENGTH))
    email: Mapped[str] = mapped_column(String(EMAIL_MAX_LENGTH), unique=True)
    job_title: Mapped[str] = mapped_column(String(CATEGORY_MAX_LENGTH), index=True)
    department: Mapped[str] = mapped_column(String(CATEGORY_MAX_LENGTH), index=True)
    country: Mapped[str] = mapped_column(String(CATEGORY_MAX_LENGTH), index=True)
    currency: Mapped[str] = mapped_column(String(CURRENCY_CODE_LENGTH))
    annual_gross_salary: Mapped[Decimal] = mapped_column(Numeric(SALARY_PRECISION, SALARY_SCALE))
    hire_date: Mapped[date]
