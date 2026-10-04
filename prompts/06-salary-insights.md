# Phase 6: Salary insights (TDD)

## Prompt

> Using TDD, implement `GET /insights/countries`, `GET /insights/job-titles?country=` and `GET /insights/departments?country=`.
> Tests first with a small hand-built dataset whose expected numbers are worked out by hand: exact headcount, minimum, maximum and average per group; an empty result for a country without employees (still reporting that country's currency); averages rounded to 2 decimal places; a missing or unknown country returns 422.
> Compute every statistic with SQL `GROUP BY` in the repository.

## Notes

- **Accepted:** one private repository method builds the `GROUP BY` for any column, so the three insights share one query shape.
- **Accepted:** the dataset is documented in the factory docstring (for example India's average 3,200,000 / 3 = 1,066,666.67) so a reviewer can check the expected values.
- **Changed:** the breakdown response states `country` and `currency` once, with a `groups` list, instead of repeating the currency on every row.
- **Changed:** averages are rounded in SQL (`ROUND(AVG(...), 2)`) and then quantized to cents in the service, so the JSON always has exactly two decimals (`"700000.00"`).
- **Rejected:** a cross-country "global average". Without exchange rates it would mix currencies and mislead. Recorded in the trade-offs.
- **Rejected:** paginating insight responses. They return one row per group (12 job titles at most), so pagination would only add friction.
