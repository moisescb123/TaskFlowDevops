# Proposal

## Why

Viewers (and other authenticated users) need a status-organized board to see progress without Viewer mutating data (US04 / RF08).

## What Changes

- Authenticated board UI with To Do / In progress / Done columns.
- `GET /api/tasks` for board data; Viewer read-only (no mutate controls; writes 403).
- Persist tasks across restart (RNF02); browser compatibility (RNF04).

## Non-goals

- Create/edit/delete/move tasks (US05–US11); DevOps pipelines.

## Capabilities

### New Capabilities

- `task-board`: Present tasks grouped by status for authenticated users with Viewer read-only constraints.

### Modified Capabilities

- (none)

## Impact

- Board templates/CSS/JS, list tasks API, authz; depends on auth + Task model (may land with create story).
