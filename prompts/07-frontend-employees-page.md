# Phase 7: Frontend employees page

## Prompt

> Build the Employees page following the frontend MVC layers:
> models (Employee types), services (`employeeService` on the shared `apiClient`), controllers (`useEmployees` for list, filters, search, sorting and pagination; `useEmployeeForm` for create, edit and validation), and views (`EmployeesPage`, `EmployeeTable`, `EmployeeFilters`, `EmployeeFormDialog`).
> Features: paginated sortable table, debounced search, filter dropdowns, add and edit in a dialog, delete with confirmation, loading and error states, salaries formatted in each employee's local currency. Every label, message and limit comes from constants.
> Write Vitest tests first for the service, the hooks, the form validation and the key components, mocking the service layer. Work in slices: failing test commit, then implementation commit.

## Notes

- **Accepted:** an axios response interceptor turns every failure into one `ApiError` (status, code, message), so hooks never look at axios internals.
- **Accepted:** the form takes its allowed values and the country-to-currency mapping from `GET /meta/reference-data`; currency is filled in automatically and read-only.
- **Accepted:** client-side validation mirrors the backend rules; a duplicate email from the server (409) is shown next to the email field.
- **Changed:** salary stays a decimal **string** end to end and is only converted to a number by `Intl.NumberFormat` for display.
- **Changed:** split `validateEmployeeForm` into `employeeFormValidation.ts` when `useEmployeeForm.ts` reached 200 lines.
- **Changed:** added `ConfirmDeleteDialog.tsx`, `employeeConstants.ts` and `todayIsoDate.ts`, which the folder structure did not list but the "labels and limits from constants" rule needed.
- **Rejected:** `@mui/icons-material` for edit and delete icons, because it is not in the agreed stack; used labelled text buttons instead.
- **Rejected:** a debounce library; a `setTimeout` in `useEmployees` is enough and is tested with fake timers.
