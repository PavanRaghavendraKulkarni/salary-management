/** Fixed locale so numbers and dates look the same for every user and in tests. */
export const DISPLAY_LOCALE = 'en-US';

export const APP_TITLE = 'ACME Salary Management';

export const NAV_LABELS = {
  EMPLOYEES: 'Employees',
  INSIGHTS: 'Insights',
} as const;

export const PAGE_TITLES = {
  EMPLOYEES: 'Employees',
  INSIGHTS: 'Salary Insights',
} as const;

export const ERROR_MESSAGES = {
  NETWORK: 'Could not reach the server. Check your connection and try again.',
  UNKNOWN: 'Something went wrong. Please try again.',
  LOAD_EMPLOYEES: 'Could not load employees.',
  LOAD_OPTIONS: 'Could not load filter options.',
  DELETE_EMPLOYEE: 'Could not delete the employee.',
} as const;

export const NOTIFICATION_DURATION_MS = 4000;

export const SUCCESS_MESSAGES = {
  EMPLOYEE_CREATED: 'Employee added.',
  EMPLOYEE_UPDATED: 'Employee updated.',
  EMPLOYEE_DELETED: 'Employee deleted.',
} as const;

export const VALIDATION_MESSAGES = {
  REQUIRED: 'This field is required.',
  FULL_NAME_LENGTH: 'Name must be between 2 and 100 characters.',
  EMAIL_INVALID: 'Enter a valid email address.',
  SALARY_INVALID: 'Enter an amount with at most two decimal places.',
  SALARY_POSITIVE: 'Salary must be greater than zero.',
  SALARY_TOO_HIGH: 'Salary is too large.',
  HIRE_DATE_FUTURE: 'Hire date cannot be in the future.',
} as const;

export const FIELD_LABELS = {
  full_name: 'Full name',
  email: 'Email',
  job_title: 'Job title',
  department: 'Department',
  country: 'Country',
  currency: 'Currency',
  annual_salary: 'Annual salary',
  hire_date: 'Hire date',
} as const;

export const ACTION_LABELS = {
  ADD: 'Add employee',
  EDIT: 'Edit',
  DELETE: 'Delete',
  SAVE: 'Save',
  CANCEL: 'Cancel',
  CONFIRM_DELETE: 'Delete employee',
  CLEAR_FILTERS: 'Clear filters',
} as const;

export const TABLE_LABELS = {
  ACTIONS: 'Actions',
  EMPTY: 'No employees match your search.',
  ROWS_PER_PAGE: 'Rows per page',
} as const;

export const FILTER_LABELS = {
  SEARCH: 'Search name or email',
  ALL: 'All',
} as const;

export const DIALOG_TITLES = {
  CREATE: 'Add employee',
  EDIT: 'Edit employee',
  CONFIRM_DELETE: 'Delete employee?',
} as const;

export function deleteConfirmationMessage(fullName: string): string {
  return `${fullName} will be removed permanently. This cannot be undone.`;
}

export const INSIGHT_LABELS = {
  INTRO:
    'Salaries are annual base pay in each country’s local currency, so figures are only compared within a country.',
  COUNTRY_SUMMARY: 'Pay by country',
  COUNTRY_SUMMARY_HINT: 'Select a country to see its breakdown.',
  COUNTRY_SELECT: 'Country',
  BY_JOB_TITLE: 'By job title',
  BY_DEPARTMENT: 'By department',
  COUNTRY: 'Country',
  JOB_TITLE: 'Job title',
  DEPARTMENT: 'Department',
  CURRENCY: 'Currency',
  HEADCOUNT: 'Headcount',
  MINIMUM: 'Minimum',
  AVERAGE: 'Average',
  MAXIMUM: 'Maximum',
  EMPTY: 'No salary data yet.',
  CHART_RANGE: 'Range',
} as const;

export function averageSalaryChartTitle(country: string, currency: string): string {
  return `Average salary by job title in ${country} (${currency})`;
}
