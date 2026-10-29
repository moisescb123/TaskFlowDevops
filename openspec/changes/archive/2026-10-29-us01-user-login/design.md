# Design

## Context

See `proposal.md` for motivation (US01 login). The repository is greenfield for application code; standards and contracts already exist in `docs/` (Flask, SQLite, HTML/CSS/JS, Pytest, `api-spec.yml`, `User` model). Registration UI is out of scope (US03), so login tests and local demos need a controlled way to insert users with hashed passwords (fixtures/seed script).

## Goals / Non-Goals

**Goals:**
- Deliver session-based login and `/api/auth/me` aligned with `docs/api-spec.yml`.
- Keep presentation, auth/business logic, and SQLite access separated (RNF01).
- Prefer TDD with Pytest for AC1–AC5 before wiring the UI.

**Non-Goals:**
- Designing logout, user admin, or task board beyond “protected until authenticated.”
- Choosing a production IdP or JWT-only API style for this academic slice.

## Decisions

1. **Session cookies over JWT for US01**
   - **Choice:** Flask server-side session (signed cookie) with `SECRET_KEY` from environment.
   - **Why:** Matches academic scope, simplifies `/api/auth/me`, and fits HttpOnly/SameSite guidance in US01.
   - **Alternative:** JWT in localStorage — rejected for XSS exposure and extra complexity.

2. **Password hashing**
   - **Choice:** Werkzeug `generate_password_hash` / `check_password_hash` (or equivalent strong hash API).
   - **Why:** Standard with Flask; no plain-text storage.
   - **Alternative:** Custom hashing — rejected.

3. **Persistence**
   - **Choice:** SQLite table `users` per `docs/data-model.md`.
   - **Why:** Project standard; survives restart (RNF02) for user records.
   - **Seed for login without US03:** test fixtures + optional `scripts/seed_users.py` (or Flask CLI) creating demo Admin/Developer/Viewer accounts. Not a public registration endpoint.

4. **App layout**
   - **Choice:** Lightweight package layout, e.g. `app/` with `routes/auth.py`, `services/auth_service.py`, `models/user.py`, `db.py`, plus `templates/login.html` and `static/js/login.js`.
   - **Why:** Matches expected modules in US01 and layered standards.
   - **Alternative:** Single-file Flask app — acceptable only as a temporary spike; prefer modular from the start for maintainability.

5. **API shape**
   - **Choice:** JSON `POST /api/auth/login` and `GET /api/auth/me` as in `docs/api-spec.yml`; login page may also post via fetch to the same API.
   - **Why:** Single contract for UI and Pytest.

6. **Post-login redirects**
   - **Choice:** Client redirects by role: Admin → admin users placeholder/config route; Developer/Viewer → board placeholder route. Placeholders may be minimal pages until US03/US04 land.
   - **Why:** Satisfies US01 behavior without implementing full board/admin features.

7. **Protecting resources**
   - **Choice:** Shared `login_required` dependency/decorator returning `401` for API; UI routes redirect to login. `/admin/users` additionally requires `admin` role (`admin_required_page`); non-admins redirect to `/board`.
   - **Why:** AC5 and role-aware admin entry; future stories reuse the same guards.

8. **Login attempts clear prior session**
   - **Choice:** Every `POST /api/auth/login` calls `clear_session()` before validate/authenticate; only success calls `establish_session`.
   - **Why:** Failed re-login must not leave a stale authenticated session.

## Risks / Trade-offs

- **[No registration yet]** → Demo/seed users required; document credentials for local use only, never commit real secrets.
- **[Placeholder board/admin pages]** → Login redirects may hit stubs; acceptable until later US stories.
- **[Session fixation / CSRF]** → Use Flask session regeneration on login; prefer SameSite cookie; full CSRF tokens can be added if form posts are used beyond JSON+same-site fetch.
- **[SQLite concurrency]** → Fine for academic single-demo deploy; not a production scale target.

## Migration Plan

- Fresh DB schema create on startup or via init script.
- No production data migration (greenfield).
- Rollback: remove auth routes/UI and drop session usage; SQLite file can be deleted in local/dev.

## Open Questions

- Exact placeholder paths for Admin vs board after login (`/admin/users` vs `/board`) — finalize during apply to match templates; does not change login requirements.
