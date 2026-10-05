from collections.abc import Mapping
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from app.constants.currency_constants import USD_EXCHANGE_RATES, USD_EXCHANGE_RATES_AS_OF
from app.constants.employee_constants import COUNTRY_CURRENCY, SALARY_QUANTUM, Country, Currency
from app.repositories.salary_insight_repository import (
    SalaryAggregate,
    SalaryInsightRepository,
    UsdAggregate,
)
from app.views.insight_view import (
    CountryBreakdownResponse,
    CountryInsight,
    GroupInsight,
    OrganizationInsight,
    UsdSalaryStatistics,
)


class InsightService:
    """Salary statistics in each country's local currency, plus approximate USD figures.

    Local figures are exact. USD figures use fixed, dated rates so they are reproducible,
    and convert each salary before aggregating so every employee carries the same weight.
    """

    def __init__(
        self,
        repository: SalaryInsightRepository,
        usd_rates: Mapping[Currency, Decimal] = USD_EXCHANGE_RATES,
        rates_as_of: date = USD_EXCHANGE_RATES_AS_OF,
    ) -> None:
        self._repository = repository
        self._usd_rates = usd_rates
        self._rates_as_of = rates_as_of

    def get_country_insights(self) -> list[CountryInsight]:
        return [
            CountryInsight(
                country=Country(aggregate.group),
                currency=aggregate.currency,
                usd_rate=self._usd_rates[Currency(aggregate.currency)],
                usd=self._usd_statistics(aggregate.usd),
                **self._statistics(aggregate),
            )
            for aggregate in self._repository.salary_stats_by_country(self._usd_rates)
        ]

    def get_job_title_insights(self, country: Country) -> CountryBreakdownResponse:
        return self._breakdown(
            country, self._repository.salary_stats_by_job_title(country, self._usd_rates)
        )

    def get_department_insights(self, country: Country) -> CountryBreakdownResponse:
        return self._breakdown(
            country, self._repository.salary_stats_by_department(country, self._usd_rates)
        )

    def get_organization_insight(self) -> OrganizationInsight:
        """Only meaningful in one currency, so the organisation-wide view is USD only."""
        aggregate = self._repository.organization_salary_stats(self._usd_rates)
        return OrganizationInsight(
            headcount=aggregate.headcount,
            usd=self._usd_statistics(aggregate.usd) if aggregate.usd else None,
        )

    def _breakdown(
        self, country: Country, aggregates: list[SalaryAggregate]
    ) -> CountryBreakdownResponse:
        """The currency comes from the mapping so an empty country still reports one."""
        currency = COUNTRY_CURRENCY[country]
        return CountryBreakdownResponse(
            country=country,
            currency=currency,
            usd_rate=self._usd_rates[currency],
            groups=[
                GroupInsight(
                    name=aggregate.group,
                    usd=self._usd_statistics(aggregate.usd),
                    **self._statistics(aggregate),
                )
                for aggregate in aggregates
            ],
        )

    def _usd_statistics(self, usd: UsdAggregate) -> UsdSalaryStatistics:
        return UsdSalaryStatistics(
            min_salary=_to_cents(usd.min_salary),
            max_salary=_to_cents(usd.max_salary),
            average_salary=_to_cents(usd.average_salary),
            rates_as_of=self._rates_as_of,
        )

    @staticmethod
    def _statistics(aggregate: SalaryAggregate) -> dict[str, int | Decimal]:
        return {
            "headcount": aggregate.headcount,
            "min_salary": _to_cents(aggregate.min_salary),
            "max_salary": _to_cents(aggregate.max_salary),
            "average_salary": _to_cents(aggregate.average_salary),
        }


def _to_cents(amount: Decimal) -> Decimal:
    return amount.quantize(SALARY_QUANTUM, ROUND_HALF_UP)
