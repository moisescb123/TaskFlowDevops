# Proposal

## Why

Developer sets priority High/Medium/Low with visible card indicator. (RF06; story `us10-task-priority`).

## What Changes

- Implement the behavior described in `US/us10.md` Enhanced section.
- Align API with `docs/api-spec.yml` (`priority on POST/PUT /api/tasks`).
- Pytest for acceptance scenarios; Developer allowed, Viewer forbidden where applicable.

## Non-goals

- Unrelated CRUD/status features covered by sibling US stories.
- Auth registration/login except as dependency.
- CI/CD pipelines.

## Capabilities

### New Capabilities

- `task-priority`: Developer sets priority High/Medium/Low with visible card indicator.

### Modified Capabilities

- (none — may integrate into `task-management` at archive time if consolidated)

## Impact

- Task services/routes, board UI controls as needed, Pytest, docs; depends on auth and Task model.
