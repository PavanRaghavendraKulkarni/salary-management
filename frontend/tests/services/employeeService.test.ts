import { AxiosError, type AxiosResponse } from 'axios';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { API_PATHS } from '../../src/constants/apiConstants';
import { ApiError, apiClient, toApiError } from '../../src/services/apiClient';
import { employeeService } from '../../src/services/employeeService';
import { buildEmployee, buildPage } from '../fixtures';

function axiosErrorWith(status: number, data: unknown): AxiosError {
  const response = { status, data } as AxiosResponse;
  return new AxiosError('Request failed', 'ERR_BAD_REQUEST', undefined, undefined, response);
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe('toApiError', () => {
  it('reads the code and message from the backend error shape', () => {
    const error = toApiError(
      axiosErrorWith(409, { error: { code: 'DUPLICATE_EMAIL', message: 'Email taken.' } }),
    );

    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({ status: 409, code: 'DUPLICATE_EMAIL', message: 'Email taken.' });
  });

  it('falls back to a generic message when the server is unreachable', () => {
    const error = toApiError(new AxiosError('Network Error', 'ERR_NETWORK'));

    expect(error.code).toBe('NETWORK_ERROR');
    expect(error.message).toMatch(/could not reach the server/i);
  });
});

describe('employeeService', () => {
  it('lists employees with only the parameters that are set', async () => {
    const page = buildPage([buildEmployee()]);
    const get = vi.spyOn(apiClient, 'get').mockResolvedValue({ data: page });

    const result = await employeeService.list({
      search: '',
      country: 'India',
      department: '',
      job_title: '',
      page: 2,
      page_size: 20,
      sort_by: 'full_name',
      sort_order: 'asc',
    });

    expect(result).toEqual(page);
    expect(get).toHaveBeenCalledWith(API_PATHS.EMPLOYEES, {
      params: { country: 'India', page: 2, page_size: 20, sort_by: 'full_name', sort_order: 'asc' },
    });
  });

  it('creates, updates and deletes employees through the shared client', async () => {
    const employee = buildEmployee({ id: 7 });
    const { id, created_at, updated_at, ...input } = employee;
    void created_at;
    void updated_at;
    const post = vi.spyOn(apiClient, 'post').mockResolvedValue({ data: employee });
    const put = vi.spyOn(apiClient, 'put').mockResolvedValue({ data: employee });
    const remove = vi.spyOn(apiClient, 'delete').mockResolvedValue({ data: '' });

    await employeeService.create(input);
    await employeeService.update(id, input);
    await employeeService.remove(id);

    expect(post).toHaveBeenCalledWith(API_PATHS.EMPLOYEES, input);
    expect(put).toHaveBeenCalledWith(`${API_PATHS.EMPLOYEES}/7`, input);
    expect(remove).toHaveBeenCalledWith(`${API_PATHS.EMPLOYEES}/7`);
  });
});
