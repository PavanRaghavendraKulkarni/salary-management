import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { ACTION_LABELS, DIALOG_TITLES } from '../../src/constants/messageConstants';
import { employeeService } from '../../src/services/employeeService';
import EmployeesPage from '../../src/views/pages/EmployeesPage';
import { buildEmployee, buildPage, REFERENCE_DATA } from '../fixtures';

vi.mock('../../src/services/employeeService', () => ({
  employeeService: {
    list: vi.fn(),
    remove: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    getFilterOptions: vi.fn(),
    getReferenceData: vi.fn(),
  },
}));

const service = vi.mocked(employeeService);

beforeEach(() => {
  vi.clearAllMocks();
  service.list.mockResolvedValue(buildPage([buildEmployee({ id: 5 })]));
  service.getFilterOptions.mockResolvedValue({
    countries: ['India'],
    departments: ['Engineering'],
    job_titles: ['Software Engineer'],
  });
  service.getReferenceData.mockResolvedValue(REFERENCE_DATA);
  service.remove.mockResolvedValue(undefined);
});

describe('EmployeesPage', () => {
  it('lists employees returned by the service', async () => {
    render(<EmployeesPage />);

    expect(await screen.findByText('Asha Rao')).toBeInTheDocument();
  });

  it('deletes an employee only after confirmation', async () => {
    render(<EmployeesPage />);
    fireEvent.click(
      await screen.findByRole('button', { name: `${ACTION_LABELS.DELETE} Asha Rao` }),
    );

    expect(service.remove).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole('button', { name: ACTION_LABELS.CONFIRM_DELETE }));

    await waitFor(() => expect(service.remove).toHaveBeenCalledWith(5));
  });

  it('opens the add dialog', async () => {
    render(<EmployeesPage />);
    await screen.findByText('Asha Rao');

    fireEvent.click(screen.getByRole('button', { name: ACTION_LABELS.ADD }));

    expect(await screen.findByText(DIALOG_TITLES.CREATE)).toBeInTheDocument();
  });
});
