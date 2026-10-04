import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';

import App from '../src/App';
import { PAGE_TITLES, NAV_LABELS } from '../src/constants/messageConstants';
import { ROUTES } from '../src/constants/routeConstants';

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
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
