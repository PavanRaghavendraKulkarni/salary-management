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
- Salary insights: per country (headcount, min, max, average) and, within a country, per job title and per department, each in local currency and as an approximate USD figure.
- An organisation-wide view (headcount, min, max, average) in USD, so HR can compare pay across countries.
- A seed of 10,000 realistic employees so the app can be evaluated immediately.

## Out of scope

| Item | Reason |
|---|---|
| Authentication and roles | Single trusted HR user for this exercise; would be added before real use. |
| Multi-tenancy | One organisation (ACME). |
| Payroll processing and tax | Different domain with legal rules per country. |
| Excel import or export | Valuable, but not required to prove the core workflow. |
| Audit history | Needs a separate design (event log); `created_at` / `updated_at` cover the basics. |
| Live exchange rates | USD figures use fixed rates; see assumption 2. |

## Assumptions

1. **Confirmed:** salary means the **annual gross base salary** of a full-time employee, stored as `annual_gross_salary`. Bonus, deductions and equity are out of scope.
2. **Confirmed:** salaries are stored in each country's **local currency**, which is exact. Insights also show **approximate USD** figures, converted with **fixed exchange rates** kept in backend constants with an "as of" date. Fixed rates make every figure reproducible and testable and need no external service; the "as of" date is shown next to every USD figure so nobody mistakes them for current rates. Each salary is converted before aggregating, so the organisation-wide average weighs every employee equally rather than every country. Each country has exactly one currency.
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
