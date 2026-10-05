# Phase 11: USD insights with fixed exchange rates

## Prompt

> Using TDD, add approximate USD figures to the salary insights, using fixed exchange rates kept in constants with an "as of" date.
> Org-wide USD figures convert each salary before aggregating (`AVG(salary * rate)`), not by averaging per-country results. Add a test with uneven headcounts that proves this.
> Use `Decimal` for rates and round only at the final output.
> Label USD figures in the UI as approximate, with the "as of" date.
> In the same phase, update `docs/requirements.md` (move currency conversion into scope, with the fixed-rate reasoning) and `docs/tradeoffs.md` (fixed vs. live rates).

## Notes

- **Accepted:** rates live in `app/constants/currency_constants.py` as `Decimal` values with `USD_EXCHANGE_RATES_AS_OF`. A test checks that every currency has a positive rate and that USD is 1, so a new currency cannot silently drop out of the USD figures.
- **Accepted:** the repository converts per row with `CASE currency WHEN ... THEN rate END` and aggregates `MIN`, `MAX` and `AVG` of `salary * rate` in SQL, returning unrounded values; the service rounds to cents once.
- **Accepted:** the uneven-headcount test (1 employee at 200 USD, 3 at 100 USD) expects 125.00, not the 150.00 an average of country averages would give. A second test uses salaries whose converted values round differently per row (1.006, 1.006, 1.0001), so rounding before averaging would fail it.
- **Changed:** the service receives its rates and date as constructor arguments (defaulting to the constants), so tests use round rates and their expected values do not change when the real rates are updated. One integration test checks the default wiring uses the constants.
- **Changed:** every `usd` block in the API carries `rates_as_of`, so a USD figure is never shown without its date. The organisation endpoint is USD only, because local currencies cannot be combined.
- **Changed:** declared `app`, `scripts` and `tests` as first-party for Ruff's import sorting, so a red test that imports a module which does not exist yet still passes lint.
- **Rejected:** live rates from an external API. They would make results non-reproducible and add a network dependency; recorded in the trade-offs.
- **Verified on 10,000 seeded rows:** the organisation average from the API (70,837.43 USD) matches an independent SQL query; averaging country averages would give 68,809.30. `/insights/organization` responds in about 5 ms.
