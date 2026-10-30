# Proposal

## Why

Admins must register users and assign roles so login and role-based access work for a real team (US03).

## What Changes

- Admin-only user creation (email, password, full_name, role).
- Admin user list without password hashes.
- Admin UI; password hashing; Pytest for success, validation, duplicates, 403/401.

## Non-goals

- Self-registration, edit/deactivate users, password reset, login/logout.

## Capabilities

### New Capabilities

- `user-management`: Admin creates and lists users with assigned roles.

### Modified Capabilities

- (none)

## Impact

- `POST/GET /api/users`, Admin UI, authz, SQLite users, docs; depends on US01 auth.
