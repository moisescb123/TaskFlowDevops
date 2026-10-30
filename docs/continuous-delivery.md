# Continuous delivery (US15)

Deploy TaskFlow to a Flask-compatible demo host **after** CI succeeds on `main` (RN03).

## Platform choice

This project uses **Render** (Python web service):

| Artifact | Role |
|----------|------|
| `.github/workflows/cd.yml` | CD workflow: runs only when workflow **CI** completes with **success** on `main` |
| `render.yaml` | Render Blueprint for the web service |
| `Procfile` / `wsgi.py` | Process start (`gunicorn wsgi:app`) |
| GitHub secret `RENDER_DEPLOY_HOOK` | Deploy Hook URL (never commit the URL) |

## One-time setup (repo Admin)

1. Merge CD artifacts to `main` (after green **Pytest**).
2. In [Render](https://render.com): **New** → **Blueprint** → select this repo (or create a Python **Web Service** using `render.yaml` / start command `gunicorn --bind 0.0.0.0:$PORT wsgi:app`).
3. Set environment variables on the service:
   - `SECRET_KEY` — strong random value (required)
   - `FLASK_ENV=production` (optional; Blueprint sets it)
   - `DATABASE_PATH=taskflow.db` (SQLite on the instance; ephemeral on free tier)
4. Open the service → **Settings** → **Deploy Hook** → copy the URL.
5. In GitHub: **Settings** → **Secrets and variables** → **Actions** → New repository secret:
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: the Deploy Hook URL
6. Smoke: merge a trivial change to `main` (or re-run **CI** on `main`) so CD runs after green **CI**. There is no manual CD dispatch — that would bypass RN03.

## Developer flow

1. Open a PR → wait for **Pytest** (US12/US13).
2. Merge to `main` only when checks are green (US14).
3. CI runs on `main`; on **success**, CD triggers and calls the Render deploy hook.
4. If CI **fails**, CD does **not** deploy that run.
5. Open the Render service URL (login `/login`, board after auth).

## Secrets policy (AC4)

- Do **not** commit deploy hooks, API tokens, or production `SECRET_KEY`.
- Use GitHub Actions secrets and the host’s Environment UI only.
- `.env` stays local and gitignored.

## Failure modes

| Situation | Result |
|-----------|--------|
| CI red on `main` | CD job skipped (`conclusion != success`) |
| CI green on a non-`main` branch | CD job skipped (`head_branch` must be `main`) |
| `RENDER_DEPLOY_HOOK` missing | CD fails with a clear error (configure the secret) |
| Hook URL revoked | CD curl fails; fix secret / Render service |
