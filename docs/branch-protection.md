# Branch protection on `main` (US14 / RN03)

Protect `main` so merges require a green CI check and direct pushes are restricted.

## Required status check

| Item | Value |
|------|--------|
| Workflow file | `.github/workflows/ci.yml` |
| Workflow name | `CI` |
| **Required check name** | **`Pytest`** (job `name:` in the workflow) |
| Triggers | `push`, `pull_request` |

Do not require `CI`, `test`, or `Run Pytest` — GitHub’s required check must match the job display name **`Pytest`**.

## Recommended GitHub settings (Rulesets or classic Branch protection)

Apply as a repository **Admin** (Settings permission). Prefer **Rulesets** when available.

### Option A — Ruleset (recommended)

1. GitHub → **Settings** → **Rules** → **Rulesets** → **New branch ruleset**.
2. Name: `Protect main (RN03)`.
3. Enforcement: **Active**.
4. Target branches: include `main` (or `refs/heads/main`).
5. Rules:
   - **Restrict deletions**
   - **Block force pushes**
   - **Require a pull request before merging** (optional for academic repos; recommended)
   - **Require status checks to pass**: add **`Pytest`**
   - Optionally **Require branches to be up to date before merging**
6. Save.

### Option B — Classic branch protection

1. **Settings** → **Branches** → **Add branch protection rule**.
2. Branch name pattern: `main`.
3. Enable:
   - **Require status checks to pass before merging** → add **`Pytest`**
   - **Require branches to be up to date before merging** (recommended)
   - **Do not allow bypassing the above settings** / include administrators if the UI offers it
   - **Restrict who can push** / disallow direct pushes as team policy allows
4. Save changes.

### Option C — Admin CLI (`gh`)

Requires `admin:repo` (or equivalent). Example classic protection payload:

```bash
gh api --method PUT repos/OWNER/REPO/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Pytest"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

Verify:

```bash
gh api repos/OWNER/REPO/branches/main/protection
```

HTTP 404 means protection is not configured. HTTP 200 with `contexts` containing `Pytest` means the required check is set.

## Default branch note

The academic repo should use **`main`** as the GitHub **default branch** so protection and PR targets align with RN03. If another branch is still default, change it under **Settings → General → Default branch** after `main` is protected.

## Developer behavior

1. Open PRs into `main` (not direct push).
2. Wait for the **Pytest** check to pass.
3. If **Pytest** is red, merge stays blocked until the suite is fixed.
4. After merge, deploy (US15) should only follow a green `main`.

## Acceptance mapping (US14)

| AC | Expectation |
|----|-------------|
| AC1 | Failing **Pytest** → merge to `main` blocked |
| AC2 | Passing **Pytest** (+ other rules) → merge allowed |
| AC3 / RN03 | Merge (and later deploy) depend on passing automated tests |
| AC4 | Required check is **`Pytest`** |
