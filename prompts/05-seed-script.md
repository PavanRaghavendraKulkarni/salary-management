# Phase 5: Seed script

## Prompt

> Write `backend/scripts/seed.py` to generate 10,000 employees with Faker.
> Use a fixed random seed from constants so every run produces the same data. Define realistic salary bands per country (in local currency) and per job title in `constants/seed_constants.py`. Insert in batches so the full seed finishes in under 10 seconds. Skip seeding if data already exists unless `--reset` is passed.
> Tests first with a small count: the correct number of rows; every row passes the same validation the API applies; the same seed gives identical data; existing data is not duplicated; `--reset` replaces it.

## Notes

- **Accepted:** one country band (mid-level Software Engineer, local currency) times a per-role multiplier, rather than 108 hand-typed country × role ranges. Still "per country and job title", far easier to review.
- **Accepted:** headcount weights per country and role so the data looks like a real organisation, and each job title maps to one department.
- **Changed:** "every row passes validation" is tested by pushing seeded rows through `EmployeeService.create_employee`, so seed data obeys exactly the API rules (currency, future dates, unique email).
- **Changed:** bulk inserts go through new repository methods (`bulk_create`, `count_all`, `delete_all`), keeping the session inside the repository layer.
- **Changed:** emails are built from an ASCII form of the name plus a sequence number, so they are always unique and valid even for Japanese names.
- **Changed:** `today` is a parameter so determinism tests do not depend on the real date.
- **Result:** the full 10,000-row seed runs in about 1.2 seconds locally.
