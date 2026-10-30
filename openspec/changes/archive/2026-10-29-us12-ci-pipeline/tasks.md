# Tasks

## 0. Feature branch

- [x] 0.1 Create and switch to `feature/us12-ci-pipeline`

## 1. Deliver `ci-pipeline`

- [x] 1.1 Implement/configure artifacts for: .github/workflows/ci.yml
- [x] 1.2 Document Developer steps in `docs/development_guide.md`
- [x] 1.3 Verify pass/fail behavior matches the spec scenarios (agent executes)

## 8. Mandatory verification

- [x] 8.1 Review and update unit tests affected by this change — verify coverage matches ACs
- [x] 8.2 Run Pytest and verify DB/state; write `openspec/changes/us12-ci-pipeline/reports/YYYY-MM-DD-step-8.2-unit-test-and-db-verification.md` (agent executes)
- [x] 8.3 Verify pipeline/config artifacts; write `openspec/changes/us12-ci-pipeline/reports/YYYY-MM-DD-step-8.3-pipeline-verification.md` (agent executes)
- [x] 8.4 Skip browser E2E (no UI in this change); note N/A in verification report
- [x] 8.5 Update technical documentation (`docs/api-spec.yml`, `docs/data-model.md`, and/or `docs/development_guide.md` as applicable)

## Workflow follow-up

- Archive with `/opsx:archive` after verify when accepted
- Prefer applying after dependent changes (e.g. login before logout/registration; tasks after auth)
