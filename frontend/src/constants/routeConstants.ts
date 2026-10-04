export const ROUTES = {
  ROOT: '/',
  EMPLOYEES: '/employees',
  INSIGHTS: '/insights',
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES];
