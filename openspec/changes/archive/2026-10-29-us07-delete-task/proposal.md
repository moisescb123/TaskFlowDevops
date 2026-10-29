# Proposal

## Why

Developer deletes tasks after confirmation so obsolete work is removed. (RF03; story `us07-delete-task`).

## What Changes

- Implement the behavior described in `US/us07.md` Enhanced section.
- Align API with `docs/api-spec.yml` (`DELETE /api/tasks/{taskId}`).
- Pytest for acceptance scenarios; Developer allowed, Viewer forbidden where applicable.

## Non-goals

- Unrelated CRUD/status features covered by sibling US stories.
- Auth registration/login except as dependency.
- CI/CD pipelines.

## Capabilities

### New Capabilities

- `delete-task`: Developer deletes tasks after confirmation so obsolete work is removed.

### Modified Capabilities

- (none — may integrate into `task-management` at archive time if consolidated)

## Impact

- Task services/routes, board UI controls as needed, Pytest, docs; depends on auth and Task model.
