---
description: Frontend development standards for TaskFlow DevOps (HTML, CSS, JavaScript task board UI).
globs: ["**/*.{html,css,js}", "**/static/**/*", "**/templates/**/*"]
alwaysApply: true
---

# Frontend Standards — TaskFlow DevOps

## Technology Stack

| Area | Choice |
|------|--------|
| Markup | HTML |
| Styles | CSS |
| Behavior | JavaScript (vanilla; no mandatory SPA framework) |
| Delivery | Flask templates and/or static assets served by Flask |

## Goals

- Provide a clear Kanban-style board with columns **To Do**, **In progress**, and **Done** (RF08 / US04).
- Support Developer CRUD flows for tasks without full page reload when practical (create/edit/delete/move).
- Enforce Viewer read-only experience in the UI (hide or disable mutating controls).
- Show clear validation errors for invalid or incomplete input (RNF03).

## UI Conventions

- Task cards show assignee, due date, and priority with clear visual labels or colors.
- Priority values: High, Medium, Low.
- Confirm before deleting a task.
- Reject UI attempts to skip `To Do` → `Done` and show an explanatory message (RN04); still rely on backend enforcement.
- Forms for create/edit collect: title, assignee (registered user), due date, priority.
- Login and logout entry points for authenticated sessions (US01, US02).
- Admin screens for user registration and role assignment (US03) must be Admin-only.

## Coding Standards

- Keep JavaScript modules small and focused (board rendering, form handling, API client).
- Prefer progressive enhancement: core flows work with standard forms; enhance with fetch/XHR when useful.
- Avoid inline script sprawl in templates; prefer static JS files.
- Accessible labels on form fields; sufficient color contrast for priority and status cues.
- Do not store secrets in frontend code.

## Compatibility (RNF04)

- Support the two latest stable versions of Chrome, Firefox, and Edge without requiring extra plugins.

## Testing

- Prefer backend Pytest for business rules.
- Add lightweight frontend checks when practical (for example, critical DOM selectors or smoke checks in CI if tooling is introduced later).
- Manual sprint review against acceptance criteria remains part of validation.
