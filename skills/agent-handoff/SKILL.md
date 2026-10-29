---
name: agent-handoff
description: Produce a compressed handoff brief for passing work from one agent to another (subagent → parent, parent → subagent, peer, or chained) without losing context. Triggers when an agent finishes a subtask and needs to report back, when delegating work to a subagent, or when writing notes that another agent (or future self) will consume. Use this skill whenever the user asks for an "agent handoff", "handoff brief", "context handoff", "task handoff", "delegation note", "agent briefing", "status report for next agent", "session handoff", or wants to preserve state across agent boundaries. Even if the user doesn't name the concept, use it when an agent has completed work and needs to summarize results in a way another agent can pick up cold.
---

# Agent Handoff

A handoff compresses what one agent knows into a brief another can consume cold — task context, decisions, file state, open questions — dense enough for context, readable enough to skim.

Use this format whenever work crosses an agent boundary. Not for user-facing status updates (write prose), commit messages (use git), or deliverables (ship the artifact).

## The format

**Prose summary first, structured tail second.** Use only the sections that carry information; omit empty ones. A trivial handoff (one bullet of state, no open questions) skips the headers entirely.

```
[One-paragraph prose: what was done, current state, what's next]

## State
- Done: <completed work>
- Pending: <work not yet done>
- Files: <path> — <one-line purpose>  (only files the reader must touch)
- Decisions: <choice made> — <one-line why>

## Open
- Blocker: <what's stuck and why>
- Question: <what needs an answer>  Default: <fallback action>
- Risk: <what could go wrong if the reader proceeds unaware>
- Missing: <expected file/info that turned out not to exist>

## Context
- Goal: <the actual objective>
- Constraints: <hard limits the reader must respect>
- Assumptions: <believed but NOT verified>
```

## Lead by direction

The first sentence is the only line guaranteed to be read — it answers "what do I do now?". What that means depends on the reader's context:

- **Subagent → parent (report-back):** lead with the verdict + a pointer to evidence. The parent has context; give the outcome. *"Pick: pino. Bench data in `perf/results.json`. One open question."*
- **Parent → subagent (delegation):** lead with the task + the file to open first (~15 words). Zero-context reader must know where to begin. Extra rules below.
- **Peer → peer (chained):** lead with what changed and what didn't — confirm what's stable, then the deltas.
- **Session → future:** lead with status (done / blocked / in-progress) + the next concrete step. Future-you is past-you with amnesia.

## Ground it — verify, don't recall

The reader can't tell your certainties from your guesses and will act on both. A wrong path or invented number costs more than a marked unknown — so check before stating, and mark what you couldn't check.

- **Re-check every path at write time.** Each file under `Files:` must exist *now* — `ls` it, don't transcribe from memory. References inside your inputs ("see docs/rollout.md") are claims, not facts: if the file isn't there, it goes in Open as `Missing:`, never in Files.
- **Cite only identifiers you've seen** — commit hashes, error strings, ticket IDs, env names. Can't confirm one? Mark it `Unverified:` or cut it.
- **Numbers need a source** in this session's artifacts — a file, command output, or log you can point at. Otherwise prefix `~`, tag unverified, or drop the figure.
- **Done means confirmed.** "Should be done" goes under Assumptions, not Done. Done items carry evidence the reader can check (a file, a test run, a commit). Don't report the plan as the outcome.

## Delegation rules

Delegations are the most failure-prone handoff — zero context, no clarifying questions until it's minutes deep. On top of the general format:

- **One page max** — ≤400 words / ≤30 lines; longer means you're dumping context. Move detail into linked files.
- **Start-here first** — first sentence names the task and the file/endpoint to open.
- **Constraints before Context** — load-bearing rules precede soft narrative. Order the tail: State → Decisions → Constraints → Open → Context.
- **Prioritize, don't enumerate** — split **Critical** (must not violate, 1-3 max) from **Required** (must do, your choice how).
- **Default on every Question** — a question with no safe default becomes a Blocker so it stops instead of guessing.
- **No implementation code** — the brief is *what to build and why*, not *how*. Pasted code gets copy-pasted instead of thought through.

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

- **Prose is judgment, tail is fact** — don't repeat across them; if it's in the tail, the prose references it.
- **Decisions need a why** — "chose Postgres" is useless; the reason lets the reader reverse it correctly if constraints change.
- **Files only when they matter** — what the reader must read, modify, or know exists; one-line purpose each; absolute paths when the reader isn't in the same directory.
- **Blockers early** — anything you couldn't solve, assumed, or that could blow up goes in Open and surfaces in the prose.

## Budgets

| Direction | Cap | Skip by default |
|---|---|---|
| Report-back | ~150 words | Context — the parent has it |
| Delegation | 400 words / 30 lines | — |
| Peer | ~250 words | Context — give deltas only |
| Session | ~300 words | — |

Over cap means you're dumping, not briefing — push detail into files and point at them.

- Drop completed subtasks visible in git or files.
- Inline single-item state into the prose; bullets start at 3 items.
- One line per tail entry — anything longer belongs in the prose.
- Reference, don't quote: "see `auth.py:42-58`" beats pasting code.

## Where handoffs live

Inline when the receiver is a spawn away. Write a file when it must outlive the session — default `.agent-handoff/<topic>.md` at the project root. Never `/tmp/` — handoffs exist to survive restarts.

## Anti-patterns

- **Transcript dump** — full work history pasted; the reader doesn't need it.
- **Vague summary** — "made progress on the feature." Where? What's left?
- **Decision-less** — "set up the database." Which one, what schema, why?
- **Buried blocker** — critical issue in bullet 7. Lead with it.
- **Everything-matters file list** — 15 files, no priority; the reader can't tell where to start.
- **Invented detail** — a path, hash, or number you didn't verify. Mark `Missing:` / `Unverified:` or cut it.

## Memory

`.memory/memory.json` → `agent-handoff`: optional `handoff_dir` override
(default `.agent-handoff/`). Handoff files themselves stay in that dir — the
store holds config, not handoffs.

## Reference files (load on demand)

- Worked examples or unusually complex handoffs → `references/handoff-examples.md` (all four directions + the trivial case).
