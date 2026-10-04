import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { useInsights } from '../../src/controllers/useInsights';
import { ApiError } from '../../src/services/apiClient';
import { insightService } from '../../src/services/insightService';
import { buildBreakdown, COUNTRY_INSIGHTS } from '../insightFixtures';

vi.mock('../../src/services/insightService', () => ({
  insightService: {
    getCountryInsights: vi.fn(),
    getJobTitleInsights: vi.fn(),
    getDepartmentInsights: vi.fn(),
  },
}));

const service = vi.mocked(insightService);

beforeEach(() => {
  service.getCountryInsights.mockResolvedValue(COUNTRY_INSIGHTS);
  service.getJobTitleInsights.mockImplementation(async (country) =>
    buildBreakdown(country, 'XXX', `${country} job title`),
  );
  service.getDepartmentInsights.mockImplementation(async (country) =>
    buildBreakdown(country, 'XXX', `${country} department`),
  );
});

afterEach(() => {
  vi.clearAllMocks();
});

describe('useInsights', () => {
  it('loads the country summary and selects the first country', async () => {
    const { result } = renderHook(() => useInsights());

    await waitFor(() => expect(result.current.countries).toEqual(COUNTRY_INSIGHTS));
    expect(result.current.selectedCountry).toBe('Germany');
  });

  it('loads job title and department breakdowns for the selected country', async () => {
    const { result } = renderHook(() => useInsights());

    await waitFor(() =>
      expect(result.current.jobTitleBreakdown?.groups[0]?.name).toBe('Germany job title'),
    );
    expect(result.current.departmentBreakdown?.groups[0]?.name).toBe('Germany department');
    expect(result.current.isLoadingBreakdown).toBe(false);
  });

  it('reloads the breakdowns when another country is selected', async () => {
    const { result } = renderHook(() => useInsights());
    await waitFor(() => expect(result.current.selectedCountry).toBe('Germany'));

    act(() => result.current.selectCountry('India'));

    await waitFor(() =>
      expect(result.current.jobTitleBreakdown?.groups[0]?.name).toBe('India job title'),
    );
    expect(service.getDepartmentInsights).toHaveBeenLastCalledWith('India');
  });

  it('does not request breakdowns when there are no employees', async () => {
    service.getCountryInsights.mockResolvedValue([]);
    const { result } = renderHook(() => useInsights());

    await waitFor(() => expect(result.current.isLoadingCountries).toBe(false));

    expect(result.current.selectedCountry).toBe('');
    expect(service.getJobTitleInsights).not.toHaveBeenCalled();
  });

  it('exposes the error message when loading fails', async () => {
    service.getCountryInsights.mockRejectedValue(new ApiError(500, 'UNKNOWN_ERROR', 'Down.'));
    const { result } = renderHook(() => useInsights());

    await waitFor(() => expect(result.current.error).toBe('Down.'));
  });
});
