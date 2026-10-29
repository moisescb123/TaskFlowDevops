# user-auth Specification

## Purpose

Authenticate TaskFlow DevOps users with email and password, establish a role-aware session, and deny unauthenticated access to protected resources.

## Requirements

### Requirement: User login with email and password

The system SHALL allow a registered user to authenticate with email and password and SHALL establish a server-side session that identifies the user and their role (`admin`, `developer`, or `viewer`).

#### Scenario: Successful login returns user and role
- **WHEN** a registered user submits a valid email and password
- **THEN** the system creates a session and returns the user identity including `id`, `email`, `full_name`, and `role` without exposing the password or password hash

#### Scenario: Invalid credentials are rejected
- **WHEN** a user submits an unknown email or an incorrect password
- **THEN** the system does not create a session and returns an authentication failure with a generic message that does not reveal which field failed

#### Scenario: Missing credentials are rejected
- **WHEN** a login request omits email or password, or supplies an invalid email format
- **THEN** the system rejects the request with a validation error that identifies the problem clearly

### Requirement: Session identity introspection

The system SHALL expose the currently authenticated user from the active session.

#### Scenario: Authenticated caller reads current user
- **WHEN** an authenticated client requests the current-user resource
- **THEN** the system returns the same user identity fields as a successful login (`id`, `email`, `full_name`, `role`)

#### Scenario: Unauthenticated caller cannot read current user
- **WHEN** an unauthenticated client requests the current-user resource
- **THEN** the system responds with unauthorized status

### Requirement: Role-aware post-login access context

After successful login, the system SHALL associate the session with exactly one role so that subsequent authorization decisions can distinguish Admin, Developer, and Viewer capabilities. The Admin users page SHALL be restricted to the Admin role.

#### Scenario: Session carries assigned role
- **WHEN** a user with role Admin, Developer, or Viewer logs in successfully
- **THEN** subsequent authorized requests in that session observe the same role that is stored for the user

#### Scenario: Non-admin denied admin users page
- **WHEN** a Developer or Viewer requests the Admin users page
- **THEN** the system denies access (forbidden or redirect away from admin configuration)

### Requirement: Protect authenticated resources

The system SHALL deny unauthenticated access to protected application resources (board and admin entry points and their APIs).

#### Scenario: Unauthenticated request to protected resource
- **WHEN** an unauthenticated client requests a protected resource
- **THEN** the system responds with unauthorized status (API) or redirects to the login experience (UI)

### Requirement: Credential security

The system SHALL store passwords only as irreversible hashes, SHALL NOT return password material in responses, and SHALL NOT log raw passwords. Any login attempt (successful or failed) SHALL leave the client without a prior session unless a new session is established by a successful login in that same attempt.

#### Scenario: Password never returned
- **WHEN** login or current-user succeeds
- **THEN** the response body does not include `password` or `password_hash`

#### Scenario: Failed login does not create a session
- **WHEN** login fails for any reason
- **THEN** no authenticated session is established for that client and any previous session for that client is cleared
