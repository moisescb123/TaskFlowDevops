# Design

## Context

See proposal.md. Board may show empty until US05 creates tasks; list endpoint still required.

## Goals / Non-Goals

**Goals:** Readable board + Viewer read-only enforcement.
**Non-Goals:** Drag-and-drop mutations (US09).

## Decisions

1. `GET /api/tasks` returns all tasks; client groups by `status`.
2. Hide/disable mutate controls for `viewer` role in JS/templates; still enforce 403 server-side.
3. Placeholder empty state when no tasks.

## Risks / Trade-offs

- **[No Task table yet]** → Coordinate apply order with US05 or include minimal Task schema here for list-empty.
