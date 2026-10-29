# Tasks

## 0. Feature branch

- [ ] 0.1 Create and switch to `feature/us02-user-logout` (verify with `git branch --show-current`)

## 1. Logout API (TDD)

- [ ] 1.1 Write failing Pytest: authenticated logout then `/api/auth/me` → 401
- [ ] 1.2 Write failing Pytest: unauthenticated logout → 401
- [ ] 1.3 Implement `POST /api/auth/logout` until tests pass

## 2. Logout UI

- [ ] 2.1 Add logout control; call API; redirect to login
- [ ] 2.2 Expose logout for Admin, Developer, and Viewer layouts

## 8. Mandatory verification

- [ ] 8.1 Review and update unit tests affected by this change — verify coverage matches ACs
- [ ] 8.2 Run Pytest and verify DB/state; write `openspec/changes/us02-user-logout/reports/YYYY-MM-DD-step-8.2-unit-test-and-db-verification.md` (agent executes)
- [ ] 8.3 Manual curl testing of new/changed endpoints; restore state; write `openspec/changes/us02-user-logout/reports/YYYY-MM-DD-step-8.3-curl-endpoint-testing.md` (agent executes)
- [ ] 8.4 E2E with Playwright MCP for user-facing flow; write report under `openspec/changes/us02-user-logout/reports/` (agent executes)
- [ ] 8.5 Update technical documentation (`docs/api-spec.yml`, `docs/data-model.md`, and/or `docs/development_guide.md` as applicable)

## Workflow follow-up

- Archive with `/opsx:archive` after verify when accepted
- Prefer applying after dependent changes (e.g. login before logout/registration; tasks after auth)
