# Spec Delta

## Purpose

Developer creates tasks in To Do with required title, priority, due date (RN02).

## ADDED Requirements

### Requirement: Create task

The system SHALL allow a Developer to create a task with required title, priority, and due date, defaulting status to `todo`. Create is Developer-only: Admin and Viewer SHALL receive forbidden on create. The create UI SHALL ignore duplicate in-flight submits so one user action creates at most one task.

#### Scenario: Successful create
- **WHEN** a Developer submits valid task data
- **THEN** the task is stored as To Do and returned

#### Scenario: RN02 validation
- **WHEN** title, priority, or due date is missing/invalid
- **THEN** the system returns validation error and creates nothing

#### Scenario: Viewer forbidden
- **WHEN** a Viewer creates a task
- **THEN** the system responds forbidden

#### Scenario: Admin forbidden
- **WHEN** an Admin creates a task
- **THEN** the system responds forbidden

#### Scenario: Duplicate submit ignored
- **WHEN** a Developer triggers create again while a create request is in flight
- **THEN** the client does not send a second create until the first request finishes
