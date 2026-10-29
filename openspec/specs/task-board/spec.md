# task-board Specification

## Purpose

Show an authenticated Kanban-style board of tasks by status, with Viewer unable to mutate data.

## Requirements

### Requirement: Board shows tasks by status

The system SHALL display authenticated users a board with columns To Do, In progress, and Done containing the corresponding tasks.

#### Scenario: Viewer sees columns
- **WHEN** a Viewer opens the board and tasks exist with statuses todo, in_progress, and done
- **THEN** each task appears under the column matching its status, with title, assignee, due date, and priority visible when present
- **AND** automated tests prove status-to-column placement (not only column shell markup or a flat task list)

### Requirement: Viewer cannot mutate

The system SHALL prevent Viewer from create/edit/delete/status-change actions in UI and API.

#### Scenario: Viewer write forbidden
- **WHEN** a Viewer calls a mutating task endpoint
- **THEN** the system responds forbidden

### Requirement: Board requires authentication

The system SHALL deny unauthenticated access to board task listing.

#### Scenario: Anonymous denied
- **WHEN** an unauthenticated client requests board tasks
- **THEN** the system responds unauthorized

### Requirement: Persistence across restart

The system SHALL persist tasks so the board shows the same tasks and statuses after an application restart.

#### Scenario: Data survives restart
- **WHEN** tasks exist and the application restarts
- **THEN** the board shows the same tasks and statuses
