export const EMPLOYEE_SORT_FIELDS = {
  FULL_NAME: 'full_name',
  EMAIL: 'email',
  JOB_TITLE: 'job_title',
  DEPARTMENT: 'department',
  COUNTRY: 'country',
  ANNUAL_SALARY: 'annual_salary',
  HIRE_DATE: 'hire_date',
} as const;

export type EmployeeSortField = (typeof EMPLOYEE_SORT_FIELDS)[keyof typeof EMPLOYEE_SORT_FIELDS];

export const DEFAULT_EMPLOYEE_SORT_FIELD: EmployeeSortField = EMPLOYEE_SORT_FIELDS.FULL_NAME;

export const EMPLOYEE_VALIDATION = {
  FULL_NAME_MIN_LENGTH: 2,
  FULL_NAME_MAX_LENGTH: 100,
  EMAIL_PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  SALARY_PATTERN: /^\d+(\.\d{1,2})?$/,
  MAX_ANNUAL_SALARY: 9_999_999_999.99,
} as const;

export const SEARCH_DEBOUNCE_MS = 300;
