# Tasks

## 0. Feature branch

- [x] 0.1 Create and switch to `feature/us03-user-registration`

## 1. API (TDD)

- [x] 1.1 Failing Pytest: create success, duplicate, validation, 403, 401
- [x] 1.2 Implement `POST /api/users` until tests pass
- [x] 1.3 Implement Admin `GET /api/users` without password fields

## 2. Admin UI + seed

- [x] 2.1 Admin users page (form + list)
- [x] 2.2 Non-Admin cannot access management UI
- [x] 2.3 Seed initial Admin when empty — verify login works

## 8. Mandatory verification

- [x] 8.1 Review and update unit tests affected by this change — verify coverage matches ACs
- [x] 8.2 Run Pytest and verify DB/state; write `openspec/changes/us03-user-registration/reports/YYYY-MM-DD-step-8.2-unit-test-and-db-verification.md` (agent executes)
- [x] 8.3 Manual curl testing of new/changed endpoints; restore state; write `openspec/changes/us03-user-registration/reports/YYYY-MM-DD-step-8.3-curl-endpoint-testing.md` (agent executes)
- [x] 8.4 E2E with Playwright MCP for user-facing flow; write report under `openspec/changes/us03-user-registration/reports/` (agent executes)
- [x] 8.5 Update technical documentation (`docs/api-spec.yml`, `docs/data-model.md`, and/or `docs/development_guide.md` as applicable)

## Workflow follow-up

- Archive with `/opsx:archive` after verify when accepted
- Prefer applying after dependent changes (e.g. login before logout/registration; tasks after auth)
