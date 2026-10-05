import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import OrganizationSummary from '../../src/views/components/OrganizationSummary';
import { ORGANIZATION_INSIGHT } from '../insightFixtures';

describe('OrganizationSummary', () => {
  it('shows organisation-wide headcount and USD minimum, average and maximum', () => {
    render(<OrganizationSummary organization={ORGANIZATION_INSIGHT} />);

    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('$7,910.00')).toBeInTheDocument();
    expect(screen.getByText('$32,972.05')).toBeInTheDocument();
    expect(screen.getByText('$70,200.00')).toBeInTheDocument();
  });

  it('labels the USD figures as approximate with the exchange rate date', () => {
    render(<OrganizationSummary organization={ORGANIZATION_INSIGHT} />);

    expect(screen.getByRole('heading', { name: /approx\. USD/i })).toBeInTheDocument();
    expect(screen.getByText(/approximate.*as of October 2, 2026/i)).toBeInTheDocument();
  });

  it('shows an empty message when there are no employees', () => {
    render(<OrganizationSummary organization={{ headcount: 0, usd: null }} />);

    expect(screen.getByText(/no salary data/i)).toBeInTheDocument();
  });
});
