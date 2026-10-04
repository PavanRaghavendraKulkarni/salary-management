import { API_PATHS } from '../constants/apiConstants';
import type {
  Employee,
  EmployeeInput,
  EmployeeListParams,
  FilterOptions,
  PaginatedResponse,
  ReferenceData,
} from '../models/employee';
import { apiClient } from './apiClient';

function withoutEmptyValues(params: EmployeeListParams): Partial<EmployeeListParams> {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) => value !== '' && value !== undefined),
  );
}

function employeeUrl(id: number): string {
  return `${API_PATHS.EMPLOYEES}/${id}`;
}

export const employeeService = {
  async list(params: EmployeeListParams): Promise<PaginatedResponse<Employee>> {
    const response = await apiClient.get<PaginatedResponse<Employee>>(API_PATHS.EMPLOYEES, {
      params: withoutEmptyValues(params),
    });
    return response.data;
  },

  async create(input: EmployeeInput): Promise<Employee> {
    const response = await apiClient.post<Employee>(API_PATHS.EMPLOYEES, input);
    return response.data;
  },

  async update(id: number, input: EmployeeInput): Promise<Employee> {
    const response = await apiClient.put<Employee>(employeeUrl(id), input);
    return response.data;
  },

  async remove(id: number): Promise<void> {
    await apiClient.delete(employeeUrl(id));
  },

  async getFilterOptions(): Promise<FilterOptions> {
    const response = await apiClient.get<FilterOptions>(API_PATHS.META_FILTERS);
    return response.data;
  },

  async getReferenceData(): Promise<ReferenceData> {
    const response = await apiClient.get<ReferenceData>(API_PATHS.META_REFERENCE_DATA);
    return response.data;
  },
};
