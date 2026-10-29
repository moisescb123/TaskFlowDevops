# Spec Delta

## Purpose

Deploy automatically after green verification to a Flask-compatible host.

## ADDED Requirements

### Requirement: Deploy after green checks

The system SHALL support automated deployment after successful CI on the release branch, and SHALL NOT deploy from a failing verification run (RN03).

#### Scenario: Green main deploys
- **WHEN** CI succeeds on main
- **THEN** CD deploys the app to the configured environment

#### Scenario: Red CI does not deploy
- **WHEN** CI fails
- **THEN** that run does not deploy

#### Scenario: Secrets not in source
- **WHEN** deployment credentials are configured
- **THEN** they are stored outside the git tree (Actions secrets / host env)
