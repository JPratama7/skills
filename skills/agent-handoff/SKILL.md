---
name: agent-handoff
description: Produce a compressed handoff brief for passing work from one agent to another (subagent → parent, parent → subagent, peer, or chained) without losing context. Triggers when an agent finishes a subtask and needs to report back, when delegating work to a subagent, or when writing notes that another agent (or future self) will consume. Use this skill whenever the user asks for an "agent handoff", "handoff brief", "context handoff", "task handoff", "delegation note", "agent briefing", "status report for next agent", "session handoff", or wants to preserve state across agent boundaries. Even if the user doesn't name the concept, use it when an agent has completed work and needs to summarize results in a way another agent can pick up cold.
---

# Agent Handoff

A handoff is the act of compressing everything one agent knows into a brief another agent can consume cold. The challenge: humans read handoffs, but agents need *recoverable* state — task context, decisions made, file state, open questions. A good handoff is dense enough to fit in context but readable enough to skim.

## When to use

Trigger this skill when ANY of these are true:

- An agent finishes work and needs to report results to a calling/parent agent
- A parent agent is delegating a subtask and needs to brief the subagent
- Two peer agents at the same level pass work between each other
- You're writing notes for a future agent or future session that will pick up where you left off
- The user explicitly asks for a "handoff", "brief", "context dump for next agent", "delegation note", or similar

Do NOT use for: user-facing status updates (write prose), commit messages (use git), or final deliverables (the actual artifact, not a handoff).

## The format

Every handoff is **prose summary first, structured tail second**. The prose reads like a sentence a human would write to another human. The tail is a tight reference block an agent (or human) can scan without re-reading the prose.

```
[One-paragraph prose: what was done, what's the current state, what's next]

## State
- Done: <bullet of completed work>
- Pending: <bullet of work not yet done>
- Files: <path> — <one-line purpose>  (only files that matter)
- Decisions: <choice made> — <one-line why>

## Open
- Blocker: <what's stuck and why>
- Question: <what needs an answer before next step>
- Risk: <what could go wrong if next agent proceeds without knowing>

## Context
- Goal: <the actual objective, restated>
- Constraints: <hard limits the next agent must respect>
- Assumptions: <things assumed but not verified>
```

That's the whole format. Use the sections you need; omit empty ones. If the handoff is trivial (one bullet of state, no open questions), skip the headers entirely and just write the prose.

## How to write it well

**Lead with the verdict.** The first sentence of the prose should answer "where are we?" — done, in progress, blocked, or handed off cleanly. If the next agent reads only one sentence, they should know the status.

**State is fact, prose is judgment.** The prose captures *why* and *what it means*; the tail captures *what exists*. Don't repeat yourself across the two — if it's in the tail, the prose just references it.

**Decisions need a "why".** A handoff that says "chose Postgres" is useless; "chose Postgres over SQLite because dataset exceeds 1GB and we need concurrent writes" lets the next agent reverse it correctly if constraints change.

**Files only when they matter.** Don't list every file touched — list files the next agent will need to read, modify, or be aware exist. One-line purpose each. Use absolute paths when the next agent isn't in the same directory.

**Open questions are gold.** A handoff that hides a blocker wastes the next agent's first 5 minutes. Surface anything you couldn't figure out, anything you assumed, and anything that could blow up later.

**Constraints beat goals.** If the next agent only reads one section, it should be constraints. Goals can be inferred; constraints (deadlines, format requirements, things not to touch) cannot.

## Compression rules

The skill is token-aware. Apply these when the handoff would otherwise be long:

- **Drop completed subtasks entirely** if their outcome is in the prose. Don't recap work the next agent can see in git/files.
- **Inline small state** (single file, single decision) into the prose; only break out into bullets when there are 3+ items.
- **Use one-line entries**, never multi-line bullets in the tail. If an entry needs more than one line, it belongs in the prose.
- **Reference, don't quote.** "See `auth.py:42-58` for token refresh logic" beats pasting the code.
- **Omit obvious context.** Don't tell the next agent what `package.json` is.

Target: a typical handoff fits in 200-500 tokens. A complex multi-stage handoff with several open questions can go to ~1000 tokens. If you're past 1500, you're dumping context instead of handing off.

## Anti-patterns

- **The transcript dump.** Pasting your full work history. The next agent doesn't need it.
- **The vague summary.** "Made progress on the feature." Where? What progress? What's left?
- **The decision-less handoff.** "Set up the database." Set up *which* database, with *what* schema, and *why* that one?
- **The buried blocker.** Mentioning a critical issue in bullet 7 of a 10-bullet list. Lead with it in the prose.
- **The everything-matters file list.** 15 files with no priority. The next agent doesn't know where to start.

## Reference files

- `references/handoff-examples.md` — Annotated examples covering the four handoff directions (subagent→parent, parent→subagent, peer, chain) plus the trivial case.

Load it when you want a worked example, or when the handoff is unusually complex and you want to see how the format handles it.