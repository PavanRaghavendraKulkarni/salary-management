import type { Employee, PaginatedResponse, ReferenceData } from '../src/models/employee';

export function buildEmployee(overrides: Partial<Employee> = {}): Employee {
  return {
    id: 1,
    full_name: 'Asha Rao',
    email: 'asha.rao@acme.com',
    job_title: 'Software Engineer',
    department: 'Engineering',
    country: 'India',
    currency: 'INR',
    annual_salary: '1500000.00',
    hire_date: '2022-04-01',
    created_at: '2024-01-01T00:00:00',
    updated_at: '2024-01-01T00:00:00',
    ...overrides,
  };
}

export function buildPage(
  items: Employee[],
  overrides: Partial<PaginatedResponse<Employee>> = {},
): PaginatedResponse<Employee> {
  return { items, total: items.length, page: 1, page_size: 20, ...overrides };
}

export const REFERENCE_DATA: ReferenceData = {
  countries: [
    { name: 'India', currency: 'INR' },
    { name: 'Germany', currency: 'EUR' },
  ],
  departments: ['Engineering', 'Sales'],
  job_titles: ['Software Engineer', 'Sales Representative'],
};
