# Salary Management System: Engineering Instructions

## Context

You are a senior software engineer building an employee salary management web app for ACME, an organization with 10,000 employees across multiple countries. The user is an HR Manager who manages salaries in Excel today. They need to view, add, edit, and delete employee salary records, and answer questions about how the organization pays people.

This is a take-home assessment for Incubyte, a software craft consultancy. Reviewers value clean and maintainable code, meaningful tests written test-first, small incremental commits, thoughtful design decisions, and good engineering judgment over complexity.

## Tech stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (typed ORM), Pydantic v2, pydantic-settings, SQLite
- **Backend tooling:** pytest, pytest-cov, httpx (TestClient), Faker, Ruff (lint and format), mypy
- **Frontend:** React 18 + TypeScript (strict), Vite, MUI, React Router, Recharts, axios
- **Frontend tooling:** Vitest, React Testing Library, ESLint, Prettier
- **Deployment:** one Render web service where FastAPI serves the built React app

Do not add libraries beyond this list without asking me first and explaining why.

## Architecture: strict MVC with thin controllers

### Backend layers

- **Model** (`app/models/`): SQLAlchemy ORM entities. Data shape only. No business logic, no HTTP.
- **View** (`app/views/`): Pydantic request and response schemas. They define exactly what the API accepts and returns. Never return ORM objects directly from a controller.
- **Controller** (`app/controllers/`): FastAPI routers. Parse the request, call one service method, return a view. No business logic and no database queries.
- **Service** (`app/services/`): business rules and validation. Raises domain exceptions and knows nothing about HTTP.
- **Repository** (`app/repositories/`): all database queries. The only layer that touches the SQLAlchemy session.

Dependency direction is always controller, then service, then repository, then model. Never skip or reverse a layer. Wire layers together with FastAPI `Depends` in `app/dependencies/`.

### Frontend layers

- **Model** (`src/models/`): TypeScript types and interfaces for API data.
- **View** (`src/views/`): pages and presentational components. They render props and call handlers; they never call the API directly.
- **Controller** (`src/controllers/`): custom hooks such as `useEmployees` that hold state, handle loading and errors, and call services.
- **Service** (`src/services/`): API calls only, through one shared axios client.

## Folder structure

Follow this structure exactly. Ask before adding new top-level folders.

```
salary-management/
|-- CLAUDE.md
|-- README.md
|-- docs/
|   |-- requirements.md
|   |-- design.md
|   |-- tradeoffs.md
|-- prompts/
|-- backend/
|   |-- app/
|   |   |-- main.py
|   |   |-- config/
|   |   |   |-- settings.py
|   |   |   |-- database.py
|   |   |-- constants/
|   |   |   |-- api_constants.py
|   |   |   |-- employee_constants.py
|   |   |   |-- pagination_constants.py
|   |   |   |-- message_constants.py
|   |   |   |-- seed_constants.py
|   |   |   |-- currency_constants.py
|   |   |-- models/
|   |   |   |-- base_model.py
|   |   |   |-- employee_model.py
|   |   |-- views/
|   |   |   |-- employee_view.py
|   |   |   |-- insight_view.py
|   |   |   |-- pagination_view.py
|   |   |   |-- error_view.py
|   |   |-- controllers/
|   |   |   |-- health_controller.py
|   |   |   |-- employee_controller.py
|   |   |   |-- meta_controller.py
|   |   |   |-- insight_controller.py
|   |   |-- services/
|   |   |   |-- employee_service.py
|   |   |   |-- insight_service.py
|   |   |-- repositories/
|   |   |   |-- employee_repository.py
|   |   |   |-- salary_insight_repository.py
|   |   |-- exceptions/
|   |   |   |-- domain_exceptions.py
|   |   |   |-- exception_handlers.py
|   |   |-- dependencies/
|   |       |-- providers.py
|   |-- scripts/
|   |   |-- seed.py
|   |-- tests/
|   |   |-- conftest.py
|   |   |-- factories.py
|   |   |-- unit/
|   |   |-- integration/
|   |-- pyproject.toml
|   |-- .env.example
|-- frontend/
    |-- src/
    |   |-- constants/
    |   |   |-- apiConstants.ts
    |   |   |-- routeConstants.ts
    |   |   |-- messageConstants.ts
    |   |   |-- paginationConstants.ts
    |   |-- models/
    |   |   |-- employee.ts
    |   |   |-- insight.ts
    |   |-- services/
    |   |   |-- apiClient.ts
    |   |   |-- employeeService.ts
    |   |   |-- insightService.ts
    |   |-- controllers/
    |   |   |-- useEmployees.ts
    |   |   |-- useEmployeeForm.ts
    |   |   |-- useInsights.ts
    |   |-- views/
    |   |   |-- pages/
    |   |   |   |-- EmployeesPage.tsx
    |   |   |   |-- InsightsPage.tsx
    |   |   |-- components/
    |   |       |-- EmployeeTable.tsx
    |   |       |-- EmployeeFormDialog.tsx
    |   |       |-- EmployeeFilters.tsx
    |   |       |-- SalaryStatsTable.tsx
    |   |       |-- SalaryChart.tsx
    |   |-- utils/
    |   |   |-- formatCurrency.ts
    |   |-- App.tsx
    |   |-- main.tsx
    |-- tests/
    |-- package.json
```

## Constants

- Every fixed value lives in a `constants/` folder: API prefix and route paths, pagination defaults and limits, validation limits (name length, minimum and maximum salary), allowed values (countries, currencies, departments, job titles), the country-to-currency mapping, error and success messages, and seed settings.
- No magic numbers or hard-coded strings in models, views, services, controllers, components, or hooks. Import them from constants.
- One file per topic. Use UPPER_SNAKE_CASE names. In Python, use `Enum` for fixed sets such as currencies. In TypeScript, use `as const` objects and union types.
- Environment-specific values (database URL, CORS origins, environment name) are not constants. They belong in `app/config/settings.py` via pydantic-settings, read from `.env`, with `.env.example` committed.

## Data model

Employee:

- `id`: integer primary key
- `full_name`: required, 2 to 100 characters
- `email`: required, unique, valid email format
- `job_title`: required, from the allowed list in constants
- `department`: required, from the allowed list in constants
- `country`: required, from the allowed list in constants
- `currency`: ISO 4217 code; must match the country, using the country-to-currency mapping in constants
- `annual_gross_salary`: Decimal(12, 2), greater than zero, in the country's local currency
- `hire_date`: date, not in the future
- `created_at`, `updated_at`: timestamps set automatically

Add database indexes on `country`, `job_title`, `department`, and a composite index on (`country`, `job_title`).

**Confirmed decisions:** salary means the annual gross base salary of a full-time employee; bonus, deductions and equity are out of scope. Salaries are stored in local currency. Insights also show approximate USD figures using fixed exchange rates from `currency_constants.py` with an "as of" date, converting each salary before aggregating. Keep the design open so bonus components or live rates can be added later without a rewrite.

## API (prefix `/api/v1`)

- `GET /health`: service status
- `GET /employees`: query params `search` (name or email), `country`, `department`, `job_title`, `page`, `page_size` (default 20, max 100), `sort_by`, `sort_order`. Returns `items`, `total`, `page`, `page_size`.
- `GET /employees/{id}`: one employee
- `POST /employees`: create, returns 201
- `PUT /employees/{id}`: update
- `DELETE /employees/{id}`: delete, returns 204
- `GET /meta/filters`: distinct countries, departments, and job titles for dropdowns
- `GET /insights/countries`: per country: headcount, currency, minimum, maximum, and average salary
- `GET /insights/job-titles?country=`: per job title within a country: headcount, minimum, maximum, average
- `GET /insights/departments?country=`: the same, per department
- `GET /insights/organization`: organisation-wide headcount, minimum, maximum, and average salary in approximate USD, converting each salary at fixed dated rates before aggregating

Errors use one JSON shape, produced by central exception handlers: `{"error": {"code": "...", "message": "..."}}`. Use 404 for not found, 409 for a duplicate email, 422 for validation errors, and 500 `INTERNAL_ERROR` for anything unexpected: log the traceback and return a generic message from constants, never internal details.

## Coding standards

- Type hints everywhere and mypy clean. TypeScript strict mode with no `any`.
- Small, single-purpose functions with descriptive names. No unclear abbreviations.
- Docstrings on public classes and service methods that explain why, not what.
- No commented-out code, no print statements, no unused imports. Ruff, ESLint, and Prettier must pass.
- Do aggregations in SQL with `GROUP BY`. Never load all rows into Python to compute statistics.
- Paginate every list endpoint. Never return all 10,000 rows.
- Keep files focused. If a file grows past about 200 lines, propose a split.

## Testing (TDD)

- Follow red, green, refactor: write a failing test first, write the minimum code to pass it, then refactor.
- Unit tests for services; integration tests for controllers using FastAPI's TestClient.
- Tests use in-memory SQLite (StaticPool) and FastAPI dependency overrides. No network calls, no shared state between tests, no sleeps, and no random data without a fixed seed.
- Name tests by behavior, for example `test_create_employee_rejects_duplicate_email`.
- Insight tests use small hand-built datasets so the expected numbers are exact.
- Frontend: test key hooks and components with Vitest and React Testing Library, mocking the service layer.
- All tests must pass at every commit, except a deliberate red `test:` commit. That commit must be immediately followed by the commit that makes it pass, and must never be pushed alone.

## Git workflow

- Small commits, one logical change each, using Conventional Commits: `test:`, `feat:`, `refactor:`, `fix:`, `docs:`, `chore:`.
- Where practical, commit the failing test and the implementation separately.
- Never commit secrets, `.env`, database files, `node_modules`, or build output.

## How to work with me

- Work one phase at a time. At the end of each phase, stop and give me: a summary of what you did, the files changed, the test results, and proposed commit messages. Wait for my approval before continuing.
- If something is ambiguous, ask instead of guessing. Record any assumption you make in `docs/requirements.md`.
- Prefer the simplest solution that meets the requirement.
- Out of scope, do not build: authentication and roles, multi-tenancy, payroll processing, tax calculation, Excel import or export, audit history.
- When you make a design choice, explain the trade-off in two or three sentences so I can record it in `docs/tradeoffs.md`.
