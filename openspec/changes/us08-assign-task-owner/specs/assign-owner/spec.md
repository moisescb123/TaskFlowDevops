# Spec Delta

## Purpose

Developer assigns a single registered user as task owner (RN01).

## ADDED Requirements

### Requirement: Single assignee

The system SHALL allow a Developer to set at most one primary assignee referencing a registered user (RN01).

#### Scenario: Assign user
- **WHEN** a Developer sets a valid assignee_id
- **THEN** the task shows that single assignee

#### Scenario: Replace assignee
- **WHEN** a Developer assigns a different user
- **THEN** only the new assignee remains

#### Scenario: Invalid assignee
- **WHEN** assignee_id does not exist
- **THEN** the system returns validation error
