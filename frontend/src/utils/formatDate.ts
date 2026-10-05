import { DISPLAY_LOCALE, DISPLAY_TIME_ZONE } from '../constants/messageConstants';

/** Format a YYYY-MM-DD date; read and printed in UTC so no time zone moves it a day. */
export function formatIsoDate(isoDate: string): string {
  return new Intl.DateTimeFormat(DISPLAY_LOCALE, {
    dateStyle: 'long',
    timeZone: DISPLAY_TIME_ZONE,
  }).format(new Date(isoDate));
}
