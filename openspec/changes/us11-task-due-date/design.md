# Design

## Context

See proposal.md and `US/us11.md`. Stack: Flask, SQLite, board UI.

## Goals / Non-Goals

**Goals:** Deliver `task-due-date` behavior with server-side enforcement and tests.
**Non-Goals:** Sibling task stories' primary features.

## Decisions

1. Follow `docs/api-spec.yml` and `docs/data-model.md` enums/fields.
2. Enforce authz: Developer mutate; Viewer 403.
3. Prefer TDD Pytest before UI wiring.

## Risks / Trade-offs

- **[Apply order]** → Prefer US01/US03/US05 foundations before dependent stories.
