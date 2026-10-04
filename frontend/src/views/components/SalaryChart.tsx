import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  type TooltipProps,
} from 'recharts';

import {
  CHART_AXIS_TEXT_COLOR,
  CHART_BAR_RADIUS,
  CHART_BAR_THICKNESS,
  CHART_CATEGORY_AXIS_WIDTH,
  CHART_GRID_COLOR,
  CHART_MARGIN,
  CHART_ROW_HEIGHT,
  CHART_SERIES_COLOR,
  CHART_VERTICAL_PADDING,
} from '../../constants/chartConstants';
import { INSIGHT_LABELS } from '../../constants/messageConstants';
import type { GroupInsight } from '../../models/insight';
import { formatCompactCurrency, formatCurrency } from '../../utils/formatCurrency';

interface SalaryChartProps {
  title: string;
  currency: string;
  groups: GroupInsight[];
}

interface ChartDatum extends GroupInsight {
  average: number;
}

const AXIS_TICK = { fill: CHART_AXIS_TEXT_COLOR, fontSize: 12 };

function SalaryTooltip({
  active,
  payload,
  currency,
}: TooltipProps<number, string> & { currency: string }) {
  const datum = payload?.[0]?.payload as ChartDatum | undefined;
  if (!active || !datum) return null;
  return (
    <Paper variant="outlined" sx={{ px: 1.5, py: 1 }}>
      <Typography variant="subtitle2">{datum.name}</Typography>
      <Typography variant="body2">
        {INSIGHT_LABELS.AVERAGE}: {formatCurrency(datum.average_salary, currency)}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {INSIGHT_LABELS.CHART_RANGE}: {formatCurrency(datum.min_salary, currency)} –{' '}
        {formatCurrency(datum.max_salary, currency)}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {INSIGHT_LABELS.HEADCOUNT}: {datum.headcount}
      </Typography>
    </Paper>
  );
}

/** One currency per chart, so bar lengths are always comparable. */
export default function SalaryChart({ title, currency, groups }: SalaryChartProps) {
  const data: ChartDatum[] = [...groups]
    .map((group) => ({ ...group, average: Number(group.average_salary) }))
    .sort((first, second) => second.average - first.average);
  const height = data.length * CHART_ROW_HEIGHT + CHART_VERTICAL_PADDING;

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Typography variant="h6" component="h2" sx={{ mb: 1 }}>
        {title}
      </Typography>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data} layout="vertical" margin={CHART_MARGIN}>
          <CartesianGrid horizontal={false} stroke={CHART_GRID_COLOR} />
          <XAxis
            type="number"
            tick={AXIS_TICK}
            tickFormatter={(value: number) => formatCompactCurrency(value, currency)}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={CHART_CATEGORY_AXIS_WIDTH}
            tick={AXIS_TICK}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            cursor={{ fill: CHART_GRID_COLOR, fillOpacity: 0.5 }}
            content={<SalaryTooltip currency={currency} />}
          />
          <Bar
            dataKey="average"
            fill={CHART_SERIES_COLOR}
            barSize={CHART_BAR_THICKNESS}
            radius={CHART_BAR_RADIUS}
            isAnimationActive={false}
          >
            <LabelList
              dataKey="average"
              position="right"
              fill={CHART_AXIS_TEXT_COLOR}
              fontSize={12}
              formatter={(value: number) => formatCompactCurrency(value, currency)}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Paper>
  );
}
