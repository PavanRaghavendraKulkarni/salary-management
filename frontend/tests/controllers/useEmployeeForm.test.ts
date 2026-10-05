import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { EMPLOYEE_FORM_MODES } from '../../src/constants/employeeConstants';
import { SUCCESS_MESSAGES, VALIDATION_MESSAGES } from '../../src/constants/messageConstants';
import { validateEmployeeForm } from '../../src/controllers/employeeFormValidation';
import { useEmployeeForm } from '../../src/controllers/useEmployeeForm';
import type { EmployeeInput } from '../../src/models/employee';
import { ApiError } from '../../src/services/apiClient';
import { employeeService } from '../../src/services/employeeService';
import { buildEmployee, REFERENCE_DATA } from '../fixtures';

vi.mock('../../src/services/employeeService', () => ({
  employeeService: {
    create: vi.fn(),
    update: vi.fn(),
    getReferenceData: vi.fn(),
  },
}));

const service = vi.mocked(employeeService);
const TODAY = '2026-01-15';

const VALID_VALUES: EmployeeInput = {
  full_name: 'Asha Rao',
  email: 'asha.rao@acme.com',
  job_title: 'Software Engineer',
  department: 'Engineering',
  country: 'India',
  currency: 'INR',
  annual_gross_salary: '1500000.00',
  hire_date: '2022-04-01',
};

describe('validateEmployeeForm', () => {
  it('accepts valid values', () => {
    expect(validateEmployeeForm(VALID_VALUES, TODAY)).toEqual({});
  });

  it.each([
    ['full_name', 'A', VALIDATION_MESSAGES.FULL_NAME_LENGTH],
    ['full_name', 'A'.repeat(101), VALIDATION_MESSAGES.FULL_NAME_LENGTH],
    ['full_name', '   ', VALIDATION_MESSAGES.FULL_NAME_LENGTH],
    ['email', 'not-an-email', VALIDATION_MESSAGES.EMAIL_INVALID],
    ['job_title', '', VALIDATION_MESSAGES.REQUIRED],
    ['department', '', VALIDATION_MESSAGES.REQUIRED],
    ['country', '', VALIDATION_MESSAGES.REQUIRED],
    ['annual_gross_salary', '', VALIDATION_MESSAGES.SALARY_INVALID],
    ['annual_gross_salary', 'abc', VALIDATION_MESSAGES.SALARY_INVALID],
    ['annual_gross_salary', '100.123', VALIDATION_MESSAGES.SALARY_INVALID],
    ['annual_gross_salary', '-5', VALIDATION_MESSAGES.SALARY_INVALID],
    ['annual_gross_salary', '0', VALIDATION_MESSAGES.SALARY_POSITIVE],
    ['annual_gross_salary', '0.00', VALIDATION_MESSAGES.SALARY_POSITIVE],
    ['annual_gross_salary', '99999999999', VALIDATION_MESSAGES.SALARY_TOO_HIGH],
    ['hire_date', '', VALIDATION_MESSAGES.REQUIRED],
    ['hire_date', '2026-01-16', VALIDATION_MESSAGES.HIRE_DATE_FUTURE],
  ] as const)('rejects %s = "%s"', (field, value, message) => {
    const errors = validateEmployeeForm({ ...VALID_VALUES, [field]: value }, TODAY);

    expect(errors).toEqual({ [field]: message });
  });

  it('accepts a hire date of today', () => {
    expect(validateEmployeeForm({ ...VALID_VALUES, hire_date: TODAY }, TODAY)).toEqual({});
  });
});

describe('useEmployeeForm', () => {
  const onSaved = vi.fn();

  beforeEach(() => {
    service.getReferenceData.mockResolvedValue(REFERENCE_DATA);
    service.create.mockResolvedValue(buildEmployee());
    service.update.mockResolvedValue(buildEmployee());
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  async function renderFormHook() {
    const hook = renderHook(() => useEmployeeForm({ onSaved }));
    await waitFor(() => expect(hook.result.current.referenceData).toEqual(REFERENCE_DATA));
    return hook;
  }

  function fillValidValues(setField: (name: keyof EmployeeInput, value: string) => void) {
    (Object.keys(VALID_VALUES) as (keyof EmployeeInput)[]).forEach((name) =>
      setField(name, VALID_VALUES[name]),
    );
  }

  it('opens an empty form for a new employee', async () => {
    const { result } = await renderFormHook();

    act(() => result.current.openCreate());

    expect(result.current.isOpen).toBe(true);
    expect(result.current.mode).toBe(EMPLOYEE_FORM_MODES.CREATE);
    expect(result.current.values.full_name).toBe('');
  });

  it('pre-fills the form when editing an employee', async () => {
    const { result } = await renderFormHook();

    act(() => result.current.openEdit(buildEmployee({ full_name: 'Ravi Kumar' })));

    expect(result.current.mode).toBe(EMPLOYEE_FORM_MODES.EDIT);
    expect(result.current.values.full_name).toBe('Ravi Kumar');
  });

  it('sets the currency automatically when the country changes', async () => {
    const { result } = await renderFormHook();
    act(() => result.current.openCreate());

    act(() => result.current.setField('country', 'Germany'));

    expect(result.current.values.currency).toBe('EUR');
  });

  it('shows validation errors and does not call the API for invalid input', async () => {
    const { result } = await renderFormHook();
    act(() => result.current.openCreate());

    await act(() => result.current.submit());

    expect(result.current.errors.full_name).toBe(VALIDATION_MESSAGES.FULL_NAME_LENGTH);
    expect(service.create).not.toHaveBeenCalled();
  });

  it('clears a field error once the user edits that field', async () => {
    const { result } = await renderFormHook();
    act(() => result.current.openCreate());
    await act(() => result.current.submit());

    act(() => result.current.setField('full_name', 'Asha'));

    expect(result.current.errors.full_name).toBeUndefined();
  });

  it('creates an employee with trimmed values, reports success and closes', async () => {
    const { result } = await renderFormHook();
    act(() => result.current.openCreate());
    act(() => fillValidValues(result.current.setField));
    act(() => result.current.setField('full_name', '  Asha Rao  '));

    await act(() => result.current.submit());

    expect(service.create).toHaveBeenCalledWith(VALID_VALUES);
    expect(onSaved).toHaveBeenCalledWith(SUCCESS_MESSAGES.EMPLOYEE_CREATED);
    expect(result.current.isOpen).toBe(false);
  });

  it('updates the employee being edited', async () => {
    const { result } = await renderFormHook();
    act(() => result.current.openEdit(buildEmployee({ id: 42 })));
    act(() => result.current.setField('annual_gross_salary', '1600000.00'));

    await act(() => result.current.submit());

    expect(service.update).toHaveBeenCalledWith(
      42,
      expect.objectContaining({ annual_gross_salary: '1600000.00' }),
    );
    expect(onSaved).toHaveBeenCalledWith(SUCCESS_MESSAGES.EMPLOYEE_UPDATED);
  });

  it('shows a duplicate email next to the email field and keeps the form open', async () => {
    service.create.mockRejectedValue(new ApiError(409, 'DUPLICATE_EMAIL', 'Email taken.'));
    const { result } = await renderFormHook();
    act(() => result.current.openCreate());
    act(() => fillValidValues(result.current.setField));

    await act(() => result.current.submit());

    expect(result.current.errors.email).toBe('Email taken.');
    expect(result.current.isOpen).toBe(true);
    expect(onSaved).not.toHaveBeenCalled();
  });

  it('shows other server errors as a form-level message', async () => {
    service.create.mockRejectedValue(new ApiError(422, 'VALIDATION_ERROR', 'Bad currency.'));
    const { result } = await renderFormHook();
    act(() => result.current.openCreate());
    act(() => fillValidValues(result.current.setField));

    await act(() => result.current.submit());

    expect(result.current.submitError).toBe('Bad currency.');
    expect(result.current.isSubmitting).toBe(false);
  });
});
