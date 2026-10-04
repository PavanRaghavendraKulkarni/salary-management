export const ROUTES = {
  ROOT: '/',
  EMPLOYEES: '/employees',
  INSIGHTS: '/insights',
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES];

/** Opt in to React Router v7 behaviour now, so upgrading later changes nothing. */
export const ROUTER_FUTURE_FLAGS = {
  v7_startTransition: true,
  v7_relativeSplatPath: true,
} as const;
