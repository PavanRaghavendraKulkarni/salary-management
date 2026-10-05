# Phase Prompts

Paste these into your AI coding tool one at a time. Save each prompt you use in `prompts/` with a short note on what you accepted, changed, or rejected from the output.

## Phase 0: Project setup

```
Read CLAUDE.md carefully and follow it for everything in this project.

Set up the project skeleton exactly as the folder structure in CLAUDE.md describes. Do not build any features yet.

Backend: FastAPI app factory in main.py, settings via pydantic-settings, SQLAlchemy database session, constants files with initial values, a GET /api/v1/health endpoint, Ruff and mypy config in pyproject.toml, and one passing integration test for the health endpoint.

Frontend: Vite + React + TypeScript (strict), MUI, React Router with Employees and Insights routes, ESLint, Prettier, Vitest, and one passing smoke test.

Root: README with setup and test commands, .gitignore, and backend/.env.example.

Stop and show me the folder tree, test output, and proposed commit messages.
```

## Phase 1: Requirements and design docs

```
Write docs/requirements.md, maximum one page: goal, user persona, problem, in-scope features, out-of-scope items with the reason for each, assumptions, and success criteria.

Then write docs/design.md: the data model, the API list, each MVC layer's responsibility, and a Mermaid architecture diagram.

Use CLAUDE.md as the source. Keep both documents concise. Do not write any code.
```

## Phase 2: Create and fetch an employee (TDD)

```
Using TDD, implement creating and fetching an employee across all layers: model, views, repository, service, controller, domain exceptions, and exception handlers.

Write these tests first and show me each one failing before you implement it:
- valid create returns 201 with the employee
- duplicate email returns 409
- salary of zero or below returns 422
- currency that does not match the country returns 422
- hire date in the future returns 422
- fetching an unknown id returns 404

All validation limits, allowed values, and messages must come from constants. Stop after this feature.
```

## Phase 3: Update and delete (TDD)

```
Using TDD, add updating and deleting an employee. Tests first: update changes fields and refreshes updated_at, update with a duplicate email returns 409, update of an unknown id returns 404, delete returns 204, and a deleted employee can no longer be fetched.

Reuse the existing validation; do not duplicate it. Stop when done.
```

## Phase 4: List, search, filter, paginate (TDD)

```
Using TDD, implement GET /employees with search by name or email, filters for country, department, and job_title, pagination, and sorting. Add GET /meta/filters.

Tests first: filtering returns only matching rows, search is case-insensitive, pagination returns the correct total and page, page_size above the maximum is rejected, and sorting works in both directions.

All filtering, sorting, and pagination must happen in SQL in the repository. Confirm the indexes from CLAUDE.md exist. Stop when done.
```

## Phase 5: Seed script

```
Write backend/scripts/seed.py to generate 10,000 employees with Faker.

- Use a fixed random seed from constants so the data is the same every run.
- Define realistic salary ranges per country and job title in constants/seed_constants.py, in each country's local currency.
- Insert in batches so the full seed finishes in under 10 seconds.
- Skip seeding if data already exists, unless a --reset flag is passed.

Tests first, using a small count: the correct number of rows is created, every row passes model validation, and the same seed produces the same data. Stop when done.
```

## Phase 6: Salary insights (TDD)

```
Using TDD, implement the three insight endpoints from CLAUDE.md: by country, by job title within a country, and by department within a country.

Tests first, using small hand-built datasets with exact expected values: correct headcount, minimum, maximum, and average per group; an empty result for a country with no employees; and averages rounded to 2 decimal places.

Compute everything with SQL GROUP BY in the repository. Stop when done.
```

## Phase 7: Frontend employees page

```
Build the Employees page following the frontend MVC layers in CLAUDE.md:
- models: Employee types
- services: employeeService using the shared apiClient
- controllers: useEmployees (list, filters, pagination) and useEmployeeForm (create, edit, validation)
- views: EmployeesPage, EmployeeTable, EmployeeFilters, EmployeeFormDialog

Features: a paginated table, search, filter dropdowns, add, edit, and delete with confirmation, loading and error states, and salaries formatted in local currency. All labels, messages, and limits come from constants.

Write Vitest tests for the hooks and the form validation first. Stop when done.
```

## Phase 8: Frontend insights page

```
Build the Insights page: a country summary table, a bar chart of average salary by country (each country in its own currency, so label clearly), and a country selector that shows job title and department breakdowns.

Follow the same MVC layers: insight models, insightService, a useInsights hook, and presentational views. Test the hook first. Stop when done.
```

## Phase 9: Deploy and polish

```
Prepare for deployment on Render as one web service:
- FastAPI serves the built React app and the API.
- On startup, seed the database if it is empty.
- Add a render.yaml or document the build and start commands in the README.

Then finish the docs:
- README: overview, live link placeholder, local setup, how to run tests, project structure, and a note that the free tier takes 30-60 seconds to wake up.
- docs/tradeoffs.md: SQLite vs Postgres, no authentication, local-currency reporting, Decimal for money, SQL aggregation, and pagination limits.

Run all tests and linters and show me the results.
```

## Review prompt (use after every phase)

```
Review the code you just wrote as a strict senior reviewer, checking it against CLAUDE.md:
- layer violations (business logic in controllers, queries outside repositories, API calls in views)
- magic numbers or strings outside the constants folder
- missing or weak tests
- unclear names, duplication, and files that are too long

List every issue you find, then fix them, and run the tests again.
```
