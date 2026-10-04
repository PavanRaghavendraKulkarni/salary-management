import { describe, expect, it } from 'vitest';

import { formatCurrency } from '../../src/utils/formatCurrency';

describe('formatCurrency', () => {
  it('formats a decimal string in the given currency', () => {
    expect(formatCurrency('85000.50', 'USD')).toBe('$85,000.50');
  });

  it('uses the currency symbol for non-dollar currencies', () => {
    expect(formatCurrency('1500000.00', 'INR')).toBe('₹1,500,000.00');
  });

  it('omits decimals for currencies that have none', () => {
    expect(formatCurrency('6500000.00', 'JPY')).toBe('¥6,500,000');
  });

  it('accepts numbers as well as strings', () => {
    expect(formatCurrency(72000, 'EUR')).toBe('€72,000.00');
  });
});
