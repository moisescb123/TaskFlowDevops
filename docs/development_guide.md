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

### Demo users (local only, US01)

Created by `python scripts/seed_users.py`:

| Email | Password | Role |
|-------|----------|------|
| admin@taskflow.local | Admin123! | admin |
| dev@taskflow.local | Dev123! | developer |
| viewer@taskflow.local | Viewer123! | viewer |

Post-login redirects: Admin → `/admin/users`; Developer/Viewer → `/board`.

### Auth API (US01)

- `POST /api/auth/login` — `{ "email", "password" }`
- `GET /api/auth/me` — current session user
- Login UI: `/login`

## Environment

Copy `.env.example` to `.env` (do not commit secrets). **`SECRET_KEY` is required** for non-testing runs; the app refuses to start with a missing or placeholder key.

```env
FLASK_ENV=development
SECRET_KEY=change-me-to-a-long-random-value
DATABASE_PATH=taskflow.db
```

## CI/CD

- Workflow `.github/workflows/ci.yml` installs dependencies and runs Pytest on push and pull requests.
- Protect `main` so merges require a green CI check (RN03 / US14).
- Deploy only after successful verification (US15).

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
