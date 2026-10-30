# branch-protection Specification

## Purpose

Protect main so merges/deploys require passing automated tests (RN03).

## Requirements

### Requirement: Main branch protected by CI

The repository SHALL protect `main` so changes cannot merge when required CI checks fail (RN03).

#### Scenario: Failing CI blocks merge
- **WHEN** a PR to main has failing required checks
- **THEN** merge is blocked

#### Scenario: Passing CI allows merge path
- **WHEN** required checks pass and protection rules are satisfied
- **THEN** merge is allowed
