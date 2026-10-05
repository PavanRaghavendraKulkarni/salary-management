import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';

import { REPORTING_CURRENCY } from '../../constants/employeeConstants';
import { approximateUsdNote, INSIGHT_LABELS } from '../../constants/messageConstants';
import type { SalaryStatistics, UsdSalaryStatistics } from '../../models/insight';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatIsoDate } from '../../utils/formatDate';

export interface SalaryStatsRow extends SalaryStatistics {
  label: string;
  currency: string;
  usd: UsdSalaryStatistics;
}

const STATISTIC_HEADERS = [
  INSIGHT_LABELS.HEADCOUNT,
  INSIGHT_LABELS.MINIMUM,
  INSIGHT_LABELS.AVERAGE,
  INSIGHT_LABELS.MAXIMUM,
  INSIGHT_LABELS.AVERAGE_USD,
];

interface SalaryStatsTableProps {
  title: string;
  groupLabel: string;
  rows: SalaryStatsRow[];
  showCurrency?: boolean;
  selectedLabel?: string;
  onSelect?: (label: string) => void;
}

export default function SalaryStatsTable({
  title,
  groupLabel,
  rows,
  showCurrency = false,
  selectedLabel,
  onSelect,
}: SalaryStatsTableProps) {
  const groupColumns = showCurrency ? [groupLabel, INSIGHT_LABELS.CURRENCY] : [groupLabel];
  const columnCount = groupColumns.length + STATISTIC_HEADERS.length;

  return (
    <Paper variant="outlined">
      <Typography variant="h6" component="h2" sx={{ px: 2, pt: 2 }}>
        {title}
      </Typography>
      {/* Scrolls sideways on narrow screens so no column, including USD, is ever clipped. */}
      <TableContainer sx={{ overflowX: 'auto' }}>
        <Table size="small" aria-label={title}>
          <TableHead>
            <TableRow>
              {groupColumns.map((label) => (
                <TableCell key={label} sx={{ whiteSpace: 'nowrap' }}>
                  {label}
                </TableCell>
              ))}
              {STATISTIC_HEADERS.map((label) => (
                <TableCell key={label} align="right" sx={{ whiteSpace: 'nowrap' }}>
                  {label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow
                key={row.label}
                hover={Boolean(onSelect)}
                selected={row.label === selectedLabel}
                aria-selected={onSelect ? row.label === selectedLabel : undefined}
                onClick={onSelect ? () => onSelect(row.label) : undefined}
                sx={onSelect ? { cursor: 'pointer' } : undefined}
              >
                <TableCell>{row.label}</TableCell>
                {showCurrency && <TableCell>{row.currency}</TableCell>}
                <TableCell align="right">{row.headcount}</TableCell>
                <TableCell align="right">{formatCurrency(row.min_salary, row.currency)}</TableCell>
                <TableCell align="right">
                  {formatCurrency(row.average_salary, row.currency)}
                </TableCell>
                <TableCell align="right">{formatCurrency(row.max_salary, row.currency)}</TableCell>
                <TableCell align="right">
                  {formatCurrency(row.usd.average_salary, REPORTING_CURRENCY)}
                </TableCell>
              </TableRow>
            ))}
            {rows.length === 0 && (
              <TableRow>
                <TableCell colSpan={columnCount} align="center" sx={{ py: 4 }}>
                  {INSIGHT_LABELS.EMPTY}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      {rows[0] && (
        <Typography variant="caption" color="text.secondary" component="p" sx={{ px: 2, py: 1 }}>
          {approximateUsdNote(formatIsoDate(rows[0].usd.rates_as_of))}
        </Typography>
      )}
    </Paper>
  );
}
