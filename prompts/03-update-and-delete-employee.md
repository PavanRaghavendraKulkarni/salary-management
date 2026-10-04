# Phase 3: Update and delete (TDD)

## Prompt

> Using TDD, add updating (PUT) and deleting an employee. Tests first: update changes fields and refreshes `updated_at`; update with another employee's email returns 409; updating to your own email is allowed; update of an unknown id returns 404; delete returns 204 with an empty body; a deleted employee can no longer be fetched; delete of an unknown id returns 404.
> Reuse the existing validation; do not duplicate it.

## Notes

- **Accepted:** `update_employee` calls the same private `_validated_values` as create, so currency, hire-date and email rules have one implementation.
- **Accepted:** PUT replaces every editable field, matching the form that always sends the full record.
- **Changed:** the email-uniqueness check takes `excluding_employee_id`, otherwise saving an unchanged record would fail with 409. Added a test for it.
- **Rejected:** soft delete. Audit history is out of scope, so a hard delete is simpler and honest.
