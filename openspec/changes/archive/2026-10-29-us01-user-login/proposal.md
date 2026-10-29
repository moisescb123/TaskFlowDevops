# Proposal

## Why

TaskFlow DevOps requires authenticated access so board and admin features can enforce Admin / Developer / Viewer capabilities. Without login (US01), users cannot establish a role-aware session, blocking the rest of the academic product and DevOps demonstration path.

## What Changes

- Add email/password login that creates a server session and returns the authenticated user including `role`.
- Add session introspection (`GET /api/auth/me`) for post-login checks.
- Add a login page (HTML/CSS/JS) with clear validation vs authentication errors.
- Protect subsequent board/admin entry points so unauthenticated callers receive `401` / redirect to login.
- Add Pytest coverage for US01 acceptance criteria (TDD).
- Align implementation with `docs/api-spec.yml` and `docs/data-model.md` (`User` with hashed password and role).

## Non-goals

- User registration and role assignment (US03).
- Logout (US02).
- Password reset, OAuth, MFA, or multi-device session revocation.
- Task board CRUD and DevOps CI/CD pipelines (later stories).
- Full production-hardened auth (rate limiting beyond academic needs, SSO).

## Capabilities

### New Capabilities

- `user-auth`: Authenticate users with email/password, establish and expose session identity and role, and deny unauthenticated access to protected resources.

### Modified Capabilities

- (none — no main specs exist yet)

## Impact

- **Code:** New Flask app scaffolding as needed (`app/` routes, auth service, user model, SQLite), login templates/static assets, Pytest suite.
- **API:** `POST /api/auth/login`, `GET /api/auth/me` per `docs/api-spec.yml`.
- **Data:** `User` persistence in SQLite (`email`, `password_hash`, `full_name`, `role`); seed or fixture users for login tests (creation UI is US03).
- **Security:** `SECRET_KEY` from environment; HttpOnly/SameSite session cookie; no plain-text passwords.
- **Dependencies:** Flask, SQLite driver/ORM as chosen in design, Werkzeug password hashing (or equivalent), Pytest.
- **Docs:** Keep `docs/api-spec.yml` / development guide consistent if paths or setup details are finalized during apply.
