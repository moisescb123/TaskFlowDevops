# Proposal

## Why

Developer assigns a single registered user as task owner (RN01). (RF04 RN01; story `us08-assign-task-owner`).

## What Changes

- Implement the behavior described in `US/us08.md` Enhanced section.
- Align API with `docs/api-spec.yml` (`POST/PUT tasks with assignee_id`).
- Pytest for acceptance scenarios; Developer allowed, Viewer forbidden where applicable.

## Non-goals

- Unrelated CRUD/status features covered by sibling US stories.
- Auth registration/login except as dependency.
- CI/CD pipelines.

## Capabilities

### New Capabilities

- `assign-owner`: Developer assigns a single registered user as task owner (RN01).

### Modified Capabilities

- (none — may integrate into `task-management` at archive time if consolidated)

## Impact

- Task services/routes, board UI controls as needed, Pytest, docs; depends on auth and Task model.
