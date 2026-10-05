# Trade-offs

Each decision below names what was chosen, what it costs, and when to revisit it.

## SQLite instead of PostgreSQL

SQLite needs no server, makes tests fast (in-memory, isolated per test) and is ample for 10,000 rows: a filtered, sorted page returns in about 10 ms and the country insight in about 7 ms locally. The cost is that it allows only one writer at a time, and on Render's free tier the file is lost on every redeploy. The app re-seeds itself in that case. SQLAlchemy keeps the code portable, so switching is a change of `DATABASE_URL` plus a managed Postgres instance.

## No authentication

HR salary data is sensitive, so a real deployment must have authentication and role-based access. It was left out on purpose to keep the exercise focused on the salary workflows. It would sit in front of every route as a FastAPI dependency, without changing services or repositories.

## Local currency first, USD as an approximate view

Each salary is stored in the currency of its country, and every per-country statistic is exact in that currency. For comparisons across countries, and for the organisation-wide view, the insights also show USD figures. Each salary is converted before aggregating (`AVG(salary * rate)` in SQL): averaging the per-country averages instead would weigh a country of 300 people the same as one of 3,000. The chart stays in local currency because it compares job titles within one country.

## Fixed exchange rates instead of live rates

USD rates are `Decimal` constants with an "as of" date (`app/constants/currency_constants.py`), and the date is shown next to every USD figure. They are derived from the ECB euro foreign exchange reference rates of 2 October 2026: USD per unit = (USD per EUR) / (currency per EUR), with USD per EUR = 1.1225. Fixed rates make results reproducible, so a figure in a report can be checked later and tests can assert exact values. They also avoid a network dependency, an API key and failure handling for a rate provider. The cost is that USD figures drift from reality as rates move, so they are labelled approximate and the constants need an occasional update. If HR needs current or historical rates, the next step is an `exchange_rates` table keyed by currency and date, refreshed from a provider, with the reporting date as a query parameter.

Rates and the final figures are `Decimal`, and rounding happens once, after aggregation. SQLite still computes `salary * rate` and `AVG` in double precision, which is far below a cent at this scale; PostgreSQL `NUMERIC` would make the arithmetic exact as well.

## Decimal for money

Salaries are `Decimal` in Python, `NUMERIC(12, 2)` in the database and decimal **strings** in JSON (`"85000.00"`). Floats cannot represent most cents exactly, and a JSON number can be silently rounded by clients. The cost is that the frontend converts to a number for display only. SQLite stores numerics with float affinity, which is exact for values of this size; Postgres would store them exactly.

## Aggregation in SQL

Headcount, minimum, maximum and average are computed with `GROUP BY` in the database, so Python never loads 10,000 rows to calculate a statistic. Averages are rounded in SQL and then quantized to cents. Indexes on `country`, `job_title`, `department` and (`country`, `job_title`) support the filters and the per-country breakdown.

## Pagination limits

Every employee list request is paginated: default 20, maximum 100 rows, enforced by the API with a 422 above the limit. This keeps responses small and stops a client from requesting every record at once. Insight endpoints are not paginated, because they return one row per group (at most 12 job titles or 9 countries).

## Validation in two places

Field rules (lengths, allowed values, salary > 0) are on the Pydantic request views; cross-field and database rules (currency matches country, hire date not in the future, unique email) are in the service. The frontend mirrors the rules for instant feedback, but the backend remains the authority. The cost is that limits are defined in both `constants` folders; allowed values come from `GET /meta/reference-data`, so they exist only once.

## Fixed reference lists in code

Countries, currencies, departments and job titles are enums in backend constants. This keeps validation simple and type-checked. Adding a new country or job title needs a code change and a deploy rather than an admin screen. If HR needs to manage these lists, they would move to database tables.

## Tables created at start-up, no migration tool

The schema is one table, so `create_all` is enough. It runs when the app starts (so the API works on an empty database before any seed) and again in the seed script. Once the schema starts changing in production, Alembic migrations should replace it. Renaming `annual_salary` to `annual_gross_salary` showed the cost: `create_all` does not alter an existing table, so a local database has to be deleted and re-seeded. That was acceptable here because the data is seeded and the free-tier database is recreated on every deploy.

## Hard delete

Deleting an employee removes the row. Audit history is out of scope; `created_at` and `updated_at` cover basic tracking. A soft delete or an audit log would be the next step if HR needs to recover records.

## Red test commits in the history

Each behaviour is committed as a failing `test:` commit followed immediately by the commit that makes it pass, so the history shows the tests were written first. The cost is that the red commit alone does not pass its tests, which matters for `git bisect` or a checkout of that exact commit. To contain this, every other commit must pass all tests, a red commit is always followed directly by its green commit, and the two are always pushed together.

## Unexpected errors logged twice

Unexpected errors are logged twice in production, once by our 500 handler (with the request method and path) and once by uvicorn, because Starlette re-raises after the handler responds; this is accepted to keep the default server behaviour.
