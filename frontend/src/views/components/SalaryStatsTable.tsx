import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';

import { INSIGHT_LABELS } from '../../constants/messageConstants';
import type { SalaryStatistics } from '../../models/insight';
import { formatCurrency } from '../../utils/formatCurrency';

export interface SalaryStatsRow extends SalaryStatistics {
  label: string;
  currency: string;
}

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
  const columnCount = showCurrency ? 6 : 5;

  return (
    <Paper variant="outlined">
      <Typography variant="h6" component="h2" sx={{ px: 2, pt: 2 }}>
        {title}
      </Typography>
      <TableContainer>
        <Table size="small" aria-label={title}>
          <TableHead>
            <TableRow>
              <TableCell>{groupLabel}</TableCell>
              {showCurrency && <TableCell>{INSIGHT_LABELS.CURRENCY}</TableCell>}
              <TableCell align="right">{INSIGHT_LABELS.HEADCOUNT}</TableCell>
              <TableCell align="right">{INSIGHT_LABELS.MINIMUM}</TableCell>
              <TableCell align="right">{INSIGHT_LABELS.AVERAGE}</TableCell>
              <TableCell align="right">{INSIGHT_LABELS.MAXIMUM}</TableCell>
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
    </Paper>
  );
}
