# task-priority Specification

## Purpose

Developer sets priority High/Medium/Low with visible card indicator.

## Requirements

### Requirement: Task priority

The system SHALL require priority on create as one of `high`, `medium`, `low` and SHALL expose it on the board.

#### Scenario: Set priority
- **WHEN** a Developer sets a valid priority
- **THEN** it is stored and shown on the card

#### Scenario: Invalid priority
- **WHEN** priority is missing on create or not in the enum
- **THEN** the system returns validation error
