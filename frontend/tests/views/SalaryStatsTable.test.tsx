import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import SalaryStatsTable from '../../src/views/components/SalaryStatsTable';
import { buildBreakdown, COUNTRY_INSIGHTS } from '../insightFixtures';

const ROWS = COUNTRY_INSIGHTS.map((insight) => ({ ...insight, label: insight.country }));
const BREAKDOWN = buildBreakdown('India', 'INR', 'Software Engineer');
const BREAKDOWN_ROWS = BREAKDOWN.groups.map((group) => ({
  ...group,
  label: group.name,
  currency: BREAKDOWN.currency,
}));

describe('SalaryStatsTable', () => {
  it('shows each statistic formatted in the row currency', () => {
    render(<SalaryStatsTable title="By country" groupLabel="Country" rows={ROWS} />);

    expect(screen.getByText('₹1,066,666.67')).toBeInTheDocument();
    expect(screen.getByText('€50,000.20')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
  });

  it('adds an approximate USD average column labelled with the exchange rate date', () => {
    render(<SalaryStatsTable title="By country" groupLabel="Country" rows={ROWS} />);

    expect(screen.getByRole('columnheader', { name: /average \(≈ USD\)/i })).toBeInTheDocument();
    expect(screen.getByText('$12,053.33')).toBeInTheDocument();
    expect(screen.getByText(/approximate.*as of October 2, 2026/i)).toBeInTheDocument();
  });

  it('keeps the USD column readable in a breakdown table that scrolls horizontally', () => {
    render(<SalaryStatsTable title="By job title" groupLabel="Job title" rows={BREAKDOWN_ROWS} />);

    const usdHeader = screen.getByRole('columnheader', { name: /average \(≈ USD\)/i });
    const scrollContainer = screen.getByRole('table', { name: 'By job title' }).parentElement;
    expect(getComputedStyle(usdHeader).whiteSpace).toBe('nowrap');
    expect(scrollContainer).not.toBeNull();
    expect(getComputedStyle(scrollContainer as HTMLElement).overflowX).toBe('auto');
  });

  it('reports the clicked row and highlights the selected one', () => {
    const onSelect = vi.fn();
    render(
      <SalaryStatsTable
        title="By country"
        groupLabel="Country"
        rows={ROWS}
        selectedLabel="India"
        onSelect={onSelect}
      />,
    );

    fireEvent.click(screen.getByText('Germany'));

    expect(onSelect).toHaveBeenCalledWith('Germany');
    expect(screen.getByText('India').closest('tr')).toHaveAttribute('aria-selected', 'true');
  });

  it('shows an empty message when there are no rows', () => {
    render(<SalaryStatsTable title="By country" groupLabel="Country" rows={[]} />);

    expect(screen.getByText(/no salary data/i)).toBeInTheDocument();
  });
});
