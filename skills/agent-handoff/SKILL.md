---
name: agent-handoff
description: Produce a compressed handoff brief for passing work from one agent to another (subagent → parent, parent → subagent, peer, or chained) without losing context. Triggers when an agent finishes a subtask and needs to report back, when delegating work to a subagent, or when writing notes that another agent (or future self) will consume. Use this skill whenever the user asks for an "agent handoff", "handoff brief", "context handoff", "task handoff", "delegation note", "agent briefing", "status report for next agent", "session handoff", or wants to preserve state across agent boundaries. Even if the user doesn't name the concept, use it when an agent has completed work and needs to summarize results in a way another agent can pick up cold.
---

# Agent Handoff

A handoff compresses everything one agent knows into a brief another agent can consume cold. Agents need *recoverable* state — task context, decisions made, file state, open questions — dense enough to fit in context but readable enough to skim.

Use this format whenever work crosses an agent boundary. Do NOT use it for user-facing status updates (write prose), commit messages (use git), or final deliverables (ship the artifact, not a description of it).

## The format

**Prose summary first, structured tail second.** The prose reads like a sentence a human would write to another human; the tail is a scanable reference block. Use the sections you need and omit empty ones. If the handoff is trivial (one bullet of state, no open questions), skip the headers entirely and just write the prose.

```
[One-paragraph prose: what was done, current state, what's next]

## State
- Done: <completed work>
- Pending: <work not yet done>
- Files: <path> — <one-line purpose>  (only files that matter)
- Decisions: <choice made> — <one-line why>

## Open
- Blocker: <what's stuck and why>
- Question: <what needs an answer before next step>
- Risk: <what could go wrong if the next agent proceeds without knowing>

## Context
- Goal: <the actual objective, restated>
- Constraints: <hard limits the next agent must respect>
- Assumptions: <things assumed but not verified>
```

## Lead by direction

The first sentence of the prose is the only thing the reader is guaranteed to see — it must answer "what do I do now?". What that means depends on how much context the reader already has:

- **Subagent → parent (report-back):** lead with the verdict — which option, what shipped, what's blocked. The parent knows the context; they need the outcome and a pointer to evidence. *"Pick: pino. Reasoning in State. Two open questions."*
- **Parent → subagent (delegation):** lead with the start-here signal — the task and the file to open first. The subagent has zero context and must know where to begin in under 20 words. Delegations also get extra rules (below).
- **Peer → peer (chained):** lead with what changed and what didn't. The peer is mid-context but lost the thread — confirm what's stable, then surface the deltas.
- **Session → future session:** lead with status and where to pick up. Future-you is past-you with amnesia — status (done / blocked / in-progress) + the next concrete step.

## Delegation rules

Delegations are the most failure-prone handoff: the subagent has zero context and can't ask clarifying questions until it's minutes deep. On top of the general format:

- **One page max** — ≤400 words / ≤30 lines. Longer means you're dumping context instead of briefing; move detail into linked files the subagent can read on demand.
- **Start-here first** — first sentence names the task and the file/endpoint to open (~15 words).
- **Constraints before Context** — the subagent scans top-to-bottom, so load-bearing rules must precede soft narrative. Order the tail: State → Decisions → Constraints → Open → Context.
- **Prioritize, don't enumerate** — a flat list of MUSTs says none matter most. Split into **Critical** (must not violate, 1-3 max) and **Required** (must do, your choice how).
- **Default on every question** — the point of delegating is that the subagent moves; each Question carries a `Default:` it can act on. A question with no safe default becomes a `Blocker` so it stops instead of guessing.
- **No implementation code** — the brief is *what to build and why*, not *how*. Code blocks get copy-pasted instead of thought through.

```
## Constraints
- Critical:
  - Auth required on every request; reuse `@login_required` from siblings — do NOT write a new decorator
- Required:
  - Stream the response; match existing error shape; tests for auth happy path + 401

## Open
- Question: which fields in the export? Default: profile + orders (see assumption below). Override if a spec exists in /docs.
```

## Writing rules

- **Prose is judgment, State is fact.** The prose carries *why* and *what it means*; the tail lists *what exists*. Don't repeat across the two — if it's in the tail, the prose just references it.
- **Decisions need a why.** "Chose Postgres" is useless; "chose Postgres over SQLite because the dataset exceeds 1GB and we need concurrent writes" lets the next agent reverse it correctly if constraints change.
- **Files only when they matter.** List files the next agent must read, modify, or know exist — one-line purpose each, absolute paths when the reader isn't in the same directory.
- **Surface blockers early.** Hiding a blocker wastes the next agent's first 5 minutes. Anything you couldn't figure out, assumed, or that could blow up later belongs in Open.

## Compression

A typical handoff fits in 200-500 tokens; a complex multi-stage one can go to ~1000 (delegations cap at 400 words). Past 1500 you're dumping context instead of handing off.

- Drop completed subtasks whose outcome is in the prose — don't recap what the reader can see in git/files.
- Inline small state (single file, single decision) into the prose; break out bullets only at 3+ items.
- One-line entries only in the tail — anything needing more than a line belongs in the prose.
- Reference, don't quote: "see `auth.py:42-58` for token refresh" beats pasting the code.
- Omit obvious context — don't explain what `package.json` is.

## Anti-patterns

- **The transcript dump.** Full work history pasted. The next agent doesn't need it.
- **The vague summary.** "Made progress on the feature." Where? What progress? What's left?
- **The decision-less handoff.** "Set up the database." Which one, what schema, why?
- **The buried blocker.** Critical issue in bullet 7 of a 10-bullet list. Lead with it in the prose.
- **The everything-matters file list.** 15 files, no priority — the next agent can't tell where to start.

## Reference files

- `references/handoff-examples.md` — Annotated examples covering the four handoff directions (subagent→parent, parent→subagent, peer, chain) plus the trivial case.

Load it when you want a worked example, or when the handoff is unusually complex and you want to see how the format handles it.
