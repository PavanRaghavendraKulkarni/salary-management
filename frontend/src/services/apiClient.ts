import axios from 'axios';

import { API_BASE_URL, API_ERROR_CODES, type ApiErrorCode } from '../constants/apiConstants';
import { ERROR_MESSAGES } from '../constants/messageConstants';

interface ApiErrorBody {
  error?: { code?: string; message?: string };
}

/** One error type for every failed request, so hooks never inspect axios internals. */
export class ApiError extends Error {
  readonly status: number | null;
  readonly code: ApiErrorCode | string;

  constructor(status: number | null, code: ApiErrorCode | string, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

export function toApiError(error: unknown): ApiError {
  if (error instanceof ApiError) {
    return error;
  }
  if (!axios.isAxiosError<ApiErrorBody>(error)) {
    return new ApiError(null, API_ERROR_CODES.UNKNOWN_ERROR, ERROR_MESSAGES.UNKNOWN);
  }
  if (!error.response) {
    return new ApiError(null, API_ERROR_CODES.NETWORK_ERROR, ERROR_MESSAGES.NETWORK);
  }
  const body = error.response.data?.error;
  return new ApiError(
    error.response.status,
    body?.code ?? API_ERROR_CODES.UNKNOWN_ERROR,
    body?.message ?? ERROR_MESSAGES.UNKNOWN,
  );
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.response.use(undefined, (error: unknown) =>
  Promise.reject(toApiError(error)),
);
