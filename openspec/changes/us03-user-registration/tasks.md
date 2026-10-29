# Tasks

## 0. Feature branch

- [ ] 0.1 Create and switch to `feature/us03-user-registration`

## 1. API (TDD)

- [ ] 1.1 Failing Pytest: create success, duplicate, validation, 403, 401
- [ ] 1.2 Implement `POST /api/users` until tests pass
- [ ] 1.3 Implement Admin `GET /api/users` without password fields

## 2. Admin UI + seed

- [ ] 2.1 Admin users page (form + list)
- [ ] 2.2 Non-Admin cannot access management UI
- [ ] 2.3 Seed initial Admin when empty — verify login works

## 8. Mandatory verification

- [ ] 8.1 Review and update unit tests affected by this change — verify coverage matches ACs
- [ ] 8.2 Run Pytest and verify DB/state; write `openspec/changes/us03-user-registration/reports/YYYY-MM-DD-step-8.2-unit-test-and-db-verification.md` (agent executes)
- [ ] 8.3 Manual curl testing of new/changed endpoints; restore state; write `openspec/changes/us03-user-registration/reports/YYYY-MM-DD-step-8.3-curl-endpoint-testing.md` (agent executes)
- [ ] 8.4 E2E with Playwright MCP for user-facing flow; write report under `openspec/changes/us03-user-registration/reports/` (agent executes)
- [ ] 8.5 Update technical documentation (`docs/api-spec.yml`, `docs/data-model.md`, and/or `docs/development_guide.md` as applicable)

## Workflow follow-up

- Archive with `/opsx:archive` after verify when accepted
- Prefer applying after dependent changes (e.g. login before logout/registration; tasks after auth)
