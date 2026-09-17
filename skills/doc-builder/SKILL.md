---
name: doc-builder
version: 1.0.0
description: Create structured documents — root cause analyses, reports, and
  requirements docs — by interviewing the user and filling proven templates.
  Use whenever the user asks to write, draft, or create an RCA, incident
  review, postmortem, status/project report, requirements doc, PRD, or spec —
  even if they only say "write a doc" or "document this". Never let the user
  start from a blank page.
---

# doc-builder

Produce a complete, well-structured document without making the user invent
the structure. Each supported doc type ships a template plus the questions
needed to fill it.

## Workflow

1. **Identify the doc type** — match the request to a supported type below.
   If the user names the type explicitly, trust it. If ambiguous ("write a
   doc about X"), ask one clarifying question, offering the closest match.
2. **Load the reference file** for that type — it contains the interview
   questions, the template, and the quality bar.
3. **Interview the user** — ask the reference's question set, batched into
   one turn. Skip questions the conversation or codebase already answers;
   state what you inferred instead of re-asking. Unanswered questions become
   `TODO:` markers in the draft, never silently invented content.
4. **Fill the template** — every section gets real content or an explicit
   `TODO:` with what is missing. No placeholder lorem ipsum, no invented
   metrics, dates, or names.
5. **Save the doc** — markdown file, named after the doc (e.g.
   `rca-payment-outage-2026-09.md`, `requirements-search-v2.md`). Ask where
   to save if the repo has no obvious docs location.

## Doc types

| Type | Use when | Reference |
|------|----------|-----------|
| Root cause analysis | Incident, outage, bug postmortem, "why did X happen" | `references/root-cause-analysis.md` |
| Report | Status update, progress summary, investigation findings, periodic review | `references/report.md` |
| Requirements | New feature/system spec, PRD, "what should we build" | `references/requirements.md` |

## Rules

- Interview before drafting. A template filled with guesses is worse than a
  short list of questions — wrong facts in an RCA or requirements doc get
  treated as truth later.
- One interview round, not a drip-feed. Batch all questions so the user can
  answer in a single reply.
- Keep the template's section order — downstream readers (reviewers,
  auditors, stakeholders) rely on it.
- Match formality to the type: RCA is factual and blameless, report is
  scannable, requirements are testable statements.
- If the user's request spans types ("RCA plus a report for leadership"),
  produce both docs rather than merging them — the audiences differ.
- Diagrams are Mermaid — fenced ` ```mermaid ` blocks, never ASCII art.
  ASCII breaks in renderers and drifts from the text it describes. Each
  reference names the diagram its doc type requires.

## Reference files (load on demand)

- Incident, outage, bug postmortem, "why did X happen" → `references/root-cause-analysis.md`
- Status update, progress summary, investigation findings → `references/report.md`
- Feature/system spec, PRD, "what should we build" → `references/requirements.md`
