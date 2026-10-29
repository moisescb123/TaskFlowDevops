# Proposal

## Why

Developer updates existing task fields while enforcing RN02. (RF02; story `us06-edit-task`).

## What Changes

- Implement the behavior described in `US/us06.md` Enhanced section.
- Align API with `docs/api-spec.yml` (`PUT /api/tasks/{taskId}`).
- Pytest for acceptance scenarios; Developer allowed, Viewer forbidden where applicable.

## Non-goals

- Unrelated CRUD/status features covered by sibling US stories.
- Auth registration/login except as dependency.
- CI/CD pipelines.

## Capabilities

### New Capabilities

- `edit-task`: Developer updates existing task fields while enforcing RN02.

### Modified Capabilities

- (none — may integrate into `task-management` at archive time if consolidated)

## Impact

- Task services/routes, board UI controls as needed, Pytest, docs; depends on auth and Task model.
