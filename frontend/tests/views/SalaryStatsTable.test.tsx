import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import SalaryStatsTable from '../../src/views/components/SalaryStatsTable';
import { COUNTRY_INSIGHTS } from '../insightFixtures';

const ROWS = COUNTRY_INSIGHTS.map((insight) => ({ ...insight, label: insight.country }));

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
