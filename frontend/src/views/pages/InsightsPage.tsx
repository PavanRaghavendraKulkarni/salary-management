import Alert from '@mui/material/Alert';
import LinearProgress from '@mui/material/LinearProgress';
import MenuItem from '@mui/material/MenuItem';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';

import {
  INSIGHT_LABELS,
  PAGE_TITLES,
  averageSalaryChartTitle,
} from '../../constants/messageConstants';
import { useInsights } from '../../controllers/useInsights';
import type { CountryBreakdown } from '../../models/insight';
import OrganizationSummary from '../components/OrganizationSummary';
import SalaryChart from '../components/SalaryChart';
import SalaryStatsTable, { type SalaryStatsRow } from '../components/SalaryStatsTable';

function toRows(breakdown: CountryBreakdown | null): SalaryStatsRow[] {
  if (!breakdown) return [];
  return breakdown.groups.map((group) => ({
    ...group,
    label: group.name,
    currency: breakdown.currency,
  }));
}

export default function InsightsPage() {
  const insights = useInsights();
  const { jobTitleBreakdown, departmentBreakdown, selectedCountry } = insights;
  const countryRows: SalaryStatsRow[] = insights.countries.map((country) => ({
    ...country,
    label: country.country,
  }));

  return (
    <Stack spacing={3}>
      <div>
        <Typography variant="h4" component="h1">
          {PAGE_TITLES.INSIGHTS}
        </Typography>
        <Typography color="text.secondary">{INSIGHT_LABELS.INTRO}</Typography>
      </div>

      {insights.error && <Alert severity="error">{insights.error}</Alert>}
      {insights.isLoadingCountries && <LinearProgress />}
      {insights.organization && <OrganizationSummary organization={insights.organization} />}

      <div>
        <SalaryStatsTable
          title={INSIGHT_LABELS.COUNTRY_SUMMARY}
          groupLabel={INSIGHT_LABELS.COUNTRY}
          rows={countryRows}
          showCurrency
          selectedLabel={selectedCountry}
          onSelect={insights.selectCountry}
        />
        <Typography variant="caption" color="text.secondary">
          {INSIGHT_LABELS.COUNTRY_SUMMARY_HINT}
        </Typography>
      </div>

      {selectedCountry && (
        <>
          <TextField
            select
            label={INSIGHT_LABELS.COUNTRY_SELECT}
            value={selectedCountry}
            onChange={(event) => insights.selectCountry(event.target.value)}
            size="small"
            sx={{ maxWidth: 280 }}
          >
            {insights.countries.map(({ country }) => (
              <MenuItem key={country} value={country}>
                {country}
              </MenuItem>
            ))}
          </TextField>

          {insights.isLoadingBreakdown && <LinearProgress />}

          {jobTitleBreakdown && jobTitleBreakdown.groups.length > 0 && (
            <SalaryChart
              title={averageSalaryChartTitle(jobTitleBreakdown.country, jobTitleBreakdown.currency)}
              currency={jobTitleBreakdown.currency}
              groups={jobTitleBreakdown.groups}
            />
          )}

          {/* Full width: side by side, seven columns did not fit and clipped the USD column. */}
          <SalaryStatsTable
            title={INSIGHT_LABELS.BY_JOB_TITLE}
            groupLabel={INSIGHT_LABELS.JOB_TITLE}
            rows={toRows(jobTitleBreakdown)}
          />
          <SalaryStatsTable
            title={INSIGHT_LABELS.BY_DEPARTMENT}
            groupLabel={INSIGHT_LABELS.DEPARTMENT}
            rows={toRows(departmentBreakdown)}
          />
        </>
      )}
    </Stack>
  );
}
