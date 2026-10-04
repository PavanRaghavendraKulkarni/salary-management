import type { CountryBreakdown, CountryInsight } from '../src/models/insight';

export const COUNTRY_INSIGHTS: CountryInsight[] = [
  {
    country: 'Germany',
    currency: 'EUR',
    headcount: 2,
    min_salary: '50000.20',
    max_salary: '60000.00',
    average_salary: '55000.10',
  },
  {
    country: 'India',
    currency: 'INR',
    headcount: 3,
    min_salary: '700000.00',
    max_salary: '1500000.00',
    average_salary: '1066666.67',
  },
];

export function buildBreakdown(country: string, currency: string, name: string): CountryBreakdown {
  return {
    country,
    currency,
    groups: [
      {
        name,
        headcount: 1,
        min_salary: '100.00',
        max_salary: '100.00',
        average_salary: '100.00',
      },
    ],
  };
}
