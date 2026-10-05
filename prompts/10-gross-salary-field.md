# Phase 10: Annual gross salary field

## Prompt

> Act as a strict Incubyte reviewer and verify the repository against the engineering instructions, the assessment brief and two confirmed decisions: salary is the annual gross base salary of a full-time employee (field `annual_gross_salary`; bonus, deductions and equity out of scope), and salaries are stored in local currency with a USD view using fixed exchange rates from constants. Report PASS, FAIL or PARTIAL with evidence, then a prioritised fix list.
>
> Then fix the must-fix items one phase at a time, starting with the field rename.

## Notes

- **Accepted:** the review found the field still named `annual_salary` and the requirements describing "annual base pay"; this phase renames it everywhere (model, schemas, sort field, seed, frontend types, form, table, tests and docs).
- **Accepted:** test-first even for a rename: the tests were renamed first and failed (backend 29 failed and 16 errors, frontend 25 failed), then the code was renamed until everything passed.
- **Changed:** the visible label is now "Annual gross salary", and docstrings and the insights note say "gross base".
- **Rejected:** keeping `annual_salary` in the database with a Pydantic alias. Two names for one value would confuse future readers; the seeded database is cheap to recreate.
- **Results:** backend 96 tests, 98% coverage, Ruff and strict mypy clean; frontend 75 tests, ESLint, Prettier and `tsc` clean.
