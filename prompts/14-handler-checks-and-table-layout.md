# Phase 14: Handler type checks and table layout

## Prompt

> Before pushing, two more changes:
> 1. Replace the `assert isinstance` in `handle_domain_error` and `handle_request_validation_error` with explicit type checks that fall back to the unexpected-error handler, matching `handle_http_exception`. Add unit tests the same way. Use red and green commits.
> 2. Fix the breakdown table layout so the USD column is never cut off. Wrap the stats tables in a container that scrolls horizontally on narrow screens (MUI `TableContainer` with `overflowX: auto`), and keep the column header and the "approx. USD, as of" note readable. Check it manually at desktop width and at about 375px wide, and add or update a component test that the USD column header renders. Commit as `fix:`.
> 3. Add one line to `docs/tradeoffs.md`: unexpected errors are logged twice in production (by our handler and by uvicorn), accepted to keep the default server behavior.
>
> Run all checks, show git log, then push all commits to origin/main and confirm with git status.

## Notes

- **Accepted:** the existing handler test is parametrized over all three handlers; the two new cases failed with `AssertionError` before the fix. The test's handler type is `Coroutine[...]`, because `asyncio.run` needs a coroutine.
- **Changed:** a scrolling container alone would still hide the USD column on desktop, because the two breakdown tables sat side by side at half width (about 560 px for seven columns). They are now stacked at full width, so nothing scrolls at desktop width; at phone width each table scrolls on its own.
- **Accepted:** header cells use `white-space: nowrap`, so "Average (≈ USD)" stays on one line. The "as of" note sits outside the scrolling area, so it stays readable and wraps at 375 px.
- **Verified in headless Chrome** (driven over the DevTools protocol on 10,000 seeded rows). At 1400 px no table scrolls and every USD header is visible. At 375 px the page does not scroll sideways, each table scrolls, every USD header becomes visible after scrolling, and headers stay one line high.
- **Noticed, not changed:** at 375 px the navigation links run together and the salary chart is cramped.
