import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { EMPLOYEE_FORM_MODES } from '../../src/constants/employeeConstants';
import { ACTION_LABELS, DIALOG_TITLES, FIELD_LABELS } from '../../src/constants/messageConstants';
import EmployeeFormDialog from '../../src/views/components/EmployeeFormDialog';
import { buildEmployee, REFERENCE_DATA } from '../fixtures';

function renderDialog(overrides: Partial<Parameters<typeof EmployeeFormDialog>[0]> = {}) {
  const { id, created_at, updated_at, ...values } = buildEmployee();
  void id;
  void created_at;
  void updated_at;
  const props = {
    isOpen: true,
    mode: EMPLOYEE_FORM_MODES.CREATE,
    values,
    errors: {},
    submitError: null,
    isSubmitting: false,
    referenceData: REFERENCE_DATA,
    onChange: vi.fn(),
    onSubmit: vi.fn(),
    onClose: vi.fn(),
    ...overrides,
  };
  render(<EmployeeFormDialog {...props} />);
  return props;
}

describe('EmployeeFormDialog', () => {
  it('uses a title that matches the mode', () => {
    renderDialog({ mode: EMPLOYEE_FORM_MODES.EDIT });

    expect(screen.getByText(DIALOG_TITLES.EDIT)).toBeInTheDocument();
  });

  it('reports typed changes by field name', () => {
    const props = renderDialog();

    fireEvent.change(screen.getByLabelText(FIELD_LABELS.full_name, { exact: false }), {
      target: { value: 'Ravi' },
    });

    expect(props.onChange).toHaveBeenCalledWith('full_name', 'Ravi');
  });

  it('shows the currency derived from the country as read-only', () => {
    renderDialog();

    const currency = screen.getByLabelText(FIELD_LABELS.currency, { exact: false });
    expect(currency).toHaveValue('INR');
    expect(currency).toHaveAttribute('readonly');
  });

  it('shows field errors and the form-level error', () => {
    renderDialog({ errors: { email: 'Email taken.' }, submitError: 'Server said no.' });

    expect(screen.getByText('Email taken.')).toBeInTheDocument();
    expect(screen.getByText('Server said no.')).toBeInTheDocument();
  });

  it('submits and cancels through the handlers', () => {
    const props = renderDialog();

    fireEvent.click(screen.getByRole('button', { name: ACTION_LABELS.SAVE }));
    fireEvent.click(screen.getByRole('button', { name: ACTION_LABELS.CANCEL }));

    expect(props.onSubmit).toHaveBeenCalledOnce();
    expect(props.onClose).toHaveBeenCalledOnce();
  });

  it('disables saving while a request is in flight', () => {
    renderDialog({ isSubmitting: true });

    expect(screen.getByRole('button', { name: ACTION_LABELS.SAVE })).toBeDisabled();
  });
});
