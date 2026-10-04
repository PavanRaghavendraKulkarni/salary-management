export const API_BASE_URL = '/api/v1';

export const API_PATHS = {
  HEALTH: '/health',
  EMPLOYEES: '/employees',
  META_FILTERS: '/meta/filters',
  META_REFERENCE_DATA: '/meta/reference-data',
  INSIGHTS_COUNTRIES: '/insights/countries',
  INSIGHTS_JOB_TITLES: '/insights/job-titles',
  INSIGHTS_DEPARTMENTS: '/insights/departments',
} as const;

export const API_ERROR_CODES = {
  NOT_FOUND: 'NOT_FOUND',
  DUPLICATE_EMAIL: 'DUPLICATE_EMAIL',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  NETWORK_ERROR: 'NETWORK_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR',
} as const;

export type ApiErrorCode = (typeof API_ERROR_CODES)[keyof typeof API_ERROR_CODES];
