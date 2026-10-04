import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { EMPLOYEE_SORT_FIELDS, SEARCH_DEBOUNCE_MS } from '../../src/constants/employeeConstants';
import { SUCCESS_MESSAGES } from '../../src/constants/messageConstants';
import { DEFAULT_PAGE_SIZE, SORT_ORDER } from '../../src/constants/paginationConstants';
import { useEmployees } from '../../src/controllers/useEmployees';
import { ApiError } from '../../src/services/apiClient';
import { employeeService } from '../../src/services/employeeService';
import { buildEmployee, buildPage } from '../fixtures';

vi.mock('../../src/services/employeeService', () => ({
  employeeService: {
    list: vi.fn(),
    remove: vi.fn(),
    getFilterOptions: vi.fn(),
  },
}));

const service = vi.mocked(employeeService);
const FILTER_OPTIONS = { countries: ['India'], departments: ['Engineering'], job_titles: [] };

function lastListParams() {
  return service.list.mock.lastCall?.[0];
}

async function renderLoadedHook() {
  const hook = renderHook(() => useEmployees());
  await waitFor(() => expect(hook.result.current.isLoading).toBe(false));
  return hook;
}

beforeEach(() => {
  service.list.mockResolvedValue(buildPage([buildEmployee()], { total: 1 }));
  service.getFilterOptions.mockResolvedValue(FILTER_OPTIONS);
  service.remove.mockResolvedValue(undefined);
});

afterEach(() => {
  vi.clearAllMocks();
  vi.useRealTimers();
});

describe('useEmployees', () => {
  it('loads the first page with default parameters', async () => {
    const { result } = await renderLoadedHook();

    expect(lastListParams()).toEqual({
      search: '',
      country: '',
      department: '',
      job_title: '',
      page: 1,
      page_size: DEFAULT_PAGE_SIZE,
      sort_by: EMPLOYEE_SORT_FIELDS.FULL_NAME,
      sort_order: SORT_ORDER.ASC,
    });
    expect(result.current.employees).toHaveLength(1);
    expect(result.current.total).toBe(1);
    expect(result.current.error).toBeNull();
  });

  it('loads filter options for the dropdowns', async () => {
    const { result } = await renderLoadedHook();

    await waitFor(() => expect(result.current.filterOptions).toEqual(FILTER_OPTIONS));
  });

  it('exposes the error message when loading fails', async () => {
    service.list.mockRejectedValue(new ApiError(500, 'UNKNOWN_ERROR', 'Server exploded.'));

    const { result } = await renderLoadedHook();

    expect(result.current.error).toBe('Server exploded.');
    expect(result.current.employees).toEqual([]);
  });

  it('applies a filter and goes back to the first page', async () => {
    const { result } = await renderLoadedHook();
    act(() => result.current.setPage(3));

    act(() => result.current.setFilter('country', 'India'));

    await waitFor(() => expect(lastListParams()).toMatchObject({ country: 'India', page: 1 }));
  });

  it('clears every filter at once', async () => {
    const { result } = await renderLoadedHook();
    act(() => result.current.setFilter('department', 'Sales'));

    act(() => result.current.clearFilters());

    await waitFor(() =>
      expect(lastListParams()).toMatchObject({ department: '', country: '', search: '' }),
    );
  });

  it('requests the chosen page', async () => {
    const { result } = await renderLoadedHook();

    act(() => result.current.setPage(2));

    await waitFor(() => expect(lastListParams()).toMatchObject({ page: 2 }));
  });

  it('changes page size and returns to the first page', async () => {
    const { result } = await renderLoadedHook();
    act(() => result.current.setPage(4));

    act(() => result.current.setPageSize(50));

    await waitFor(() => expect(lastListParams()).toMatchObject({ page: 1, page_size: 50 }));
  });

  it('sorts ascending by a new column and toggles direction on the same column', async () => {
    const { result } = await renderLoadedHook();

    act(() => result.current.setSort(EMPLOYEE_SORT_FIELDS.ANNUAL_SALARY));
    await waitFor(() =>
      expect(lastListParams()).toMatchObject({ sort_by: 'annual_salary', sort_order: 'asc' }),
    );

    act(() => result.current.setSort(EMPLOYEE_SORT_FIELDS.ANNUAL_SALARY));
    await waitFor(() =>
      expect(lastListParams()).toMatchObject({ sort_by: 'annual_salary', sort_order: 'desc' }),
    );
  });

  it('waits for the user to stop typing before searching', async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    const { result } = await renderLoadedHook();

    act(() => result.current.setSearch('asha'));
    expect(result.current.searchInput).toBe('asha');
    expect(lastListParams()).toMatchObject({ search: '' });

    act(() => vi.advanceTimersByTime(SEARCH_DEBOUNCE_MS));

    await waitFor(() => expect(lastListParams()).toMatchObject({ search: 'asha', page: 1 }));
  });

  it('deletes an employee, reloads the list and confirms', async () => {
    const { result } = await renderLoadedHook();
    const callsBefore = service.list.mock.calls.length;

    let deleted = false;
    await act(async () => {
      deleted = await result.current.deleteEmployee(1);
    });

    expect(deleted).toBe(true);
    expect(service.remove).toHaveBeenCalledWith(1);
    await waitFor(() => expect(service.list.mock.calls.length).toBeGreaterThan(callsBefore));
    expect(result.current.notification).toBe(SUCCESS_MESSAGES.EMPLOYEE_DELETED);
  });

  it('reports a failed delete without throwing', async () => {
    service.remove.mockRejectedValue(new ApiError(404, 'NOT_FOUND', 'Employee not found.'));
    const { result } = await renderLoadedHook();

    let deleted = true;
    await act(async () => {
      deleted = await result.current.deleteEmployee(99);
    });

    expect(deleted).toBe(false);
    expect(result.current.error).toBe('Employee not found.');
  });

  it('reloads and shows a notification after an employee is saved', async () => {
    const { result } = await renderLoadedHook();
    const callsBefore = service.list.mock.calls.length;

    act(() => result.current.handleEmployeeSaved(SUCCESS_MESSAGES.EMPLOYEE_CREATED));

    await waitFor(() => expect(service.list.mock.calls.length).toBeGreaterThan(callsBefore));
    expect(result.current.notification).toBe(SUCCESS_MESSAGES.EMPLOYEE_CREATED);

    act(() => result.current.dismissNotification());
    expect(result.current.notification).toBeNull();
  });
});
