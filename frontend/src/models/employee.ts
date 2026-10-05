import type { SortOrder } from '../constants/paginationConstants';
import type { EmployeeSortField } from '../constants/employeeConstants';

export interface Employee {
  id: number;
  full_name: string;
  email: string;
  job_title: string;
  department: string;
  country: string;
  currency: string;
  /** Decimal string such as "85000.00", kept as text so no precision is lost. */
  annual_gross_salary: string;
  /** ISO date, YYYY-MM-DD. */
  hire_date: string;
  created_at: string;
  updated_at: string;
}

export type EmployeeInput = Omit<Employee, 'id' | 'created_at' | 'updated_at'>;

export interface PaginatedResponse<Item> {
  items: Item[];
  total: number;
  page: number;
  page_size: number;
}

export interface EmployeeFilterValues {
  country: string;
  department: string;
  job_title: string;
}

export type EmployeeFilterName = keyof EmployeeFilterValues;

export interface EmployeeListParams extends EmployeeFilterValues {
  search: string;
  page: number;
  page_size: number;
  sort_by: EmployeeSortField;
  sort_order: SortOrder;
}

export interface FilterOptions {
  countries: string[];
  departments: string[];
  job_titles: string[];
}

export interface CountryOption {
  name: string;
  currency: string;
}

export interface ReferenceData {
  countries: CountryOption[];
  departments: string[];
  job_titles: string[];
}
