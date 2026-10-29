---
name: enrich-us
description: Analyze and enhance user stories into implementation-ready detail with acceptance criteria and technical notes. Use when the user runs /enrich-us, asks to enrich a user story, refine US/usXX.md, or improve a vague ticket/idea before OpenSpec planning. Always overwrites the target US file.
author: LIDR.co
version: 1.2.0
---
# enrich-us Skill

Refine a vague user story or idea into an implementation-ready ticket for TaskFlow DevOps.

## Instructions

Analyze and enrich the ticket or story provided in the user message (arguments after `/enrich-us`, a path like `US/us05.md`, pasted text, or a Jira key).

Follow these steps:

1. Determine the ticket input source and **target file**:
   - **Local US file:** If the user passes `US/usXX.md` or a story id like `us05` / `US-05`, read that file. Target path = `US/usXX.md`.
   - **Direct input mode:** Use the ticket/story content shared in the prompt/chat. Ask which `US/usXX.md` to write unless the user already named one.
   - **Jira mode (optional):** If the user provides a Jira id/key, or asks to use Jira, use Jira MCP when available to fetch the ticket details. Ask which `US/usXX.md` to write unless already specified.
2. Act as a product expert with technical knowledge of this project.
3. Understand the problem described in the ticket.
4. Load project context from `docs/base-standards.md`, `docs/api-spec.yml`, `docs/data-model.md`, and related standards when enriching technical detail.
5. Decide whether the User Story is completely detailed for autonomous implementation. Validate that it includes:
   - Full functionality description (who / what / why, plus behavior)
   - Acceptance criteria (Given / When / Then when useful)
   - Fields and validations
   - Required endpoints (aligned with `docs/api-spec.yml` when applicable)
   - Files/modules to touch according to architecture
   - Definition of done (implementation, tests, docs)
   - Non-functional requirements (security, usability, persistence, CI implications)
   - Role impact (Admin / Developer / Viewer) when relevant
6. Build the enriched markdown with exactly these sections:
   - `## Original`
   - `## Enhanced`
7. **Always overwrite the target file** with that full markdown (replace the entire file contents). Do not ask for confirmation. Do not append; replace.
8. After writing, briefly confirm the path that was overwritten. Do not create an OpenSpec change.
9. Jira write-back remains optional and only applies in Jira mode (in addition to the local file overwrite when a `US/` target was set):
   - Update the Jira ticket by appending the enhanced content after the original content, with clear `h2` sections `[original]` and `[enhanced]` when the user wants Jira updated.
   - If ticket status is `To refine`, move it to `Pending refinement validation`.

## Notes

- **Overwrite is mandatory** whenever a target `US/usXX.md` is known.
- Do not require Jira when the user already provided full ticket content or a local `US/` file.
- If input is ambiguous (no story content and no path), ask for a `US/usXX.md` path or the story text.
- Keep enhanced technical artifacts in English; the original Spanish story text may be preserved under `## Original`.
- If the file was already enriched, re-enrich from the current `## Original` section when present; otherwise treat the whole file as the original story.
