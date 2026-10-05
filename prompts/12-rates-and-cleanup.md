# Phase 12: Real exchange rates and clean-up

## Prompt

> Phase 11 is approved, with the following changes. Work through them in order, run all tests and checks after each step, and stop at the end with a summary.
>
> 1. Replace the placeholder exchange rates in `backend/app/constants/currency_constants.py` with the official ECB reference rates of 2 October 2026 (USD 1, EUR 1.1225, GBP 1.320076, INR 0.010382, CAD 0.702265, AUD 0.693929, SGD 0.781359, JPY 0.006342). Set the "as of" date to 2 October 2026 and add a comment with the source and the formula: USD per 1 unit = (USD per EUR) / (currency per EUR), with USD per EUR = 1.1225. Confirm every currency used by the 9 countries has a rate. Update the source and date in `docs/tradeoffs.md`, check that the UI note reads "as of October 2, 2026", and re-run the seeded-data check, verifying the organisation-wide USD average against an independent SQL query.
> 2. Commit Phase 11 as the six proposed commits, each red test commit followed directly by its green commit.
> 3. Move the four salary-aggregation methods into `repositories/salary_insight_repository.py` so each file stays under about 200 lines. No behaviour change. Commit as `refactor:`.
> 4. Update CLAUDE.md: add `/insights/organization` to the API section; add `salary_insight_repository.py` and `currency_constants.py` to the folder structure; keep the new commit rule. Commit it with `docs:`; it belongs in the repo as the main AI instruction artifact.
> 5. Add a performance section to `docs/design.md`: work done in SQL, indexes and why each exists, the `page_size` limit, seed time, measured response times on seeded data, and the SQLite floating-point note with the PostgreSQL alternative. Commit as `docs:`.
> 6. Run every test, linter, type check and the production build; show the new commits; save this prompt and the notes here. Do not push.
>
> Follow-up while working: "please don't commit".

## Notes

- **Accepted:** the rates keep the existing names (`USD_EXCHANGE_RATES`, `USD_EXCHANGE_RATES_AS_OF`) and are keyed by the `Currency` enum. All 8 currencies used by the 9 countries have a rate; the constants test already guards this.
- **Accepted:** the frontend fixtures now use `2026-10-02`, so the tests check that the note reads "as of October 2, 2026".
- **Verified on 10,000 seeded rows:** the organisation-wide USD average is 69,851.52, matching an independent SQL query and an exact Python `Decimal` calculation. Averaging the country averages would give 67,708.39.
- **Changed:** the commits in steps 2 to 5 were not made, because the follow-up asked for no commits. A snapshot of the Phase 11 files from before the refactor was kept, so the red and green commits can still be made separately.
- **Accepted:** `SalaryInsightRepository` holds the aggregations and their result types, with its own `Depends` provider. `EmployeeRepository` is down to CRUD, listing and seeding (121 lines; the new file has 112). Test assertions are unchanged.
- **Changed:** CLAUDE.md also had a stale `annual_salary` field and an assumptions note still marked "pending confirmation"; both now state the confirmed decisions. It was removed from `.git/info/exclude` so it can be committed; `PHASE_PROMPTS.md` and the PDF stay excluded.
- **Accepted:** the performance section records the measured times, the reason for each index (including the unique email index), and that deep pages are slowest because of `OFFSET`, with keyset pagination as the fix if the data grows.

## Commit prompt

> Approved. Make the nine commits in that order, restoring the snapshot for commits 1–6 and then reapplying the current files for 7–9. Before starting, save a full backup of the working tree. Run the tests after each red `test:` commit and confirm only the expected tests fail; run every suite and linter before each other commit. After commit 9, the working tree must match the backup exactly. Also commit `PHASE_PROMPTS.md` as `prompts/00-phase-plan.md` with a `docs:` commit; keep the PDF excluded. Do not push.

## Commit notes

- **Accepted:** each commit was built by restoring only that commit's files onto a clean tree, so the tests and linters ran on exactly what was committed rather than on a working tree that also held later changes.
- **Accepted:** `prompts/00-phase-plan.md` is a copy of the phase plan; the original stays outside the repository alongside the PDF.
