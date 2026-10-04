from decimal import ROUND_HALF_UP, Decimal

from app.constants.employee_constants import COUNTRY_CURRENCY, SALARY_QUANTUM, Country
from app.repositories.employee_repository import EmployeeRepository, SalaryAggregate
from app.views.insight_view import CountryBreakdownResponse, CountryInsight, GroupInsight


class InsightService:
    """Salary statistics reported per country in local currency, since currencies don't mix.

    Totals across countries would need exchange rates, which are out of scope for now.
    """

    def __init__(self, repository: EmployeeRepository) -> None:
        self._repository = repository

    def get_country_insights(self) -> list[CountryInsight]:
        return [
            CountryInsight(
                country=Country(aggregate.group),
                currency=aggregate.currency,
                **self._statistics(aggregate),
            )
            for aggregate in self._repository.salary_stats_by_country()
        ]

    def get_job_title_insights(self, country: Country) -> CountryBreakdownResponse:
        return self._breakdown(country, self._repository.salary_stats_by_job_title(country))

    def get_department_insights(self, country: Country) -> CountryBreakdownResponse:
        return self._breakdown(country, self._repository.salary_stats_by_department(country))

    def _breakdown(
        self, country: Country, aggregates: list[SalaryAggregate]
    ) -> CountryBreakdownResponse:
        """The currency comes from the mapping so an empty country still reports one."""
        return CountryBreakdownResponse(
            country=country,
            currency=COUNTRY_CURRENCY[country],
            groups=[
                GroupInsight(name=aggregate.group, **self._statistics(aggregate))
                for aggregate in aggregates
            ],
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
