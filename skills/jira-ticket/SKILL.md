---
name: jira-ticket
version: 1.0.0
description: Generate Jira ticket or PR description from compact templates
---

# Jira Ticket & PR Templates

## When to use

Use this skill when asked to:
- Create a Jira ticket (task, bug, or story)
- Generate a PR description
- Draft ticket content from a feature request, bug report, or spec

## How it works

1. Identify the ticket type: **task**, **bug**, or **story**
2. Ask the user for what you need: summary, context, scope, acceptance criteria, and any refs (repo, epic, PRs). You don't need everything upfront — ask for the essentials, fill what you can, and ask for the rest as gaps emerge.
3. Fill the appropriate template below, omitting any section the user didn't provide info for
4. Output the result ready to paste into Jira

For PR descriptions, use the PR template at the bottom.

## Design principles

- **Ticket = what & why** — context, scope, acceptance criteria. Stable, rarely changes.
- **PR = how** — technical implementation lives next to the code, stays accurate.
- **Refs links them** — ticket references PRs, PR references ticket.
- **No duplication** — Jira already tracks assignee, priority, sprint, epic link, labels. Templates don't duplicate those.
- **Summary prefixes** — `[BE]`, `[FE]`, `[INFRA]`, `[BUG]`, `[STORY]` matches team convention.
- **Compact** — every section earns its place. No filler.
- **Omit what you don't know** — if the user didn't provide info for a section (repo, epic, environment, refs), drop that section entirely. Never leave placeholder text like `<TBD>`, `<repo>`, or `<link PRs here>`. A ticket with fewer sections is better than one with visible gaps. When you're interacting with the user, ask for the missing info first — but if you can't ask, just omit.
- **No meta-commentary** — the output is the ticket/PR description and nothing else. Don't append "Assumptions made", "Notes", or similar sections explaining what you omitted or why. Omission speaks for itself; a clean ticket is more useful than one cluttered with self-referential notes about the skill's own rules.
- **Commit to scope** — scope items are definitive commitments, not hedged guesses. Don't write "confirm during discovery" or "TBD" in scope. If something is uncertain, ask the user; if you can't ask, either include it as a committed item or move it to Out of Scope. A ticket reader should know exactly what's being delivered. When the user expresses qualified uncertainty ("might need a backend endpoint"), include it in scope as a conditional item ("Backend streaming endpoint if the dataset exceeds client-side export limits") rather than hedging with "confirm during discovery" — the condition makes it actionable, the hedge makes it noise.

## Summary field

The Summary is the Jira ticket **title** — the one-line headline visible in backlog, boards, search results, and notifications.

Guidelines:
- **Prefix** identifies team/domain: `[BE]`, `[FE]`, `[INFRA]`, `[BUG]`, `[STORY]`
- **Under ~60 chars** — Jira truncates longer titles in board/column views
- **Describe the outcome, not the implementation** — "Add ICD10 search API" not "Modify icd10.go handler"
- **No ticket numbers in summary** — Jira already shows the key next to it

---

## Template: Task

**Summary:** `[BE|FE|INFRA] <short description>`

**Description:**

```
## Context
<1-2 sentences: why this task exists, what it's part of>

## Scope
- <what needs to be done>
- <what needs to be done>

## Refs
*Repo:* <repo name>
*Epic:* <epic key>
*PRs:* <link PRs here as they land>

## Acceptance Criteria
- <criterion>
- <criterion>
```

> Sections like Refs and Environment are optional — include them only when the user provided the info. See "Omit what you don't know" above.

---

## Template: Bug

**Summary:** `[BUG] <short description>`

**Description:**

```
## Reproduction
*Steps:*
# <step 1>
# <step 2>
# <step 3>

*Expected:* <what should happen>
*Actual:* <what happens instead>

## Environment
*Env:* <dev/staging/prod>
*Version:* <build/commit>
*Repo:* <repo>

## Refs
*Epic:* <epic key>
*PRs:* <link PRs here as they land>

## Acceptance Criteria
- <criterion>
- <criterion>
```

> Environment and Refs are optional — include them only when the user provided the info. See "Omit what you don't know" above.

---

## Template: Story

**Summary:** `[STORY] <short description>`

**Description:**

```
## User Story
As a <role>,
I want <capability>,
so that <benefit>.

## Context
<1-2 sentences: business background>

## Scope
- <in-scope item>
- <in-scope item>

## Out of Scope
- <explicitly excluded>

## Refs
*Repo:* <repo>
*Epic:* <epic key>
*PRs:* <link PRs here as they land>

## Acceptance Criteria
- <criterion>
- <criterion>
```

> Refs is optional — include it only when the user provided the info. See "Omit what you don't know" above.

---

## Template: PR Description

Use this when opening a PR. Fills the gap left by removing Technical Details from the ticket.

```
## Ticket
<Jira link>

## What changed
<summary of changes, 2-5 bullets>

## Technical Details
<code paths, design decisions, trade-offs, commands, config changes>

## Test plan
- <how to verify>
- <how to verify>
```

> If the user mentions a repo name, include it in the Ticket line (e.g. `PAY-112 (clinic-api)`) or as a header note. Omit if not provided.

**Substance guidance for PR descriptions:**
- **Technical Details** should include design rationale and trade-offs, not just parameter values. Explain *why* the chosen approach makes sense — what failure mode it prevents, what alternatives were considered, how the pieces interact. A reader should understand the design, not just the config.
- **Test plan** should cover edge cases and error scenarios, not just the happy path. Include verification of failure modes (e.g. "non-retryable errors are not retried", "breaker transitions to half-open after timeout"), not just confirmation that features work.

## Reference files (load on demand)

- User wants to see what a good ticket looks like, or a drafted ticket feels off and needs a concrete contrast → `references/examples.md`
- Acceptance criteria are vague, untestable, or the user is stuck writing them → `references/acceptance-criteria.md`
- Scope contains hedges, TBDs, or fuzzy boundaries that need an explicit out-of-scope list → `references/scope.md`
