# Phase 8: Frontend insights page

## Prompt

> Build the Insights page with the same MVC layers: insight models, `insightService`, a `useInsights` hook and presentational views.
> Show a per-country summary table (headcount, min, average, max in local currency), a country selector, job title and department breakdowns for the selected country, and a bar chart of average salary.
> Test the service, the hook and the stats table first, mocking the service layer.

## Notes

- **Accepted:** `useInsights` loads the country summary once, selects the first country, then loads both breakdowns in parallel and ignores stale responses when the user switches country quickly.
- **Accepted:** one reusable `SalaryStatsTable` for countries, job titles and departments; clicking a country row selects it.
- **Changed:** the original idea of one bar chart of average salary *across* countries was rejected. Bars in INR, JPY and USD side by side would be misleading (¥7M looks huge next to $120k). The chart shows average salary **by job title within the selected country**, so every bar shares one currency, which is stated in the title.
- **Accepted (chart design):** horizontal bars (long job-title labels), sorted by value, one validated colour, thin bars with a rounded end, value labels at the bar tip, a hover tooltip with range and headcount, recessive grid, and no legend for a single series. The tables double as the accessible table view.
- **Changed:** `App.test.tsx` now mocks both services, so no test makes a network call; opted into the React Router v7 future flags to silence deprecation notices.
