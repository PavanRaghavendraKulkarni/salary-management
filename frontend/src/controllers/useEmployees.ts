import { useCallback, useEffect, useState } from 'react';

import {
  DEFAULT_EMPLOYEE_SORT_FIELD,
  SEARCH_DEBOUNCE_MS,
  type EmployeeSortField,
} from '../constants/employeeConstants';
import { ERROR_MESSAGES, SUCCESS_MESSAGES } from '../constants/messageConstants';
import { DEFAULT_PAGE, DEFAULT_PAGE_SIZE, SORT_ORDER } from '../constants/paginationConstants';
import type {
  Employee,
  EmployeeFilterName,
  EmployeeFilterValues,
  EmployeeListParams,
  FilterOptions,
} from '../models/employee';
import { toApiError } from '../services/apiClient';
import { employeeService } from '../services/employeeService';

const EMPTY_FILTERS: EmployeeFilterValues = { country: '', department: '', job_title: '' };
const EMPTY_FILTER_OPTIONS: FilterOptions = { countries: [], departments: [], job_titles: [] };

const INITIAL_PARAMS: EmployeeListParams = {
  search: '',
  ...EMPTY_FILTERS,
  page: DEFAULT_PAGE,
  page_size: DEFAULT_PAGE_SIZE,
  sort_by: DEFAULT_EMPLOYEE_SORT_FIELD,
  sort_order: SORT_ORDER.ASC,
};

export interface UseEmployeesResult {
  employees: Employee[];
  total: number;
  params: EmployeeListParams;
  searchInput: string;
  filterOptions: FilterOptions;
  isLoading: boolean;
  error: string | null;
  notification: string | null;
  setSearch: (search: string) => void;
  setFilter: (name: EmployeeFilterName, value: string) => void;
  clearFilters: () => void;
  setPage: (page: number) => void;
  setPageSize: (pageSize: number) => void;
  setSort: (field: EmployeeSortField) => void;
  deleteEmployee: (id: number) => Promise<boolean>;
  handleEmployeeSaved: (message: string) => void;
  dismissNotification: () => void;
}

/** Owns the employee table's query state and keeps it in sync with the API. */
export function useEmployees(): UseEmployeesResult {
  const [params, setParams] = useState<EmployeeListParams>(INITIAL_PARAMS);
  const [searchInput, setSearchInput] = useState('');
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [total, setTotal] = useState(0);
  const [filterOptions, setFilterOptions] = useState<FilterOptions>(EMPTY_FILTER_OPTIONS);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [notification, setNotification] = useState<string | null>(null);
  const [reloadCount, setReloadCount] = useState(0);

  useEffect(() => {
    let isCurrent = true;
    setIsLoading(true);
    employeeService
      .list(params)
      .then((page) => {
        if (!isCurrent) return;
        setEmployees(page.items);
        setTotal(page.total);
        setError(null);
      })
      .catch((caught: unknown) => {
        if (!isCurrent) return;
        setEmployees([]);
        setTotal(0);
        setError(toApiError(caught).message || ERROR_MESSAGES.LOAD_EMPLOYEES);
      })
      .finally(() => {
        if (isCurrent) setIsLoading(false);
      });
    return () => {
      isCurrent = false;
    };
  }, [params, reloadCount]);

  useEffect(() => {
    employeeService
      .getFilterOptions()
      .then(setFilterOptions)
      .catch(() => setError(ERROR_MESSAGES.LOAD_OPTIONS));
  }, [reloadCount]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setParams((current) =>
        current.search === searchInput
          ? current
          : { ...current, search: searchInput, page: DEFAULT_PAGE },
      );
    }, SEARCH_DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [searchInput]);

  const reload = useCallback(() => setReloadCount((count) => count + 1), []);

  const setFilter = useCallback((name: EmployeeFilterName, value: string) => {
    setParams((current) => ({ ...current, [name]: value, page: DEFAULT_PAGE }));
  }, []);

  const clearFilters = useCallback(() => {
    setSearchInput('');
    setParams((current) => ({ ...current, ...EMPTY_FILTERS, search: '', page: DEFAULT_PAGE }));
  }, []);

  const setPage = useCallback((page: number) => {
    setParams((current) => ({ ...current, page }));
  }, []);

  const setPageSize = useCallback((pageSize: number) => {
    setParams((current) => ({ ...current, page_size: pageSize, page: DEFAULT_PAGE }));
  }, []);

  const setSort = useCallback((field: EmployeeSortField) => {
    setParams((current) => {
      const isSameField = current.sort_by === field;
      const toggledOrder = current.sort_order === SORT_ORDER.ASC ? SORT_ORDER.DESC : SORT_ORDER.ASC;
      return {
        ...current,
        sort_by: field,
        sort_order: isSameField ? toggledOrder : SORT_ORDER.ASC,
      };
    });
  }, []);

  const deleteEmployee = useCallback(
    async (id: number) => {
      try {
        await employeeService.remove(id);
        setNotification(SUCCESS_MESSAGES.EMPLOYEE_DELETED);
        reload();
        return true;
      } catch (caught) {
        setError(toApiError(caught).message || ERROR_MESSAGES.DELETE_EMPLOYEE);
        return false;
      }
    },
    [reload],
  );

  const handleEmployeeSaved = useCallback(
    (message: string) => {
      setNotification(message);
      reload();
    },
    [reload],
  );

  const dismissNotification = useCallback(() => setNotification(null), []);

  return {
    employees,
    total,
    params,
    searchInput,
    filterOptions,
    isLoading,
    error,
    notification,
    setSearch: setSearchInput,
    setFilter,
    clearFilters,
    setPage,
    setPageSize,
    setSort,
    deleteEmployee,
    handleEmployeeSaved,
    dismissNotification,
  };
}
