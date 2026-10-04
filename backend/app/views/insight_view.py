from decimal import Decimal

from pydantic import BaseModel

from app.constants.employee_constants import Country, Currency


class SalaryStatistics(BaseModel):
    """Salary figures for one group, always in that group's local currency."""

    headcount: int
    min_salary: Decimal
    max_salary: Decimal
    average_salary: Decimal


class CountryInsight(SalaryStatistics):
    country: Country
    currency: Currency


class GroupInsight(SalaryStatistics):
    """Statistics for one job title or department inside a single country."""

    name: str


class CountryBreakdownResponse(BaseModel):
    """Groups within one country; the currency is stated once because every group shares it."""

    country: Country
    currency: Currency
    groups: list[GroupInsight]
