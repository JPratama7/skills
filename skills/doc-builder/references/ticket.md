# Ticket

Work item for a tracker — Jira task/bug/story, GitHub issue. Readers are
engineers picking up work and PMs tracking scope. The ticket carries the
**what & why**; the **how** lives in the PR description next to the code.
Refs link them: ticket references PRs, PR references ticket.

## Interview questions

Ask all that are not already answered by context. You don't need everything
upfront — ask for the essentials, fill what you can, ask for the rest as
gaps emerge:

1. Type — task, bug, or story?
2. Summary — one-line outcome headline (see Summary rules)?
3. Context — why does this exist, what epic/effort is it part of?
4. Scope — what gets delivered? Anything explicitly out of scope?
5. Refs — repo, epic, related PRs?
6. Acceptance criteria — how will we verify it's done?
7. Bug only — reproduction steps, expected vs actual, environment/version?

## Summary rules

- **Prefix** identifies team/domain when the team uses them: `[BE]`, `[FE]`,
  `[INFRA]`, `[BUG]`, `[STORY]`
- **Under ~60 chars** — Jira truncates longer titles in board/column views
- **Outcome, not implementation** — "Add ICD10 search API" not "Modify
  icd10.go handler"
- **No ticket numbers in the summary** — the tracker already shows the key

## Template: Task

**Summary:** `[BE|FE|INFRA] <short description>`

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

## Template: Bug

**Summary:** `[BUG] <short description>`

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

## Template: Story

**Summary:** `[STORY] <short description>`

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

## Quality bar

- **No duplication** — the tracker already records assignee, priority,
  sprint, epic link, labels. Templates don't restate them.
- **Omit what you don't know** — if the user didn't provide info for a
  section (repo, epic, environment, refs), drop that section entirely. Never
  leave placeholder text like `<TBD>` or `<repo>`. Fewer sections beat
  visible gaps. Ask for missing info first; omit if you can't ask.
- **No meta-commentary** — the output is the ticket and nothing else. No
  "Assumptions made" or "Notes" sections explaining what was omitted.
  Omission speaks for itself.
- **Commit to scope** — scope items are definitive commitments, not hedged
  guesses. No "TBD", no "confirm during discovery". Qualified uncertainty
  becomes a committed conditional ("Backend streaming endpoint if the
  dataset exceeds client-side export limits").
- **Acceptance criteria are checkable** by a person who didn't write the
  ticket, using only the ticket and the running system.

## Reference files (load on demand)

- Acceptance criteria vague, untestable, or user stuck writing them →
  `references/acceptance-criteria.md`
- Scope contains hedges, TBDs, or fuzzy boundaries → `references/scope.md`
- Drafted ticket feels off, needs a concrete strong/weak contrast →
  `references/examples.md`
