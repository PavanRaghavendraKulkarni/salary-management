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

export const VALIDATION_MESSAGES = {
  REQUIRED: 'This field is required.',
  FULL_NAME_LENGTH: 'Name must be between 2 and 100 characters.',
  EMAIL_INVALID: 'Enter a valid email address.',
  SALARY_INVALID: 'Enter an amount with at most two decimal places.',
  SALARY_POSITIVE: 'Salary must be greater than zero.',
  SALARY_TOO_HIGH: 'Salary is too large.',
  HIRE_DATE_FUTURE: 'Hire date cannot be in the future.',
} as const;
