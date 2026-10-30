# Proposal

## Why

Execute Pytest in CI so defects are caught before merge. (DevOps academic goal; `us13-automated-tests-ci`).

## What Changes

- Deliver the automation/configuration described in `US/us13.md`.
- Document setup in `docs/development_guide.md`.
- Keep academic scope: single demo pipeline/environment.

## Non-goals

- Enterprise multi-stage/multi-region CD, Kubernetes platforms, unrelated app features.

## Capabilities

### New Capabilities

- `automated-testing`: Execute Pytest in CI so defects are caught before merge.

### Modified Capabilities

- (none)

## Impact

- tests/ + CI pytest step; GitHub settings/secrets; no end-user role UI changes.
