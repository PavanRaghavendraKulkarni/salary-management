import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

import App from '../src/App';
import { NAV_LABELS, PAGE_TITLES } from '../src/constants/messageConstants';
import { ROUTER_FUTURE_FLAGS, ROUTES } from '../src/constants/routeConstants';

vi.mock('../src/services/employeeService', () => ({
  employeeService: {
    list: vi.fn().mockResolvedValue({ items: [], total: 0, page: 1, page_size: 20 }),
    getFilterOptions: vi.fn().mockResolvedValue({ countries: [], departments: [], job_titles: [] }),
    getReferenceData: vi.fn().mockResolvedValue({ countries: [], departments: [], job_titles: [] }),
  },
}));

vi.mock('../src/services/insightService', () => ({
  insightService: { getCountryInsights: vi.fn().mockResolvedValue([]) },
}));

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]} future={ROUTER_FUTURE_FLAGS}>
      <App />
    </MemoryRouter>,
  );
}

describe('App', () => {
  it('shows navigation links to the employees and insights pages', () => {
    renderAt(ROUTES.EMPLOYEES);

    expect(screen.getByRole('link', { name: NAV_LABELS.EMPLOYEES })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: NAV_LABELS.INSIGHTS })).toBeInTheDocument();
  });

  it('renders the employees page at the employees route', () => {
    renderAt(ROUTES.EMPLOYEES);

    expect(screen.getByRole('heading', { name: PAGE_TITLES.EMPLOYEES })).toBeInTheDocument();
  });

  it('renders the insights page at the insights route', () => {
    renderAt(ROUTES.INSIGHTS);

    expect(screen.getByRole('heading', { name: PAGE_TITLES.INSIGHTS })).toBeInTheDocument();
  });

  it('redirects the root path to the employees page', () => {
    renderAt(ROUTES.ROOT);

    expect(screen.getByRole('heading', { name: PAGE_TITLES.EMPLOYEES })).toBeInTheDocument();
  });
});
