# Spec Delta

## Purpose

Developer moves tasks across statuses with RN04 (no To Do → Done skip).

## ADDED Requirements

### Requirement: Status transitions with RN04

The system SHALL allow Developer status changes along allowed paths and SHALL reject direct `todo` → `done`.

#### Scenario: To Do to In progress
- **WHEN** a Developer moves a todo task to in_progress
- **THEN** the status updates successfully

#### Scenario: In progress to Done
- **WHEN** a Developer moves an in_progress task to done
- **THEN** the status updates successfully

#### Scenario: Illegal skip rejected
- **WHEN** a Developer moves todo directly to done
- **THEN** the system rejects the change and status is unchanged

#### Scenario: Viewer forbidden
- **WHEN** a Viewer changes status
- **THEN** the system responds forbidden
