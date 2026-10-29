# Design

## Context

See proposal.md. Builds on US01 Flask **client-signed** session cookies (no server session table).

## Goals / Non-Goals

**Goals:** Clear session + expire cookie + UI logout for all roles.
**Non-Goals:** Multi-device session store, idle timeout, server-side cookie denylist / logout-all-devices.

## Decisions

1. `POST /api/auth/logout` calls `session.clear()` and returns `204` so Flask emits an expired session cookie — matches `docs/api-spec.yml`.
2. Shared header logout → API → redirect `/login` only on `204` or `401` (do not redirect on unexpected errors).
3. Unauthenticated logout returns `401` per API spec.
4. **Cookie-session semantics:** “End session” means clear server-side session *data for this request* and expire the browser cookie. Stolen cookie replay until natural cookie lifetime remains possible without a denylist; accepted for this academic stack and listed as a non-goal above.

## Risks / Trade-offs

- **[US01 not applied]** → Apply after login scaffolding exists.
- **[Cookie replay after logout]** → Mitigated for normal browsers by `Max-Age=0`; residual risk for copied cookies documented; revocation deferred.
