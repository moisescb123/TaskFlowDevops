# Spec Delta

## Purpose

Developer sets a required due date for planning deadlines.

## ADDED Requirements

### Requirement: Task due date

The system SHALL require a valid due date on create and SHALL display it on the board.

#### Scenario: Set due date
- **WHEN** a Developer provides a valid due date
- **THEN** it is stored and shown on the card

#### Scenario: Invalid due date
- **WHEN** due date is missing on create or malformed
- **THEN** the system returns a clear validation error
