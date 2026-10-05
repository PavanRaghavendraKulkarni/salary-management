import { describe, expect, it } from 'vitest';

import { formatIsoDate } from '../../src/utils/formatDate';

describe('formatIsoDate', () => {
  it('formats an ISO date for display without shifting it by time zone', () => {
    expect(formatIsoDate('2026-10-02')).toBe('October 2, 2026');
  });
});
