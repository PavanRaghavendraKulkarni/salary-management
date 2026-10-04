import { afterEach, describe, expect, it, vi } from 'vitest';

import { API_PATHS } from '../../src/constants/apiConstants';
import { apiClient } from '../../src/services/apiClient';
import { insightService } from '../../src/services/insightService';
import { buildBreakdown, COUNTRY_INSIGHTS } from '../insightFixtures';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('insightService', () => {
  it('fetches the per-country summary', async () => {
    const get = vi.spyOn(apiClient, 'get').mockResolvedValue({ data: COUNTRY_INSIGHTS });

    await expect(insightService.getCountryInsights()).resolves.toEqual(COUNTRY_INSIGHTS);
    expect(get).toHaveBeenCalledWith(API_PATHS.INSIGHTS_COUNTRIES);
  });

  it('fetches job title and department breakdowns for one country', async () => {
    const breakdown = buildBreakdown('India', 'INR', 'Software Engineer');
    const get = vi.spyOn(apiClient, 'get').mockResolvedValue({ data: breakdown });

    await insightService.getJobTitleInsights('India');
    await insightService.getDepartmentInsights('India');

    expect(get).toHaveBeenCalledWith(API_PATHS.INSIGHTS_JOB_TITLES, {
      params: { country: 'India' },
    });
    expect(get).toHaveBeenCalledWith(API_PATHS.INSIGHTS_DEPARTMENTS, {
      params: { country: 'India' },
    });
  });
});
