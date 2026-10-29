# Spec Delta

## Purpose

Developer deletes tasks after confirmation so obsolete work is removed.

## ADDED Requirements

### Requirement: Delete task

The system SHALL allow a Developer to delete a task; deleted tasks SHALL NOT reappear after restart.

#### Scenario: Successful delete
- **WHEN** a Developer deletes an existing task
- **THEN** the system removes it and subsequent lists omit it

#### Scenario: Missing task
- **WHEN** task id does not exist
- **THEN** the system responds not found

#### Scenario: Viewer forbidden
- **WHEN** a Viewer deletes a task
- **THEN** the system responds forbidden
