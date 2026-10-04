# Phase 0: Project setup

## Prompt

> Read the engineering instructions and set up the project skeleton exactly as the agreed folder structure describes. Do not build features yet.
> Backend: FastAPI app factory, pydantic-settings configuration, SQLAlchemy session, constants files with initial values, `GET /api/v1/health`, Ruff and mypy configured in `pyproject.toml`, and one integration test for health written first.
> Frontend: Vite + React 18 + strict TypeScript, MUI, React Router with Employees and Insights routes, ESLint, Prettier, Vitest and one smoke test written first.
> Root: README with setup and test commands, `.gitignore`, `backend/.env.example`.

## Notes

- **Accepted:** app factory (`create_app`) so each test builds a fresh app with its own dependency overrides; in-memory SQLite with `StaticPool` in `conftest.py`.
- **Changed:** the Vite template now ships React 19 and oxlint. Replaced it with React 18, Vite 6 and ESLint 9 to match the agreed stack.
- **Changed:** added `views/health_view.py` so the health endpoint returns a typed view rather than a raw dict.
- **Rejected:** the template's demo assets, CSS and README.
