# Spec Delta

## Purpose

Allow authenticated TaskFlow DevOps users to end their session so protected resources become inaccessible until they sign in again.

## ADDED Requirements

### Requirement: Logout ends the session

The system SHALL allow an authenticated user to log out, SHALL invalidate the server session, and SHALL clear the session cookie.

#### Scenario: Successful logout
- **WHEN** an authenticated user requests logout
- **THEN** the session is invalidated and subsequent protected calls are unauthorized

#### Scenario: Logout available to all roles
- **WHEN** an Admin, Developer, or Viewer is authenticated
- **THEN** they can log out with the same session-ending behavior

#### Scenario: Unauthenticated logout
- **WHEN** an unauthenticated client calls logout
- **THEN** the system responds with unauthorized status
