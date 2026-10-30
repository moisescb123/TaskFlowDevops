# Proposal

## Why

Protect main so merges/deploys require passing automated tests (RN03). (DevOps academic goal; `us14-main-branch-protection`).

## What Changes

- Deliver the automation/configuration described in `US/us14.md`.
- Document setup in `docs/development_guide.md`.
- Keep academic scope: single demo pipeline/environment.

## Non-goals

- Enterprise multi-stage/multi-region CD, Kubernetes platforms, unrelated app features.

## Capabilities

### New Capabilities

- `branch-protection`: Protect main so merges/deploys require passing automated tests (RN03).

### Modified Capabilities

- (none)

## Impact

- GitHub branch protection / rulesets; GitHub settings/secrets; no end-user role UI changes.
