# Design

## Context

See proposal.md and `US/us05.md`. Stack: Flask, SQLite, board UI.

## Goals / Non-Goals

**Goals:** Deliver `create-task` behavior with server-side enforcement and tests.
**Non-Goals:** Sibling task stories' primary features.

## Decisions

1. Follow `docs/api-spec.yml` and `docs/data-model.md` enums/fields.
2. Enforce authz for create: Developer only (`developer_required_api`); Admin and Viewer 403.
3. Prefer TDD Pytest before UI wiring.
4. Create form disables submit while the POST is in flight to prevent duplicate tasks.

## Risks / Trade-offs

- **[Apply order]** → Prefer US01/US03/US05 foundations before dependent stories.
