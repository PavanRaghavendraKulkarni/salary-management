export const EMPLOYEE_SORT_FIELDS = {
  FULL_NAME: 'full_name',
  EMAIL: 'email',
  JOB_TITLE: 'job_title',
  DEPARTMENT: 'department',
  COUNTRY: 'country',
  ANNUAL_GROSS_SALARY: 'annual_gross_salary',
  HIRE_DATE: 'hire_date',
} as const;

export type EmployeeSortField = (typeof EMPLOYEE_SORT_FIELDS)[keyof typeof EMPLOYEE_SORT_FIELDS];

export const DEFAULT_EMPLOYEE_SORT_FIELD: EmployeeSortField = EMPLOYEE_SORT_FIELDS.FULL_NAME;

export const EMPLOYEE_VALIDATION = {
  FULL_NAME_MIN_LENGTH: 2,
  FULL_NAME_MAX_LENGTH: 100,
  EMAIL_PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  SALARY_PATTERN: /^\d+(\.\d{1,2})?$/,
  MAX_ANNUAL_GROSS_SALARY: 9_999_999_999.99,
} as const;

export const SEARCH_DEBOUNCE_MS = 300;

export const EMPLOYEE_FORM_MODES = {
  CREATE: 'create',
  EDIT: 'edit',
} as const;

export type EmployeeFormMode = (typeof EMPLOYEE_FORM_MODES)[keyof typeof EMPLOYEE_FORM_MODES];

export interface EmployeeTableColumn {
  field: EmployeeSortField;
  align: 'left' | 'right';
}

export const EMPLOYEE_TABLE_COLUMNS: readonly EmployeeTableColumn[] = [
  { field: EMPLOYEE_SORT_FIELDS.FULL_NAME, align: 'left' },
  { field: EMPLOYEE_SORT_FIELDS.EMAIL, align: 'left' },
  { field: EMPLOYEE_SORT_FIELDS.JOB_TITLE, align: 'left' },
  { field: EMPLOYEE_SORT_FIELDS.DEPARTMENT, align: 'left' },
  { field: EMPLOYEE_SORT_FIELDS.COUNTRY, align: 'left' },
  { field: EMPLOYEE_SORT_FIELDS.ANNUAL_GROSS_SALARY, align: 'right' },
  { field: EMPLOYEE_SORT_FIELDS.HIRE_DATE, align: 'left' },
];

/** Insights convert every salary to this currency for cross-country comparison. */
export const REPORTING_CURRENCY = 'USD';
