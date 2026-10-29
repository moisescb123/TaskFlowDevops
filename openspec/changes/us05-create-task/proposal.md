# Proposal

## Why

Developer creates tasks in To Do with required title, priority, due date (RN02). (RF01; story `us05-create-task`).

## What Changes

- Implement the behavior described in `US/us05.md` Enhanced section.
- Align API with `docs/api-spec.yml` (`POST /api/tasks`).
- Pytest for acceptance scenarios; Developer allowed, Viewer forbidden where applicable.

## Non-goals

- Unrelated CRUD/status features covered by sibling US stories.
- Auth registration/login except as dependency.
- CI/CD pipelines.

## Capabilities

### New Capabilities

- `create-task`: Developer creates tasks in To Do with required title, priority, due date (RN02).

### Modified Capabilities

- (none — may integrate into `task-management` at archive time if consolidated)

## Impact

- Task services/routes, board UI controls as needed, Pytest, docs; depends on auth and Task model.
