from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.constants.employee_constants import Country, Currency


class UsdSalaryStatistics(BaseModel):
    """Approximate USD figures: each salary is converted at a fixed rate before aggregating."""

    min_salary: Decimal
    max_salary: Decimal
    average_salary: Decimal
    rates_as_of: date


class SalaryStatistics(BaseModel):
    """Salary figures for one group, always in that group's local currency."""

    headcount: int
    min_salary: Decimal
    max_salary: Decimal
    average_salary: Decimal


class CountryInsight(SalaryStatistics):
    country: Country
    currency: Currency
    usd_rate: Decimal
    usd: UsdSalaryStatistics


class GroupInsight(SalaryStatistics):
    """Statistics for one job title or department inside a single country."""

    name: str
    usd: UsdSalaryStatistics


class CountryBreakdownResponse(BaseModel):
    """Groups within one country; the currency is stated once because every group shares it."""

    country: Country
    currency: Currency
    usd_rate: Decimal
    groups: list[GroupInsight]


class OrganizationInsight(BaseModel):
    """Organisation-wide pay, only possible in one currency; `usd` is empty without employees."""

    headcount: int
    usd: UsdSalaryStatistics | None
