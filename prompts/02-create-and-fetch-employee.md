# Phase 2: Create and fetch an employee (TDD)

## Prompt

> Using TDD, implement creating and fetching an employee across every backend layer: model, views, repository, service, controller, domain exceptions and central exception handlers.
> Write the tests first and show them failing: valid create returns 201; duplicate email returns 409; salary of zero or below returns 422; currency that does not match the country returns 422; hire date in the future returns 422; unknown id returns 404.
> Also unit-test the service directly with a fixed "today" so date rules are deterministic.
> Every limit, allowed value and message must come from constants. Stop after this feature.

## Notes

- **Accepted:** field rules (length, enum values, salary > 0, decimal places) live on the Pydantic view; cross-field and database rules (currency matches country, hire date not in future, unique email) live in the service and raise domain exceptions.
- **Accepted:** services return response views, so controllers are one line and never see ORM objects.
- **Changed:** the service takes a `today_provider` so the future-hire-date rule can be tested with a fixed date instead of the real clock.
- **Changed:** emails are stored lowercase so uniqueness is case-insensitive; added a test for it.
- **Changed:** timestamps are set in Python (`utc_now`) rather than by SQLite `CURRENT_TIMESTAMP`, which only has second precision and would make "updated_at changes" flaky.
- **Changed:** replaced the deprecated `HTTP_422_UNPROCESSABLE_ENTITY` with `HTTP_422_UNPROCESSABLE_CONTENT`.
- **Rejected:** catching `IntegrityError` for duplicates. The service checks first and the unique index is the backstop; a race between two HR users is unlikely for this app.
