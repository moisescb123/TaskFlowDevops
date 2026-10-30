# Proposal

## Why

Authenticated sessions from US01 must be terminable so users can protect access to TaskFlow DevOps when leaving a device (US02).

## What Changes

- Add logout that clears Flask session data and expires the session cookie.
- Redirect to login after logout; protected resources require a new login.
- Expose logout for Admin, Developer, and Viewer.
- Pytest coverage for logout success, cookie expiry, and unauthenticated logout.

## Non-goals

- Login (US01), registration (US03), idle timeout, logout-all-devices, server-side session denylist / cryptographic revocation of stolen cookies.

## Capabilities

### New Capabilities

- `user-logout`: End an authenticated session and return the client to an unauthenticated state safely.

### Modified Capabilities

- (none in main specs yet; apply after `us01-user-login` / `user-auth`)

## Impact

- `POST /api/auth/logout`, session helpers, header logout control, Pytest; depends on US01 sessions.
