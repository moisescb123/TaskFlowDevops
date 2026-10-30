# Development Guide — TaskFlow DevOps

Setup and workflow for the academic TaskFlow DevOps project.

## Prerequisites

- Python 3.11 or higher
- Git
- Node.js 20.19+ (for OpenSpec CLI only)
- A GitHub account (for remote repo, Actions, and branch protection)

## Spec-Driven Workflow (Specboot + OpenSpec)

This repository uses Specboot standards under `docs/` and `ai-specs/`, with OpenSpec for change management.

1. Install OpenSpec globally: `npm install -g @fission-ai/openspec@latest`
2. Project is already initialized (`openspec/` present). Verify with `openspec doctor`.
3. Recommended flow:
   - `/enrich-us` (optional) → `/openspec-propose` or `/ff` → `/apply` → `/verify` → `/adversarial-review` → `/archive` → `/commit`
4. Keep `openspec/config.yaml` aligned with `docs/` when the stack or domain changes.

## Application Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python scripts/seed_users.py
pytest
flask --app app run
```

Default local URL: `http://localhost:5000`

SQLite file defaults to `taskflow.db` in the project root (`DATABASE_PATH`). Tests use an isolated temp database.

### Demo users (local only, US01 / US03 seed)

Created by `python scripts/seed_users.py` when those emails are missing (bootstrap Admin for empty DBs):

| Email | Password | Role |
|-------|----------|------|
| admin@taskflow.local | Admin123! | admin |
| dev@taskflow.local | Dev123! | developer |
| viewer@taskflow.local | Viewer123! | viewer |

Post-login redirects: Admin → `/admin/users`; Developer/Viewer → `/board`.

### Auth API (US01 / US02)

- `POST /api/auth/login` — `{ "email", "password" }`
- `POST /api/auth/logout` — clear session data and expire the session cookie → `204` (or `401` if not authenticated). Uses Flask client-signed cookies (no server denylist).
- `GET /api/auth/me` — current session user
- Login UI: `/login`
- Logout control: shared header button on `/board` and `/admin/users`

### Task board (US04–US11)

- `GET /api/tasks` — authenticated list of tasks
- `POST /api/tasks` — Developer-only create `{ "title", "priority", "due_date", "assignee_id?" }` → `201` To Do task (RN02); Admin/Viewer `403`
- `GET /api/tasks/{taskId}` — authenticated task detail
- `PUT /api/tasks/{taskId}` — Developer-only update title/priority/due_date/assignee (US06/US08/US10/US11, RN01/RN02); Admin/Viewer `403`
- `DELETE /api/tasks/{taskId}` — Developer-only hard delete → `204`; Admin/Viewer `403`; missing id `404`
- `PATCH /api/tasks/{taskId}/status` — Developer-only `{ "status" }` with RN04 (no `todo` → `done`); Admin/Viewer `403`
- Board UI: `/board` with Create/Edit/Delete, Start/Complete/Reopen, priority badges (US10), and due dates (`YYYY-MM-DD`, US11)
- Viewer: read-only (`data-can-mutate=false`); mutating task APIs return `403`
- Tasks persist in SQLite `tasks` table across restarts; deleted rows do not return after restart; at most one `assignee_id` (RN01)

### User management API (US03 / US08)

- `POST /api/users` — Admin creates `{ "email", "password", "full_name", "role" }` → `201` public `User`
- `GET /api/users` — Admin and Developer list users (no password fields); Developer uses this for assignee picker; Viewer `403`
- Admin UI: `/admin/users` (registration form + user table)
- Anonymous callers receive `401`

## Environment

Copy `.env.example` to `.env` (do not commit secrets). **`SECRET_KEY` is required** for non-testing runs; the app refuses to start with a missing or placeholder key.

```env
FLASK_ENV=development
SECRET_KEY=change-me-to-a-long-random-value
DATABASE_PATH=taskflow.db
```

## CI/CD (US12)

Continuous integration runs on GitHub Actions so Developers get automatic validation on every integrate.

### What runs

Workflow file: `.github/workflows/ci.yml` (versioned in the repo).

| Item | Value |
|------|--------|
| Workflow name | `CI` |
| Job check name | `Pytest` (visible on commit/PR checks) |
| Triggers | `push` and `pull_request` |
| Runner | `ubuntu-latest` |
| Python | 3.11 (with pip cache) |
| Steps | Checkout → set up Python → `pip install -r requirements.txt` → `pytest` |

### Developer steps

1. Push commits or open/update a pull request.
2. Open the commit or PR **Checks** tab on GitHub; a run named **CI** / **Pytest** should start automatically.
3. Wait for green before merging. On failure, open the failed run and expand the step that failed (Install dependencies or Run Pytest) — logs identify the failing step.
4. Reproduce locally with the same commands CI uses:

```bash
pip install -r requirements.txt
pytest
```

### Related (later stories)

- Deploy only after successful verification (US15).

## Branch protection (US14)

RN03: protect `main` so merges require a green automated test check.

| Item | Value |
|------|--------|
| Protected branch | `main` |
| Required status check | **`Pytest`** (job name in `.github/workflows/ci.yml`) |
| Ops guide | [`docs/branch-protection.md`](branch-protection.md) (Rulesets, classic UI, `gh` API) |

### Developer steps

1. Open a pull request targeting **`main`** (avoid direct pushes).
2. Wait for the **Pytest** check to pass.
3. If **Pytest** fails, merge stays blocked until the suite is fixed.
4. Repo **Admins** apply or update protection using `docs/branch-protection.md` (requires GitHub admin rights).

### Default branch

Prefer **`main`** as the repository default branch so PR targets and RN03 align.

## Automated testing (US13)

Pytest is the project’s automated verification suite. CI (US12) runs it after installing dependencies so failing tests fail the check before merge.

### Suite layout

| Path | Role |
|------|------|
| `pytest.ini` | `testpaths = tests`, `pythonpath = .` |
| `tests/conftest.py` | Isolated temp SQLite DB per test (`TESTING=True`) |
| `tests/test_*.py` | Feature/API coverage (auth, users, tasks, CI structure) |

### Business-rule coverage (as features landed)

| Rule | Covered by (examples) | Notes |
|------|----------------------|--------|
| RN01 (single assignee) | `tests/test_task_assignee.py` | |
| RN02 (title, due date, priority required) | `tests/test_task_create.py`, `tests/test_task_priority.py`, `tests/test_task_due_date.py` | |
| RN03 (protect main / green tests) | CI check **`Pytest`** + `docs/branch-protection.md` | GitHub settings (US14) |
| RN04 (no To Do → Done skip) | `tests/test_task_status.py` | |

### Developer steps (local parity with CI)

Use the same commands as the CI **Run Pytest** step:

```bash
pip install -r requirements.txt
pytest
```

- Green locally should match a green **Pytest** check on GitHub when the suite and dependencies match.
- A failing test fails the CI job (non-zero exit) so the PR check stays red until fixed.

## Project References

| Path | Purpose |
|------|---------|
| `US/us01.md`–`US/us15.md` | User stories |
| `Avance_Proyecto_Grupo_1_corregido.md` | Academic avance (RF, RNF, RN) |
| `docs/` | Technical context for agents |
| `openspec/` | Specs and change proposals |
| `ai-specs/` | Agents and Specboot skills |

## Conventional Commits

Use conventional commit messages in English, for example:

- `feat: add user login with session roles`
- `test: cover auth login acceptance criteria`
- `ci: run pytest on pull requests`
