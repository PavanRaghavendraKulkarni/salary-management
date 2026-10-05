import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

import { REPORTING_CURRENCY } from '../../constants/employeeConstants';
import { approximateUsdNote, INSIGHT_LABELS } from '../../constants/messageConstants';
import type { OrganizationInsight } from '../../models/insight';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatIsoDate } from '../../utils/formatDate';

interface OrganizationSummaryProps {
  organization: OrganizationInsight;
}

function Statistic({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="h6" component="p">
        {value}
      </Typography>
    </div>
  );
}

/** Pay across every country, which is only comparable after converting to one currency. */
export default function OrganizationSummary({ organization }: OrganizationSummaryProps) {
  const { usd } = organization;

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="h6" component="h2">
        {INSIGHT_LABELS.ORGANIZATION_SUMMARY}
      </Typography>
      {usd ? (
        <>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={4} sx={{ my: 1 }}>
            <Statistic label={INSIGHT_LABELS.HEADCOUNT} value={String(organization.headcount)} />
            <Statistic
              label={INSIGHT_LABELS.MINIMUM}
              value={formatCurrency(usd.min_salary, REPORTING_CURRENCY)}
            />
            <Statistic
              label={INSIGHT_LABELS.AVERAGE}
              value={formatCurrency(usd.average_salary, REPORTING_CURRENCY)}
            />
            <Statistic
              label={INSIGHT_LABELS.MAXIMUM}
              value={formatCurrency(usd.max_salary, REPORTING_CURRENCY)}
            />
          </Stack>
          <Typography variant="caption" color="text.secondary">
            {approximateUsdNote(formatIsoDate(usd.rates_as_of))}
          </Typography>
        </>
      ) : (
        <Typography color="text.secondary">{INSIGHT_LABELS.EMPTY}</Typography>
      )}
    </Paper>
  );
}
