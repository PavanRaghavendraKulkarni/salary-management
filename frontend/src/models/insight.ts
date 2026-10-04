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
}

export interface GroupInsight extends SalaryStatistics {
  name: string;
}

export interface CountryBreakdown {
  country: string;
  currency: string;
  groups: GroupInsight[];
}
