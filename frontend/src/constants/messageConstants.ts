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

export const SUCCESS_MESSAGES = {
  EMPLOYEE_CREATED: 'Employee added.',
  EMPLOYEE_UPDATED: 'Employee updated.',
  EMPLOYEE_DELETED: 'Employee deleted.',
} as const;
