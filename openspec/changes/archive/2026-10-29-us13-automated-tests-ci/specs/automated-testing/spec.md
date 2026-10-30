# Spec Delta

## Purpose

Execute Pytest in CI so defects are caught before merge.

## ADDED Requirements

### Requirement: Pytest in CI

The CI pipeline SHALL execute the project's Pytest suite after dependency install.

#### Scenario: Tests run in CI
- **WHEN** CI runs
- **THEN** Pytest executes and failing tests fail the check

#### Scenario: Local parity
- **WHEN** a Developer runs the same Pytest command locally
- **THEN** results are consistent with CI expectations
