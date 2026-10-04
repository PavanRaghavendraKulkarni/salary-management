# Phase 1: Requirements and design docs

## Prompt

> Write `docs/requirements.md` (one page at most): goal, user persona, problem, in-scope features, out-of-scope items with a reason for each, assumptions, and success criteria.
> Then write `docs/design.md`: data model, API list, each MVC layer's responsibility, and a Mermaid architecture diagram.
> Use the engineering instructions as the source of truth. Keep both concise. No code.

## Notes

- **Accepted:** one-page requirements; Mermaid diagram showing the request flow through each layer.
- **Changed:** added a `GET /meta/reference-data` endpoint to the design so the frontend form gets allowed values and the country-to-currency mapping from the backend, instead of duplicating backend constants in TypeScript. Recorded as an assumption.
- **Changed:** money is serialised as a decimal string in JSON to avoid float rounding; recorded in the design.
