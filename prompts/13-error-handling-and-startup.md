# Phase 13: Unexpected errors and start-up tables

## Prompt

> Using TDD, make two small fixes:
> 1. Add a catch-all exception handler for unexpected errors that logs the exception and returns 500 with the standard shape `{"error": {"code": "INTERNAL_ERROR", "message": ...}}`, using a code and message from constants. Test it with a route or dependency that raises an unexpected exception.
> 2. Create database tables on application startup (lifespan), so the API works even if the seed hasn't run yet. Test that a fresh database returns an empty employee list instead of an error.
>
> Also replace the `assert isinstance` in `handle_http_exception` with an explicit type check.
> Red and green commits as usual, then run all checks and show git log. Don't push until I approve.

## Notes

- **Accepted:** a handler registered for `Exception` logs the traceback with the method and path, and returns `INTERNAL_ERROR` with a generic message from constants. Tests override the employee-service dependency to raise a `RuntimeError` and check the 500 shape, that the error text never reaches the response, and that the traceback is logged.
- **Accepted:** `handle_http_exception` now checks the type explicitly and hands anything else to the unexpected-error handler. An `assert` disappears under `python -O`; a unit test calls the handler with a `ValueError` to prove the check holds.
- **Changed:** creating tables at start-up needed each app to use the database its settings name. Before, requests went through an engine built once at import time from `.env`, so `create_app(settings)` ignored `settings.database_url`; the red test showed this by returning the developer database's rows. Each app now builds its own engine, keeps the session factory on `app.state` and disposes the engine on shutdown. The seed script builds its own engine from settings.
- **Changed:** test settings now use in-memory SQLite (`build_test_settings`), so the start-up hook never touches the developer's database file during tests.
- **Changed:** the type-only fix `json.loads(bytes(response.body))` in the new unit test went into the green commit, because mypy flagged the red version.
- **Not changed:** `handle_domain_error` and `handle_request_validation_error` still use `assert isinstance`; only `handle_http_exception` was in scope.
- **Note:** Starlette re-raises an unhandled exception after the 500 handler responds, so in production uvicorn also logs it. The handler's own log line adds the request method and path.
