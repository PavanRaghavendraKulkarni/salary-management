import { DISPLAY_LOCALE } from '../constants/messageConstants';

/** Format an amount in its own currency; Intl picks the right decimals (e.g. none for JPY). */
export function formatCurrency(amount: string | number, currency: string): string {
  return new Intl.NumberFormat(DISPLAY_LOCALE, { style: 'currency', currency }).format(
    Number(amount),
  );
}
