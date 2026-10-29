# Tasks

## 0. Feature branch

- [ ] 0.1 Create and switch to `feature/us04-task-board-view`

## 1. List API + board UI

- [ ] 1.1 Ensure Task persistence exists or minimal schema for empty list — verify migrations/init
- [ ] 1.2 Pytest: authenticated GET /api/tasks; anonymous 401; Viewer mutate still 403 if endpoints exist
- [ ] 1.3 Implement board UI columns + card fields; Viewer hides mutate controls

## 8. Mandatory verification

- [ ] 8.1 Review and update unit tests affected by this change — verify coverage matches ACs
- [ ] 8.2 Run Pytest and verify DB/state; write `openspec/changes/us04-task-board-view/reports/YYYY-MM-DD-step-8.2-unit-test-and-db-verification.md` (agent executes)
- [ ] 8.3 Manual curl testing of new/changed endpoints; restore state; write `openspec/changes/us04-task-board-view/reports/YYYY-MM-DD-step-8.3-curl-endpoint-testing.md` (agent executes)
- [ ] 8.4 E2E with Playwright MCP for user-facing flow; write report under `openspec/changes/us04-task-board-view/reports/` (agent executes)
- [ ] 8.5 Update technical documentation (`docs/api-spec.yml`, `docs/data-model.md`, and/or `docs/development_guide.md` as applicable)

## Workflow follow-up

- Archive with `/opsx:archive` after verify when accepted
- Prefer applying after dependent changes (e.g. login before logout/registration; tasks after auth)
