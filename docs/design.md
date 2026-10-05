# Design

## Architecture

One deployable service: FastAPI serves the JSON API under `/api/v1` and the built React app for every other path. Both sides follow the same layering, and dependencies only point downwards.

```mermaid
flowchart TD
    subgraph Browser["React app (browser)"]
        V[Views<br/>pages and components] --> C[Controllers<br/>hooks: useEmployees, useEmployeeForm, useInsights]
        C --> S[Services<br/>employeeService, insightService]
        S --> AC[apiClient<br/>shared axios instance]
    end

    AC -- "HTTP JSON /api/v1" --> BC

    subgraph API["FastAPI backend"]
        BC[Controllers<br/>routers] --> BS[Services<br/>business rules]
        BS --> BR[Repositories<br/>SQLAlchemy queries]
        BR --> BM[Models<br/>ORM entities]
        BC -. "request / response" .- BV[Views<br/>Pydantic schemas]
        EH[Exception handlers] -. "domain errors → JSON" .- BC
    end

    BM --> DB[(SQLite)]
```

## Backend layers

| Layer | Folder | Responsibility |
|---|---|---|
| Model | `app/models` | SQLAlchemy entities: table shape and indexes only. |
| View | `app/views` | Pydantic request/response schemas. Field-level validation (types, lengths, ranges, allowed values). |
| Controller | `app/controllers` | Parse the request, call one service method, return a view. |
| Service | `app/services` | Cross-field business rules (currency matches country, hire date not in future, unique email), raising domain exceptions. Returns views. |
| Repository | `app/repositories` | All SQL: CRUD, filtering, sorting, pagination and `GROUP BY` aggregations. |
| Exceptions | `app/exceptions` | Domain exceptions and the central handlers that turn them into `{"error": {"code", "message"}}`. |
| Dependencies | `app/dependencies` | `Depends` providers wiring session → repository → service. |

## Frontend layers

| Layer | Folder | Responsibility |
|---|---|---|
| Model | `src/models` | TypeScript types for API data. |
| Service | `src/services` | API calls through the shared axios client. |
| Controller | `src/controllers` | Hooks holding state, loading and errors, calling services. |
| View | `src/views` | Pages and presentational components; render props, call handlers. |

## Data model

`employees`

| Column | Type | Rules |
|---|---|---|
| `id` | integer PK | |
| `full_name` | varchar(100) | 2–100 characters |
| `email` | varchar(254) | unique, valid format, stored lowercase |
| `job_title` | varchar | allowed list |
| `department` | varchar | allowed list |
| `country` | varchar | allowed list |
| `currency` | char(3) | ISO 4217, must equal the country's currency |
| `annual_gross_salary` | numeric(12, 2) | > 0 |
| `hire_date` | date | not in the future |
| `created_at`, `updated_at` | datetime | set automatically |

Indexes: `country`, `job_title`, `department`, and composite (`country`, `job_title`) for the per-country job-title insight.

Money is `Decimal` end to end and serialised as a decimal **string** in JSON (for example `"85000.00"`), so no precision is lost in transit.

## API (`/api/v1`)

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Service status |
| GET | `/employees` | Paginated list: `search`, `country`, `department`, `job_title`, `page`, `page_size` (default 20, max 100), `sort_by`, `sort_order` |
| GET | `/employees/{id}` | One employee |
| POST | `/employees` | Create (201) |
| PUT | `/employees/{id}` | Replace all editable fields |
| DELETE | `/employees/{id}` | Delete (204) |
| GET | `/meta/filters` | Distinct countries, departments and job titles present in the data |
| GET | `/meta/reference-data` | Allowed values and the country-to-currency mapping for the form |
| GET | `/insights/countries` | Per country: currency, headcount, min, max, average, plus `usd_rate` and approximate `usd` figures |
| GET | `/insights/job-titles?country=` | Per job title within a country, in local currency and approximate USD |
| GET | `/insights/departments?country=` | Per department within a country, in local currency and approximate USD |
| GET | `/insights/organization` | Organisation-wide headcount, min, max, average in approximate USD |

Every `usd` block carries `rates_as_of`, the date of the fixed rates in `app/constants/currency_constants.py`. USD figures are computed in SQL as `MIN`/`MAX`/`AVG(salary * rate)`, with the rate chosen per row by a `CASE` on currency, so each employee weighs the same in the organisation-wide average. Rounding to cents happens once, in the service.

Errors: `404 NOT_FOUND`, `409 DUPLICATE_EMAIL`, `422 VALIDATION_ERROR`, always as `{"error": {"code": "...", "message": "..."}}`.

## Extensibility

- **Bonus or other pay components:** add a `compensation_components` table linked to an employee; insights can then sum components in SQL without changing the employee API.
- **Live or historical exchange rates:** replace the rate constants with an `exchange_rates` table keyed by currency and date. The service already receives its rates and date as constructor arguments, so only the provider changes.
