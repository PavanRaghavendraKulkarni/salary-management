import { useCallback, useEffect, useState } from 'react';

import { API_ERROR_CODES } from '../constants/apiConstants';
import {
  EMPLOYEE_FORM_MODES,
  EMPLOYEE_VALIDATION,
  type EmployeeFormMode,
} from '../constants/employeeConstants';
import { SUCCESS_MESSAGES, VALIDATION_MESSAGES } from '../constants/messageConstants';
import type { Employee, EmployeeInput, ReferenceData } from '../models/employee';
import { toApiError } from '../services/apiClient';
import { employeeService } from '../services/employeeService';
import { todayIsoDate } from '../utils/todayIsoDate';

export type EmployeeFormErrors = Partial<Record<keyof EmployeeInput, string>>;

const EMPTY_VALUES: EmployeeInput = {
  full_name: '',
  email: '',
  job_title: '',
  department: '',
  country: '',
  currency: '',
  annual_salary: '',
  hire_date: '',
};

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
  if (amount > EMPLOYEE_VALIDATION.MAX_ANNUAL_SALARY) return VALIDATION_MESSAGES.SALARY_TOO_HIGH;
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
  const salaryError = validateSalary(values.annual_salary);
  if (salaryError) errors.annual_salary = salaryError;
  if (values.hire_date && values.hire_date > today) {
    errors.hire_date = VALIDATION_MESSAGES.HIRE_DATE_FUTURE;
  }
  return errors;
}

function toFormValues(employee: Employee): EmployeeInput {
  const { full_name, email, job_title, department, country, currency, annual_salary, hire_date } =
    employee;
  return { full_name, email, job_title, department, country, currency, annual_salary, hire_date };
}

function trimmed(values: EmployeeInput): EmployeeInput {
  return {
    ...values,
    full_name: values.full_name.trim(),
    email: values.email.trim(),
    annual_salary: values.annual_salary.trim(),
  };
}

interface UseEmployeeFormOptions {
  onSaved: (message: string) => void;
}

export interface UseEmployeeFormResult {
  isOpen: boolean;
  mode: EmployeeFormMode;
  values: EmployeeInput;
  errors: EmployeeFormErrors;
  submitError: string | null;
  isSubmitting: boolean;
  referenceData: ReferenceData | null;
  openCreate: () => void;
  openEdit: (employee: Employee) => void;
  close: () => void;
  setField: (name: keyof EmployeeInput, value: string) => void;
  submit: () => Promise<void>;
}

/** Holds the add/edit dialog state, validates input and saves through the service. */
export function useEmployeeForm({ onSaved }: UseEmployeeFormOptions): UseEmployeeFormResult {
  const [isOpen, setIsOpen] = useState(false);
  const [mode, setMode] = useState<EmployeeFormMode>(EMPLOYEE_FORM_MODES.CREATE);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [values, setValues] = useState<EmployeeInput>(EMPTY_VALUES);
  const [errors, setErrors] = useState<EmployeeFormErrors>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [referenceData, setReferenceData] = useState<ReferenceData | null>(null);

  useEffect(() => {
    employeeService
      .getReferenceData()
      .then(setReferenceData)
      .catch((caught: unknown) => setSubmitError(toApiError(caught).message));
  }, []);

  const openWith = useCallback(
    (nextMode: EmployeeFormMode, nextValues: EmployeeInput, id: number | null) => {
      setMode(nextMode);
      setEditingId(id);
      setValues(nextValues);
      setErrors({});
      setSubmitError(null);
      setIsOpen(true);
    },
    [],
  );

  const openCreate = useCallback(
    () => openWith(EMPLOYEE_FORM_MODES.CREATE, EMPTY_VALUES, null),
    [openWith],
  );

  const openEdit = useCallback(
    (employee: Employee) => openWith(EMPLOYEE_FORM_MODES.EDIT, toFormValues(employee), employee.id),
    [openWith],
  );

  const close = useCallback(() => setIsOpen(false), []);

  const setField = useCallback(
    (name: keyof EmployeeInput, value: string) => {
      setValues((current) => {
        const next = { ...current, [name]: value };
        if (name === 'country') {
          const match = referenceData?.countries.find((country) => country.name === value);
          next.currency = match?.currency ?? '';
        }
        return next;
      });
      setErrors((current) => ({ ...current, [name]: undefined }));
    },
    [referenceData],
  );

  const submit = useCallback(async () => {
    const validationErrors = validateEmployeeForm(values, todayIsoDate());
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length > 0) return;

    setIsSubmitting(true);
    setSubmitError(null);
    try {
      const payload = trimmed(values);
      if (mode === EMPLOYEE_FORM_MODES.EDIT && editingId !== null) {
        await employeeService.update(editingId, payload);
        onSaved(SUCCESS_MESSAGES.EMPLOYEE_UPDATED);
      } else {
        await employeeService.create(payload);
        onSaved(SUCCESS_MESSAGES.EMPLOYEE_CREATED);
      }
      setIsOpen(false);
    } catch (caught) {
      const apiError = toApiError(caught);
      if (apiError.code === API_ERROR_CODES.DUPLICATE_EMAIL) {
        setErrors({ email: apiError.message });
      } else {
        setSubmitError(apiError.message);
      }
    } finally {
      setIsSubmitting(false);
    }
  }, [values, mode, editingId, onSaved]);

  return {
    isOpen,
    mode,
    values,
    errors,
    submitError,
    isSubmitting,
    referenceData,
    openCreate,
    openEdit,
    close,
    setField,
    submit,
  };
}
