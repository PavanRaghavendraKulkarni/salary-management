# Trade-offs

Each decision below names what was chosen, what it costs, and when to revisit it.

## SQLite instead of PostgreSQL

SQLite needs no server, makes tests fast (in-memory, isolated per test) and is ample for 10,000 rows: a filtered, sorted page returns in about 10 ms and the country insight in about 7 ms locally. The cost is that it allows only one writer at a time, and on Render's free tier the file is lost on every redeploy. The app re-seeds itself in that case. SQLAlchemy keeps the code portable, so switching is a change of `DATABASE_URL` plus a managed Postgres instance.

## No authentication

HR salary data is sensitive, so a real deployment must have authentication and role-based access. It was left out on purpose to keep the exercise focused on the salary workflows. It would sit in front of every route as a FastAPI dependency, without changing services or repositories.

## Salaries reported per country, in local currency

Each employee's salary is stored in the currency of their country, and every statistic is reported per country. Cross-country totals or averages would need exchange rates (and a decision on which date's rates), and mixing currencies would give misleading numbers. The chart therefore compares job titles *within* one country. Adding conversion later means an exchange-rate table and an optional `reporting_currency` parameter on the insight endpoints.

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

The schema is one table, so `create_all` at seed time is enough. Once the schema starts changing in production, Alembic migrations should replace it.

## Hard delete

Deleting an employee removes the row. Audit history is out of scope; `created_at` and `updated_at` cover basic tracking. A soft delete or an audit log would be the next step if HR needs to recover records.
