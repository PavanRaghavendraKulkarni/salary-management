import type {
  CountryBreakdown,
  CountryInsight,
  OrganizationInsight,
  UsdSalaryStatistics,
} from '../src/models/insight';

export const RATES_AS_OF = '2026-10-02';

function usd(min: string, max: string, average: string): UsdSalaryStatistics {
  return { min_salary: min, max_salary: max, average_salary: average, rates_as_of: RATES_AS_OF };
}

export const COUNTRY_INSIGHTS: CountryInsight[] = [
  {
    country: 'Germany',
    currency: 'EUR',
    headcount: 2,
    min_salary: '50000.20',
    max_salary: '60000.00',
    average_salary: '55000.10',
    usd_rate: '1.17',
    usd: usd('58500.23', '70200.00', '64350.12'),
  },
  {
    country: 'India',
    currency: 'INR',
    headcount: 3,
    min_salary: '700000.00',
    max_salary: '1500000.00',
    average_salary: '1066666.67',
    usd_rate: '0.0113',
    usd: usd('7910.00', '16950.00', '12053.33'),
  },
];

export const ORGANIZATION_INSIGHT: OrganizationInsight = {
  headcount: 5,
  usd: usd('7910.00', '70200.00', '32972.05'),
};

export function buildBreakdown(country: string, currency: string, name: string): CountryBreakdown {
  return {
    country,
    currency,
    usd_rate: '1',
    groups: [
      {
        name,
        headcount: 1,
        min_salary: '100.00',
        max_salary: '100.00',
        average_salary: '100.00',
        usd: usd('100.00', '100.00', '100.00'),
      },
    ],
  };
}
