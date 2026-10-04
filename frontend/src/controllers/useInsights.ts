import { useCallback, useEffect, useState } from 'react';

import type { CountryBreakdown, CountryInsight } from '../models/insight';
import { toApiError } from '../services/apiClient';
import { insightService } from '../services/insightService';

export interface UseInsightsResult {
  countries: CountryInsight[];
  selectedCountry: string;
  jobTitleBreakdown: CountryBreakdown | null;
  departmentBreakdown: CountryBreakdown | null;
  isLoadingCountries: boolean;
  isLoadingBreakdown: boolean;
  error: string | null;
  selectCountry: (country: string) => void;
}

/** Loads the country summary once, then the breakdowns for whichever country is selected. */
export function useInsights(): UseInsightsResult {
  const [countries, setCountries] = useState<CountryInsight[]>([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [jobTitleBreakdown, setJobTitleBreakdown] = useState<CountryBreakdown | null>(null);
  const [departmentBreakdown, setDepartmentBreakdown] = useState<CountryBreakdown | null>(null);
  const [isLoadingCountries, setIsLoadingCountries] = useState(true);
  const [isLoadingBreakdown, setIsLoadingBreakdown] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    insightService
      .getCountryInsights()
      .then((summary) => {
        setCountries(summary);
        setSelectedCountry((current) => current || (summary[0]?.country ?? ''));
      })
      .catch((caught: unknown) => setError(toApiError(caught).message))
      .finally(() => setIsLoadingCountries(false));
  }, []);

  useEffect(() => {
    if (!selectedCountry) return;
    let isCurrent = true;
    setIsLoadingBreakdown(true);
    Promise.all([
      insightService.getJobTitleInsights(selectedCountry),
      insightService.getDepartmentInsights(selectedCountry),
    ])
      .then(([jobTitles, departments]) => {
        if (!isCurrent) return;
        setJobTitleBreakdown(jobTitles);
        setDepartmentBreakdown(departments);
      })
      .catch((caught: unknown) => {
        if (isCurrent) setError(toApiError(caught).message);
      })
      .finally(() => {
        if (isCurrent) setIsLoadingBreakdown(false);
      });
    return () => {
      isCurrent = false;
    };
  }, [selectedCountry]);

  const selectCountry = useCallback((country: string) => setSelectedCountry(country), []);

  return {
    countries,
    selectedCountry,
    jobTitleBreakdown,
    departmentBreakdown,
    isLoadingCountries,
    isLoadingBreakdown,
    error,
    selectCountry,
  };
}
