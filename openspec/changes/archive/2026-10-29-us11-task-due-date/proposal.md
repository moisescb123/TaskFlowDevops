# Proposal

## Why

Developer sets a required due date for planning deadlines. (RF07; story `us11-task-due-date`).

## What Changes

- Implement the behavior described in `US/us11.md` Enhanced section.
- Align API with `docs/api-spec.yml` (`due_date on POST/PUT /api/tasks`).
- Pytest for acceptance scenarios; Developer allowed, Viewer forbidden where applicable.

## Non-goals

- Unrelated CRUD/status features covered by sibling US stories.
- Auth registration/login except as dependency.
- CI/CD pipelines.

## Capabilities

### New Capabilities

- `task-due-date`: Developer sets a required due date for planning deadlines.

### Modified Capabilities

- (none — may integrate into `task-management` at archive time if consolidated)

## Impact

- Task services/routes, board UI controls as needed, Pytest, docs; depends on auth and Task model.
