/** Approximate USD figures, converted per employee at fixed rates dated `rates_as_of`. */
export interface UsdSalaryStatistics {
  min_salary: string;
  max_salary: string;
  average_salary: string;
  rates_as_of: string;
}

/** Salary figures for one group, as decimal strings in that group's local currency. */
export interface SalaryStatistics {
  headcount: number;
  min_salary: string;
  max_salary: string;
  average_salary: string;
}

export interface CountryInsight extends SalaryStatistics {
  country: string;
  currency: string;
  usd_rate: string;
  usd: UsdSalaryStatistics;
}

export interface GroupInsight extends SalaryStatistics {
  name: string;
  usd: UsdSalaryStatistics;
}

export interface CountryBreakdown {
  country: string;
  currency: string;
  usd_rate: string;
  groups: GroupInsight[];
}

/** Organisation-wide pay is only comparable in one currency, so it is USD only. */
export interface OrganizationInsight {
  headcount: number;
  usd: UsdSalaryStatistics | null;
}
