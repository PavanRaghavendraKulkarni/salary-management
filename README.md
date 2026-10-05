# ACME Salary Management

A web app for ACME's HR team to manage salary records for 10,000 employees across nine countries, and to see how the organisation pays people.

- **Employees:** search by name or email, filter by country, department and job title, sort any column, page through results, and add, edit or delete employees with validation.
- **Insights:** headcount and minimum, average and maximum annual gross salary per country in local currency, with job title and department breakdowns and a chart for the selected country. Approximate USD figures, converted at fixed dated rates, allow comparison across countries and give an organisation-wide view.

- **Live app:** https://acme-salary-management-8yz1.onrender.com
- **API docs:** https://acme-salary-management-8yz1.onrender.com/docs
- **Demo video:** VIDEO_LINK_HERE

> The app runs on Render's free tier, which sleeps when idle. The first request after a pause can take **30–60 seconds** while it wakes up and, if the database was reset, re-seeds 10,000 employees.

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, pydantic-settings, SQLite |
| Frontend | React 18, TypeScript (strict), Vite, MUI, React Router, Recharts, axios |
| Quality | pytest, pytest-cov, Ruff, mypy (strict); Vitest, React Testing Library, ESLint, Prettier |
| Deploy | One Render web service: FastAPI serves the API and the built React app |

## Run locally

Prerequisites: Python 3.12 with [uv](https://docs.astral.sh/uv/), and Node.js 20+.

```bash
# Backend: http://localhost:8000 (API docs at /docs)
cd backend
cp .env.example .env
uv sync
uv run python -m scripts.seed            # creates tables and 10,000 employees; --reset to start over
uv run uvicorn app.main:app --reload

# Frontend: http://localhost:5173 (forwards /api to the backend)
cd frontend
npm install
npm run dev
```

To run it as it runs in production, build the frontend (`npm run build`) and open http://localhost:8000; FastAPI serves `frontend/dist` when it exists.

## Tests and checks

```bash
cd backend
uv run pytest --cov=app                  # unit and integration tests with coverage
uv run ruff check . && uv run ruff format --check .
uv run mypy

cd frontend
npm test
npm run lint && npm run format:check
npm run build                            # includes the TypeScript type check
```

## Deploy to Render

`render.yaml` describes the service. In Render choose **New → Blueprint**, select this repository and deploy. It:

1. builds the React app and installs the backend with `uv`;
2. on start, seeds the database if it is empty, then runs uvicorn;
3. checks health at `/api/v1/health`.

## API

All endpoints are under `/api/v1`; interactive documentation is at `/docs`.

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Service status |
| GET | `/employees` | Paginated list with `search`, `country`, `department`, `job_title`, `page`, `page_size` (≤ 100), `sort_by`, `sort_order` |
| GET / PUT / DELETE | `/employees/{id}` | Fetch, replace or delete one employee |
| POST | `/employees` | Create an employee (201) |
| GET | `/meta/filters` | Values present in the data, for filter dropdowns |
| GET | `/meta/reference-data` | Allowed values and each country's currency, for the form |
| GET | `/insights/countries` | Statistics per country |
| GET | `/insights/job-titles?country=` | Statistics per job title in one country |
| GET | `/insights/departments?country=` | Statistics per department in one country |
| GET | `/insights/organization` | Organisation-wide statistics in approximate USD |

Errors always look like `{"error": {"code": "...", "message": "..."}}`: 404 not found, 409 duplicate email, 422 invalid input, and 500 `INTERNAL_ERROR` with a generic message for anything unexpected (the traceback is logged on the server, never sent to the client).

## Project structure

```
backend/
  app/
    controllers/   FastAPI routers: parse the request, call one service method
    services/      business rules (currency matches country, unique email, ...)
    repositories/  every SQL query: filtering, paging, GROUP BY aggregations
    models/        SQLAlchemy entities
    views/         Pydantic request and response schemas
    exceptions/    domain exceptions and central error handlers
    constants/     limits, allowed values, messages, seed settings
    config/        environment settings and database session
  scripts/seed.py  deterministic 10,000-employee seed
  tests/           unit (services, seed) and integration (HTTP) tests
frontend/
  src/
    models/        API types
    services/      API calls through one axios client
    controllers/   hooks: useEmployees, useEmployeeForm, useInsights
    views/         pages and presentational components
    constants/     labels, messages, limits, routes
  tests/           Vitest + React Testing Library
docs/              requirements, design, trade-offs
prompts/           the AI prompts used for each phase, with review notes
```

## Documentation

- [Requirements](docs/requirements.md): goal, scope and assumptions
- [Design](docs/design.md): architecture, data model and API
- [Trade-offs](docs/tradeoffs.md): the main decisions and their costs
