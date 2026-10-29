---
description: This document contains all development rules and guidelines for TaskFlow DevOps, applicable to all AI agents (Claude, Cursor, Codex, Gemini, etc.).
alwaysApply: true
---

## 1. Core Principles

- **Small tasks, one at a time**: Always work in baby steps, one at a time. Never go forward more than one step.
- **Test-Driven Development**: Start with failing tests for any new functionality (TDD), according to the task details.
- **Type Safety**: Prefer explicit typing (Python type hints; clear JSDoc or typed contracts at API boundaries).
- **Clear Naming**: Use clear, descriptive names for all variables and functions.
- **Incremental Changes**: Prefer incremental, focused changes over large, complex modifications.
- **Question Assumptions**: Always question assumptions and inferences.
- **Pattern Detection**: Detect and highlight repeated code patterns.

## 2. Language Standards

- **English Only**: All technical artifacts must always use English, including:
  - Code (variables, functions, classes, comments, error messages, log messages)
  - Documentation (README, guides, API docs)
  - Tickets and user stories used as implementation input (when creating specs/tasks in English)
  - Data schemas and database names
  - Configuration files and scripts
  - Git commit messages
  - Test names and descriptions

Note: Academic course documents written in Spanish (for example `Avance_Proyecto_Grupo_1_corregido.md` and `US/*.md`) remain source requirements; implementation artifacts derived from them must still be in English.

## 3. Project Context

- **Product**: TaskFlow DevOps — web task board for software project work, used to practice DevOps.
- **Stack**: Python, Flask, SQLite, HTML, CSS, JavaScript, Pytest, GitHub Actions.
- **Roles**: Admin, Developer, Viewer.
- **Canonical user stories**: `US/us01.md` … `US/us15.md`.
- **Requirements reference**: `Avance_Proyecto_Grupo_1_corregido.md` (RF, RNF, RN).

## 4. Specific standards

For detailed standards and guidelines specific to different areas of the project, refer to:

- [Backend Standards](./backend-standards.md) — Flask API, SQLite, Pytest, security
- [Frontend Standards](./frontend-standards.md) — HTML/CSS/JavaScript board UI
- [Documentation Standards](./documentation-standards.md) — technical documentation structure and maintenance
- [Development Guide](./development_guide.md) — setup and local workflow
- [OpenSpec Tasks Mandatory Steps](./openspec-tasks-mandatory-steps.md) — required checklist when creating or updating OpenSpec `tasks.md` files
- [API Spec](./api-spec.yml) — HTTP contracts
- [Data Model](./data-model.md) — domain entities

## 5. Project Skills

- Skills live in `ai-specs/skills` (canonical) and are exposed through `.cursor/skills` and `.claude/skills`.
- When a request matches a skill, load and follow the corresponding `SKILL.md` automatically before continuing.
- Also load any referenced files in the skill folder (for example, `references/*.md`) when the skill requires them.
- OpenSpec workflow skills (`openspec-*`) are installed by the OpenSpec CLI and take precedence for OpenSpec commands.

## 6. Symlink Integrity and Multi-Agent Portability

- **Canonical Source**: Keep reusable Specboot artifacts in `ai-specs` as the canonical source. Agent-specific paths (such as `.claude` and `.cursor`) should reference them through symlinks when possible.
- **Update Safety**: Whenever a file is renamed, moved, or its suffix changes, verify and update all symlinks that target it before considering the change complete.
- **New Artifact Linking**: Whenever creating a new artifact that requires multi-agent exposure (for example new agents or skills in `ai-specs`), create the corresponding symlinks from the expected agent-specific reference paths.
- **Completion Gate**: A change is incomplete if it leaves broken symlinks, stale targets, or duplicated canonical artifacts across agent-specific folders.

## 7. Mandatory OpenSpec Artifact Updates for Post-Apply Changes

When a new fix/change request appears after `opsx:apply` (or `/apply`) and before `opsx:archive` (or `/archive`), agents must treat it as a spec update first, not as an informal "fix this quickly". Documentation is the source of truth.

Required order:

1. Update the current OpenSpec change artifacts that are affected (for example: scenarios, requirements/specs, and `tasks.md`).
2. If artifact regeneration is needed, run the corresponding OpenSpec step (`opsx:continue`, `opsx:ff`, or equivalent) before coding.
3. Implement code only after artifacts reflect the new request.
4. Re-run verification against the updated artifacts before archiving.

Do not apply direct code-only fixes in this window without updating OpenSpec artifacts.
