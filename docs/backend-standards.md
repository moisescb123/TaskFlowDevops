---
description: Backend development standards for TaskFlow DevOps (Python, Flask, SQLite, Pytest, GitHub Actions).
globs: ["**/*.py", "**/requirements*.txt", "**/.github/workflows/**/*.{yml,yaml}", "**/pytest.ini", "**/pyproject.toml"]
alwaysApply: true
---

# Backend Standards — TaskFlow DevOps

## Technology Stack

| Area | Choice |
|------|--------|
| Language | Python 3.11+ |
| Web framework | Flask |
| Database | SQLite |
| Tests | Pytest |
| VCS / CI | Git, GitHub, GitHub Actions |
| Auth | Session-based or token-based login with role checks (Admin, Developer, Viewer) |

## Architecture

Organize the application into clear layers so changes stay localized (RNF01 — maintainability):

1. **Presentation** — Flask routes / controllers, request/response mapping
2. **Business logic** — task rules, authz by role, RN01–RN04
3. **Data access** — SQLite persistence

Keep business rules out of templates and out of raw SQL scattered in routes.

## Coding Standards

- Prefer clear module and function names; avoid abbreviations.
- Use type hints on public functions.
- Validate and sanitize all user input before persistence (RNF05).
- Return clear error messages for invalid or incomplete input (RNF03).
- Do not commit secrets; use environment variables for configuration.
- Persist data so it survives application restart (RNF02).

## Domain Rules (must be enforced server-side)

- **RN01**: A task has at most one primary assignee (registered user).
- **RN02**: Creating/updating a task requires title, due date, and priority (High / Medium / Low).
- **RN03**: No merge to `main` and no production deploy if automated Pytest suite fails (enforced via CI + branch protection).
- **RN04**: A task cannot move directly from `To Do` to `Done`; it must pass through `In progress`.

## Roles and Authorization

| Role | Capabilities |
|------|----------------|
| Admin | Manage users and assign roles; access configuration |
| Developer | Create, edit, delete tasks; assign responsible; change state/priority/due date |
| Viewer | Read-only access to the board |

Unauthenticated users cannot access protected board or admin endpoints.

## Testing (Pytest)

- Write failing tests first for new behavior (TDD).
- Cover business rules RN01–RN04 and authz by role.
- Prefer fast unit/integration tests that exercise Flask app context and SQLite (in-memory or temp DB in tests).
- CI must run the same Pytest suite via GitHub Actions on push and pull request.

## CI/CD Expectations

- GitHub Actions workflow installs dependencies and runs Pytest.
- Required checks protect `main` (RN03).
- Optional CD step deploys only after successful verification to a Flask-compatible host.

## API Consistency

- Follow [api-spec.yml](./api-spec.yml) when adding or changing endpoints.
- Keep entity shapes aligned with [data-model.md](./data-model.md).
