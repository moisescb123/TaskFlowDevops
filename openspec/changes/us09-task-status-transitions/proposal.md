# Proposal

## Why

Developer moves tasks across statuses with RN04 (no To Do → Done skip). (RF05 RN04; story `us09-task-status-transitions`).

## What Changes

- Implement the behavior described in `US/us09.md` Enhanced section.
- Align API with `docs/api-spec.yml` (`PATCH /api/tasks/{taskId}/status`).
- Pytest for acceptance scenarios; Developer allowed, Viewer forbidden where applicable.

## Non-goals

- Unrelated CRUD/status features covered by sibling US stories.
- Auth registration/login except as dependency.
- CI/CD pipelines.

## Capabilities

### New Capabilities

- `status-transitions`: Developer moves tasks across statuses with RN04 (no To Do → Done skip).

### Modified Capabilities

- (none — may integrate into `task-management` at archive time if consolidated)

## Impact

- Task services/routes, board UI controls as needed, Pytest, docs; depends on auth and Task model.
