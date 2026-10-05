from decimal import Decimal

from app.constants.currency_constants import USD_EXCHANGE_RATES
from app.constants.employee_constants import Currency


def test_every_currency_has_a_positive_decimal_usd_rate() -> None:
    assert set(USD_EXCHANGE_RATES) == set(Currency)
    assert all(isinstance(rate, Decimal) and rate > 0 for rate in USD_EXCHANGE_RATES.values())


def test_usd_converts_to_itself_at_one() -> None:
    assert USD_EXCHANGE_RATES[Currency.USD] == Decimal("1")
