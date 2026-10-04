# Requirements

## Goal

Give ACME's HR Manager one place to maintain salary records for about 10,000 employees across several countries, and to answer "how do we pay people?" without spreadsheet formulas.

## User persona

**HR Manager**: comfortable with Excel, not technical. Maintains salary data today in large spreadsheets and is asked by leadership for salary statistics by country and role.

## Problem

Spreadsheets at this size are slow, error-prone (duplicate rows, wrong currency for a country, typos in job titles) and make it hard to answer simple questions such as "what is the average salary of a Software Engineer in India?".

## In scope

- View employees in a paginated table with search (name or email), filters (country, department, job title) and sorting.
- Add, edit and delete an employee, with validation of every field.
- Salary insights: per country (headcount, min, max, average) and, within a country, per job title and per department.
- A seed of 10,000 realistic employees so the app can be evaluated immediately.

## Out of scope

| Item | Reason |
|---|---|
| Authentication and roles | Single trusted HR user for this exercise; would be added before real use. |
| Multi-tenancy | One organisation (ACME). |
| Payroll processing and tax | Different domain with legal rules per country. |
| Excel import or export | Valuable, but not required to prove the core workflow. |
| Audit history | Needs a separate design (event log); `created_at` / `updated_at` cover the basics. |
| Currency conversion | See assumptions. |

## Assumptions

1. Salary means **annual base pay** only (no bonus or equity).
2. Each country has exactly one currency, and insights are reported **per country in local currency**. No cross-currency totals are shown, because they would need exchange rates.
3. Allowed countries (9), departments (9) and job titles (12) are a fixed list in backend constants; changing them is a code change.
4. Emails are unique and compared case-insensitively (stored lowercase).
5. Hire dates cannot be in the future; there is no lower bound.
6. The frontend form reads allowed values and the country-to-currency mapping from `GET /meta/reference-data`, so the backend stays the single source of truth.
7. Insight endpoints return one row per group (at most a few dozen rows), so they are not paginated.
8. Data on the free hosting tier may be reset on redeploy; the app re-seeds itself when the database is empty.

## Success criteria

- HR can find any employee in a couple of clicks and edit them without errors reaching the database.
- Invalid data (wrong currency, salary ≤ 0, future hire date, duplicate email) is rejected with a clear message.
- List and insight requests respond quickly on 10,000 rows because filtering, paging and aggregation happen in SQL.
- All backend and frontend tests, linters and type checks pass.
