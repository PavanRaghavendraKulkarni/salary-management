# ACME Salary Management

A web app for ACME's HR team to view, add, edit and delete employee salary records and to see how the organisation pays people across countries, job titles and departments.

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, SQLite
- **Frontend:** React 18, TypeScript, Vite, MUI, React Router, Recharts

## Prerequisites

- Python 3.12 and [uv](https://docs.astral.sh/uv/)
- Node.js 20+ and npm

## Backend

```bash
cd backend
cp .env.example .env
uv sync                                  # create .venv and install dependencies
uv run uvicorn app.main:app --reload     # http://localhost:8000, docs at /docs
```

Checks:

```bash
uv run pytest --cov=app                  # tests with coverage
uv run ruff check . && uv run ruff format --check .
uv run mypy
```

## Frontend

```bash
cd frontend
npm install
npm run dev                              # http://localhost:5173, proxies /api to :8000
```

Checks:

```bash
npm test
npm run lint
npm run format:check
npm run build
```

## Project structure

- `backend/app`: layered MVC (controllers → services → repositories → models, with Pydantic views)
- `frontend/src`: models, services (API calls), controllers (hooks), views (pages and components)
- `docs/`: requirements, design and trade-offs
