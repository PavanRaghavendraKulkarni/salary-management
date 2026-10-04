# Phase 4: List, search, filter, paginate (TDD)

## Prompt

> Using TDD, implement `GET /employees` with case-insensitive search on name or email, filters for country, department and job title, pagination (`page`, `page_size` default 20, max 100) and sorting (`sort_by`, `sort_order`). Add `GET /meta/filters` (distinct values in the data) and `GET /meta/reference-data` (all allowed values with each country's currency).
> Tests first: filters return only matching rows; filters combine; search is case-insensitive and matches email; pagination returns the right total and page; a page past the end is empty; `page_size` above the maximum and other invalid parameters return 422; sorting works in both directions.
> All filtering, sorting and pagination must happen in SQL inside the repository. Confirm the indexes exist with a test.

## Notes

- **Accepted:** query parameters are one Pydantic model (`EmployeeListQuery`), so bounds come from constants and invalid input returns the standard 422 shape.
- **Accepted:** sorting maps an allow-listed `EmployeeSortField` enum to columns, so users cannot sort by arbitrary SQL, and `id` breaks ties so pages are stable.
- **Changed:** search uses `icontains(..., autoescape=True)` so `%` and `_` typed by a user are matched literally; added a test.
- **Changed:** the repository takes plain keyword arguments, not the view object, so it doesn't depend on the API layer. The service turns page numbers into an offset.
- **Changed:** `/meta/filters` returns only values present in the data, while `/meta/reference-data` returns every allowed value. Both are needed: filters should never lead to an empty table, and the form must allow values with no employees yet.
- **Note:** insight endpoints are not paginated because they return one row per group (a few dozen at most). Recorded as an assumption.
