from pydantic import BaseModel

from app.constants.employee_constants import Country, Currency, Department, JobTitle


class FilterOptionsResponse(BaseModel):
    """Values that currently exist in the data, so filter dropdowns never offer empty results."""

    countries: list[str]
    departments: list[str]
    job_titles: list[str]


class CountryOption(BaseModel):
    name: Country
    currency: Currency


class ReferenceDataResponse(BaseModel):
    """Every allowed value, so the form can offer choices the data does not contain yet."""

    countries: list[CountryOption]
    departments: list[Department]
    job_titles: list[JobTitle]
