# Tasks

## 0. Feature branch

- [x] 0.1 Create and switch to `feature/us09-task-status-transitions`

## 1. Implement `status-transitions` (TDD)

- [x] 1.1 Write failing Pytest scenarios from the spec
- [x] 1.2 Implement API/domain changes until tests pass
- [x] 1.3 Wire board UI controls if user-facing for this story

## 8. Mandatory verification

- [x] 8.1 Review and update unit tests affected by this change — verify coverage matches ACs
- [x] 8.2 Run Pytest and verify DB/state; write `openspec/changes/us09-task-status-transitions/reports/YYYY-MM-DD-step-8.2-unit-test-and-db-verification.md` (agent executes)
- [x] 8.3 Manual curl testing of new/changed endpoints; restore state; write `openspec/changes/us09-task-status-transitions/reports/YYYY-MM-DD-step-8.3-curl-endpoint-testing.md` (agent executes)
- [x] 8.4 E2E with Playwright MCP for user-facing flow; write report under `openspec/changes/us09-task-status-transitions/reports/` (agent executes)
- [x] 8.5 Update technical documentation (`docs/api-spec.yml`, `docs/data-model.md`, and/or `docs/development_guide.md` as applicable)

## Workflow follow-up

- Archive with `/opsx:archive` after verify when accepted
- Prefer applying after dependent changes (e.g. login before logout/registration; tasks after auth)
