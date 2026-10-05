import { API_PATHS } from '../constants/apiConstants';
import type { CountryBreakdown, CountryInsight, OrganizationInsight } from '../models/insight';
import { apiClient } from './apiClient';

async function getBreakdown(path: string, country: string): Promise<CountryBreakdown> {
  const response = await apiClient.get<CountryBreakdown>(path, { params: { country } });
  return response.data;
}

export const insightService = {
  async getCountryInsights(): Promise<CountryInsight[]> {
    const response = await apiClient.get<CountryInsight[]>(API_PATHS.INSIGHTS_COUNTRIES);
    return response.data;
  },

  getJobTitleInsights(country: string): Promise<CountryBreakdown> {
    return getBreakdown(API_PATHS.INSIGHTS_JOB_TITLES, country);
  },

  getDepartmentInsights(country: string): Promise<CountryBreakdown> {
    return getBreakdown(API_PATHS.INSIGHTS_DEPARTMENTS, country);
  },

  async getOrganizationInsight(): Promise<OrganizationInsight> {
    const response = await apiClient.get<OrganizationInsight>(API_PATHS.INSIGHTS_ORGANIZATION);
    return response.data;
  },
};
