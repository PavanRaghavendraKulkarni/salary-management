# Phase 9: Deploy and polish

## Prompt

> Prepare for deployment on Render as one web service: FastAPI serves the built React app and the API; the database is seeded on start-up when it is empty; add a `render.yaml`.
> Test first that `/` and client-side routes return `index.html`, built assets are served, paths outside the build folder are never served, unknown `/api` routes return the JSON error shape, and the app still starts without a frontend build.
> Then finish the docs: README (overview, live-link placeholder, local setup, tests, structure, free-tier wake-up note) and `docs/tradeoffs.md` (SQLite vs Postgres, no authentication, local-currency reporting, Decimal for money, SQL aggregation, pagination limits).
> Run every test, linter and type check and show the results.

## Review prompt (run after every phase)

> Review the code just written as a strict senior reviewer against the engineering instructions: layer violations (logic in controllers, queries outside repositories, API calls in views), magic numbers or strings outside constants, missing or weak tests, unclear names, duplication and files that are too long. List every issue, fix it and run the tests again.

## Notes

- **Accepted:** one catch-all route serves files from `frontend/dist` and falls back to `index.html`; it resolves paths and refuses anything outside the build folder.
- **Accepted:** framework errors (unknown route, wrong method) now use the same `{"error": {...}}` shape as domain errors.
- **Changed:** seeding runs in the start command (`python -m scripts.seed && uvicorn ...`) instead of inside the app's startup hook. The seed already skips when data exists, and this keeps the web app free of a dependency on the scripts folder. Faker moved to runtime dependencies for this.
- **Changed:** `create_app` accepts `Settings`, so tests choose whether a frontend build exists.
- **Changed:** lazy-loaded the Insights page so Recharts is not in the initial bundle (removed Vite's >500 kB warning).
- **Review fixes:** removed the last magic values (chart font size, table column count, a literal field name), confirmed no SQL outside repositories and no API calls from views, and kept every file under 200 lines.
- **Verified locally:** with 10,000 seeded rows, a filtered and sorted page returns in about 12 ms and the country insight in about 7 ms.
- **Final results:** backend 96 tests, 98% coverage, Ruff and strict mypy clean; frontend 75 tests, ESLint, Prettier and the production build clean.
