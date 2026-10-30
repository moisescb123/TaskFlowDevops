# Proposal

## Why

Run GitHub Actions CI on push/PR to validate code automatically. (DevOps academic goal; `us12-ci-pipeline`).

## What Changes

- Deliver the automation/configuration described in `US/us12.md`.
- Document setup in `docs/development_guide.md`.
- Keep academic scope: single demo pipeline/environment.

## Non-goals

- Enterprise multi-stage/multi-region CD, Kubernetes platforms, unrelated app features.

## Capabilities

### New Capabilities

- `ci-pipeline`: Run GitHub Actions CI on push/PR to validate code automatically.

### Modified Capabilities

- (none)

## Impact

- .github/workflows/ci.yml; GitHub settings/secrets; no end-user role UI changes.
