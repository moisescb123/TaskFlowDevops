# user-management Specification

## Purpose

Enable Admins to register TaskFlow DevOps users and assign roles that drive authorization.

## Requirements

### Requirement: Admin creates users with roles

The system SHALL allow an Admin to create a user with email, password, full name, and role (`admin`, `developer`, or `viewer`), storing only a password hash.

#### Scenario: Successful create
- **WHEN** an Admin submits valid user data
- **THEN** the user is persisted and returned without password material

#### Scenario: Duplicate email rejected
- **WHEN** an Admin submits an existing email
- **THEN** the request is rejected and no user is created

#### Scenario: Validation errors
- **WHEN** required fields are missing or role is invalid
- **THEN** the system returns a clear validation error

### Requirement: Only Admin manages users

The system SHALL deny user creation to Developer, Viewer, and unauthenticated callers.

#### Scenario: Non-admin forbidden
- **WHEN** a Developer or Viewer calls create-user
- **THEN** the system responds forbidden

#### Scenario: Anonymous unauthorized
- **WHEN** an unauthenticated client calls create-user
- **THEN** the system responds unauthorized

### Requirement: Admin can list users

The system SHALL allow Admin to list users without password hashes.

#### Scenario: List users
- **WHEN** an Admin requests the user list
- **THEN** responses include id, email, full_name, and role only
