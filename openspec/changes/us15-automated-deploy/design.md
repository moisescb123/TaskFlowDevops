# Design

## Context

See proposal.md. App code may evolve in parallel; CI must run whatever Pytest suite exists.

## Goals / Non-Goals

**Goals:** Reliable automation for `continuous-delivery` within academic constraints.
**Non-Goals:** Complex release orchestration.

## Decisions

1. GitHub Actions as CI/CD engine per project standards.
2. Required check name must match workflow for US14.
3. Flask-compatible single demo host for US15 (team picks one platform at apply).

## Risks / Trade-offs

- **[Empty test suite early]** → US13 grows with features; CI still must invoke Pytest.
- **[Branch protection is repo settings]** → Document manual GitHub UI/ruleset steps in tasks/reports.
