---
name: enrich-us
description: Enrich a user story and always overwrite the target US/usXX.md file
---

Enrich a vague user story or idea into an implementation-ready ticket for TaskFlow DevOps, then **always overwrite** the target file.

**Input**: The argument after `/enrich-us` can be a local story (`US/us05.md` / `us05`), pasted text, a short idea, or a Jira key if Jira MCP is configured. If missing, ask which story to enrich from `US/`.

**Steps**

1. Load and follow `.claude/skills/enrich-us/SKILL.md` (canonical: `ai-specs/skills/enrich-us/SKILL.md`).
2. Resolve input (local US file, Jira, or pasted text) and the target `US/usXX.md`.
3. Use `docs/` technical context when enriching.
4. Build markdown with `## Original` and `## Enhanced` only.
5. **Always overwrite** the target `US/usXX.md` with that full markdown (replace entire file; no confirmation).
6. Confirm the overwritten path in one short sentence.
7. Do not create an OpenSpec change here.
