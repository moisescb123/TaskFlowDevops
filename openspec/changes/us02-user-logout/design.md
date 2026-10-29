# Design

## Context

See proposal.md. Builds on US01 Flask session cookies.

## Goals / Non-Goals

**Goals:** Session invalidation + UI logout for all roles.
**Non-Goals:** Multi-device session store, idle timeout.

## Decisions

1. `POST /api/auth/logout` clears Flask session — matches `docs/api-spec.yml`.
2. Shared header logout → API → redirect `/login`.
3. Unauthenticated logout returns `401` per API spec.

## Risks / Trade-offs

- **[US01 not applied]** → Apply after login scaffolding exists.
