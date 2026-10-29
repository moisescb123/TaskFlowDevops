# Tasks

## 0. Feature branch

- [x] 0.1 Create and switch to branch `feature/us01-user-login` before any implementation commits (verify with `git branch --show-current`)

## 1. Project scaffold and User persistence

- [x] 1.1 Add Flask app skeleton (`app/`, config with `SECRET_KEY` from env, SQLite path) so `flask --app app run` starts — verify app imports without error
- [x] 1.2 Implement `User` model/table per `docs/data-model.md` (`email`, `password_hash`, `full_name`, `role`) with create/get-by-email — verify schema via Pytest or SQLite inspect
- [x] 1.3 Add password hash helpers (Werkzeug or equivalent) and a seed/fixture helper that can create Admin/Developer/Viewer users for tests/demo — verify hashes are not plain text and users load by email

## 2. Login API (TDD)

- [x] 2.1 Write failing Pytest cases for `POST /api/auth/login`: success (AC1), invalid credentials (AC2), missing/invalid fields (AC3), response never includes password — verify tests fail for the right reason
- [x] 2.2 Implement `POST /api/auth/login` (validate, verify hash, create session, return User JSON) until login tests pass
- [x] 2.3 Write failing Pytest for `GET /api/auth/me` authenticated vs `401` unauthenticated — verify fail-first
- [x] 2.4 Implement `GET /api/auth/me` and session identity until tests pass (role present on user)

## 3. Authorization guard and placeholders

- [x] 3.1 Add `login_required` (or equivalent) returning `401` for protected API stubs — verify Pytest: unauthenticated call to a protected stub returns `401` (AC5)
- [x] 3.2 Add minimal placeholder pages/routes `/board` and `/admin/users` that require auth and redirect unauthenticated browsers to login — verify redirect behavior in test or manual check later
- [x] 3.3 On successful login response, document client redirect rules: `admin` → `/admin/users`, `developer`|`viewer` → `/board` — verify covered by frontend task below

## 4. Login UI

- [x] 4.1 Implement `templates/login.html` + CSS/JS: email/password form, clear validation vs auth errors (RNF03), call `POST /api/auth/login`, store/use session cookie, redirect by role — verify happy path and error messaging in browser during E2E step
- [x] 4.2 Ensure authenticated visit to login redirects to role landing (or stays signed in per US01) — verify in E2E

## 5. Group verification for auth module

- [x] 5.1 Review and update unit tests for auth/user modules after UI/guard changes (MANDATORY review) — verify suite still matches AC1–AC5
- [x] 5.2 Run unit tests and verify DB state; write report `openspec/changes/us01-user-login/reports/YYYY-MM-DD-step-5.2-unit-test-and-db-verification.md` (MANDATORY; agent executes) — verify report exists and tests pass
- [x] 5.3 Manual endpoint testing with curl for login success/failure/validation and `/api/auth/me`; restore DB/session state; write report `openspec/changes/us01-user-login/reports/YYYY-MM-DD-step-5.3-curl-endpoint-testing.md` (MANDATORY; agent executes)
- [x] 5.4 E2E with Playwright MCP: open login, invalid login shows error, valid login redirects by role, protected page without session goes to login (MANDATORY; agent executes); write report under `openspec/changes/us01-user-login/reports/`
- [x] 5.5 Update technical docs as needed (`docs/api-spec.yml` consistency, `docs/development_guide.md` run/seed notes) (MANDATORY)

## 6. CI hook for auth tests

- [x] 6.1 Add or extend `.github/workflows/ci.yml` to install deps and run Pytest so auth tests run on push/PR (supports RN03 later) — verify workflow file is valid YAML and invokes Pytest

## Workflow follow-up

- After apply/verify: archive change with `/opsx:archive` when the team accepts US01
- US02 (logout) and US03 (register users) remain separate changes
