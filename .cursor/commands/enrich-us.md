---
name: "/enrich-us"
id: "enrich-us"
category: "Workflow"
description: "Enrich a user story and always overwrite the target US/usXX.md file"
---

Enrich a vague user story or idea into an implementation-ready ticket for TaskFlow DevOps, then **always overwrite** the target story file.

**Input**: The argument after `/enrich-us` can be:
- a local story path or id (`US/us05.md`, `us05`, `US-05`)
- pasted story/ticket text (also name the target `US/usXX.md`)
- a Jira key (only if Jira MCP is configured; also name the target file)
- a short idea to refine (also name the target file)

If no input is provided, ask the user which story to enrich (for example, pick from `US/us01.md` … `US/us15.md`).

**Steps**

1. Load and follow the project skill at `.cursor/skills/enrich-us/SKILL.md` (canonical source: `ai-specs/skills/enrich-us/SKILL.md`).
2. Resolve the input and **target path**:
   - If it matches `US/usXX.md` or `usXX` / `US-XX`, read that file. Target = `US/usXX.md`.
   - If it looks like a Jira key and Jira MCP is available, fetch the ticket and require a `US/usXX.md` target.
   - Otherwise treat the argument/message as the story text and require a `US/usXX.md` target.
3. Use project technical context from `docs/base-standards.md`, `docs/api-spec.yml`, `docs/data-model.md`, `docs/backend-standards.md`, and `docs/frontend-standards.md` when adding technical detail.
4. Produce markdown with exactly these sections:
   - `## Original`
   - `## Enhanced`
5. The Enhanced section must be implementation-ready: behavior, acceptance criteria, fields/validations, endpoints, files/modules, definition of done, NFRs, and role impact (Admin / Developer / Viewer) when relevant.
6. **Always overwrite the target `US/usXX.md` file** with the full `## Original` + `## Enhanced` markdown. Replace the entire file. Do not ask for confirmation. Do not only print the result in chat.
7. Confirm in one short sentence which file was overwritten.
8. Do **not** create an OpenSpec change in this command. The user can then run `/opsx-propose` or `/opsx-ff` if they want planning artifacts.

**Notes**

- Overwrite is mandatory for every successful `/enrich-us` run with a known target file.
- If the file was already enriched, use the existing `## Original` section as the source story when present.
- Keep enhanced technical content in English; Spanish original story text may remain under `## Original`.
- Do not require Jira when a local `US/` file or pasted text is available.
