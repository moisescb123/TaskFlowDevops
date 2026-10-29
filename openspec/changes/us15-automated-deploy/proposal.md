# Proposal

## Why

Deploy automatically after green verification to a Flask-compatible host. (DevOps academic goal; `us15-automated-deploy`).

## What Changes

- Deliver the automation/configuration described in `US/us15.md`.
- Document setup in `docs/development_guide.md`.
- Keep academic scope: single demo pipeline/environment.

## Non-goals

- Enterprise multi-stage/multi-region CD, Kubernetes platforms, unrelated app features.

## Capabilities

### New Capabilities

- `continuous-delivery`: Deploy automatically after green verification to a Flask-compatible host.

### Modified Capabilities

- (none)

## Impact

- .github/workflows/cd.yml + host config; GitHub settings/secrets; no end-user role UI changes.
