import { EMPLOYEE_VALIDATION } from '../constants/employeeConstants';
import { VALIDATION_MESSAGES } from '../constants/messageConstants';
import type { EmployeeInput } from '../models/employee';

export type EmployeeFormErrors = Partial<Record<keyof EmployeeInput, string>>;

const REQUIRED_SELECTIONS = ['job_title', 'department', 'country', 'hire_date'] as const;

function validateFullName(fullName: string): string | undefined {
  const length = fullName.trim().length;
  const { FULL_NAME_MIN_LENGTH, FULL_NAME_MAX_LENGTH } = EMPLOYEE_VALIDATION;
  return length < FULL_NAME_MIN_LENGTH || length > FULL_NAME_MAX_LENGTH
    ? VALIDATION_MESSAGES.FULL_NAME_LENGTH
    : undefined;
}

function validateSalary(salary: string): string | undefined {
  const trimmed = salary.trim();
  if (!EMPLOYEE_VALIDATION.SALARY_PATTERN.test(trimmed)) return VALIDATION_MESSAGES.SALARY_INVALID;
  const amount = Number(trimmed);
  if (amount <= 0) return VALIDATION_MESSAGES.SALARY_POSITIVE;
  if (amount > EMPLOYEE_VALIDATION.MAX_ANNUAL_GROSS_SALARY)
    return VALIDATION_MESSAGES.SALARY_TOO_HIGH;
  return undefined;
}

/** Mirrors the backend rules so most mistakes are caught before a request is sent. */
export function validateEmployeeForm(values: EmployeeInput, today: string): EmployeeFormErrors {
  const errors: EmployeeFormErrors = {};
  const fullNameError = validateFullName(values.full_name);
  if (fullNameError) errors.full_name = fullNameError;
  if (!EMPLOYEE_VALIDATION.EMAIL_PATTERN.test(values.email.trim())) {
    errors.email = VALIDATION_MESSAGES.EMAIL_INVALID;
  }
  REQUIRED_SELECTIONS.forEach((field) => {
    if (!values[field]) errors[field] = VALIDATION_MESSAGES.REQUIRED;
  });
  const salaryError = validateSalary(values.annual_gross_salary);
  if (salaryError) errors.annual_gross_salary = salaryError;
  if (values.hire_date && values.hire_date > today) {
    errors.hire_date = VALIDATION_MESSAGES.HIRE_DATE_FUTURE;
  }
  return errors;
}
