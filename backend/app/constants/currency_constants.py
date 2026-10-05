from datetime import date
from decimal import Decimal

from app.constants.employee_constants import Currency

# Fixed rates make USD figures reproducible; they are approximate and dated, not live.
# Source: ECB euro foreign exchange reference rates, 2 October 2026.
# USD per 1 unit = (USD per EUR) / (currency per EUR), with USD per EUR = 1.1225.
USD_EXCHANGE_RATES_AS_OF = date(2026, 10, 2)

# USD value of one unit of each currency.
USD_EXCHANGE_RATES: dict[Currency, Decimal] = {
    Currency.USD: Decimal("1"),
    Currency.EUR: Decimal("1.1225"),
    Currency.GBP: Decimal("1.320076"),
    Currency.INR: Decimal("0.010382"),
    Currency.CAD: Decimal("0.702265"),
    Currency.AUD: Decimal("0.693929"),
    Currency.SGD: Decimal("0.781359"),
    Currency.JPY: Decimal("0.006342"),
}
