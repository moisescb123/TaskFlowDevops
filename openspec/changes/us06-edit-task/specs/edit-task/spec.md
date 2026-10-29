# Spec Delta

## Purpose

Developer updates existing task fields while enforcing RN02.

## ADDED Requirements

### Requirement: Edit task

The system SHALL allow a Developer to update an existing task's title, priority, due date, and assignee subject to validation.

#### Scenario: Successful update
- **WHEN** a Developer saves valid changes
- **THEN** the task is updated and returned

#### Scenario: Invalid update rejected
- **WHEN** required fields are cleared or invalid
- **THEN** the system returns validation error and keeps prior data

#### Scenario: Missing task
- **WHEN** task id does not exist
- **THEN** the system responds not found

#### Scenario: Viewer forbidden
- **WHEN** a Viewer updates a task
- **THEN** the system responds forbidden
