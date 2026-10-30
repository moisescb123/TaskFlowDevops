# Spec Delta

## Purpose

Allow authenticated TaskFlow DevOps users to end their session so protected resources become inaccessible until they sign in again.

## ADDED Requirements

### Requirement: Logout ends the session

The system SHALL allow an authenticated user to log out by clearing the Flask session data and expiring the session cookie on the logout response (`Max-Age=0` / past `Expires`). With client-signed cookie sessions (US01), there is no server-side session store: a previously captured cookie value is not cryptographically revoked. Full token revocation and logout-all-devices are out of scope.

#### Scenario: Successful logout
- **WHEN** an authenticated user requests logout
- **THEN** the response expires the session cookie, the caller's session is cleared, and subsequent protected calls from that client are unauthorized

#### Scenario: Logout available to all roles
- **WHEN** an Admin, Developer, or Viewer is authenticated
- **THEN** they can log out with the same session-ending behavior

#### Scenario: Unauthenticated logout
- **WHEN** an unauthenticated client calls logout
- **THEN** the system responds with unauthorized status
