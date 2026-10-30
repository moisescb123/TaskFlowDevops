# Design

## Context

Depends on User model and Admin session from US01. See proposal.md.

## Goals / Non-Goals

**Goals:** Secure Admin registration API + UI; hashed passwords; role enum.
**Non-Goals:** Profile editing, email invites.

## Decisions

1. Admin-only authz for `POST /api/users` and management UI.
2. Same password hashing as US01.
3. Seed script for bootstrap Admin when DB empty.

## Risks / Trade-offs

- **[No Admin yet]** → Seed initial Admin.
- **[US01 missing]** → Apply after login/guards.
