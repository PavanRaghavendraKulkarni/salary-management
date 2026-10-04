import { fireEvent, render, screen, within } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { EMPLOYEE_SORT_FIELDS } from '../../src/constants/employeeConstants';
import { ACTION_LABELS, FIELD_LABELS, TABLE_LABELS } from '../../src/constants/messageConstants';
import { SORT_ORDER } from '../../src/constants/paginationConstants';
import EmployeeTable from '../../src/views/components/EmployeeTable';
import { buildEmployee } from '../fixtures';

function renderTable(overrides: Partial<Parameters<typeof EmployeeTable>[0]> = {}) {
  const props = {
    employees: [
      buildEmployee(),
      buildEmployee({
        id: 2,
        full_name: 'John Smith',
        email: 'j.smith@acme.com',
        country: 'United States',
        currency: 'USD',
        annual_salary: '95000.00',
      }),
    ],
    total: 2,
    page: 1,
    pageSize: 20,
    sortBy: EMPLOYEE_SORT_FIELDS.FULL_NAME,
    sortOrder: SORT_ORDER.ASC,
    isLoading: false,
    onPageChange: vi.fn(),
    onPageSizeChange: vi.fn(),
    onSort: vi.fn(),
    onEdit: vi.fn(),
    onDelete: vi.fn(),
    ...overrides,
  };
  render(<EmployeeTable {...props} />);
  return props;
}

describe('EmployeeTable', () => {
  it('shows each salary in its own currency', () => {
    renderTable();

    expect(screen.getByText('₹1,500,000.00')).toBeInTheDocument();
    expect(screen.getByText('$95,000.00')).toBeInTheDocument();
  });

  it('shows a message when there are no employees', () => {
    renderTable({ employees: [], total: 0 });

    expect(screen.getByText(TABLE_LABELS.EMPTY)).toBeInTheDocument();
  });

  it('calls the edit and delete handlers with the employee in that row', () => {
    const props = renderTable();
    const row = screen.getByText('John Smith').closest('tr') as HTMLElement;

    fireEvent.click(within(row).getByRole('button', { name: `${ACTION_LABELS.EDIT} John Smith` }));
    fireEvent.click(
      within(row).getByRole('button', { name: `${ACTION_LABELS.DELETE} John Smith` }),
    );

    expect(props.onEdit).toHaveBeenCalledWith(expect.objectContaining({ id: 2 }));
    expect(props.onDelete).toHaveBeenCalledWith(expect.objectContaining({ id: 2 }));
  });

  it('asks to sort when a column header is clicked', () => {
    const props = renderTable();

    fireEvent.click(screen.getByRole('button', { name: FIELD_LABELS.annual_salary }));

    expect(props.onSort).toHaveBeenCalledWith(EMPLOYEE_SORT_FIELDS.ANNUAL_SALARY);
  });

  it('reports one-based page numbers when moving to the next page', () => {
    const props = renderTable({ total: 45 });

    fireEvent.click(screen.getByRole('button', { name: /next page/i }));

    expect(props.onPageChange).toHaveBeenCalledWith(2);
  });
});
