---
name: crewmates
description: Run your crewmates — a standing crew of persistent named
  agents with recursive leads for sub-teams. Roster persisted in memory,
  shared board, per-member inboxes, temp one-shots for leaf work. Use
  whenever delegating to subagents, spawning or coordinating parallel
  agents, or when agents keep losing context between prompts and
  re-briefing the same context wastes tokens. For fixed one-shot DAG
  plans, use graph-decompose.
---

# Crew

You are a lead. A crew is a tree of named agents: you dispatch to your
teammates, and any teammate with its own teammates is a lead running this
same SOP one level down. Members persist across prompts, so context
accumulates in the agent and in shared files instead of being re-briefed
every spawn.

## State layout

```
.memory/memory.json → "crewmates" namespace (cross-skill-memory protocol):
  roster    — the member tree: {name, role, spawn, teammates: [...]}
  defaults  — {model, max_parallel, depth_cap: 3, fanout_cap: 5}
  status    — last known state per member: running | done | failed

.crew/ → bulky state in the project root:
  board.md         — shared knowledge; the memory that kills re-briefing
  inbox/<name>.md  — mail addressed to that member
```

Gitignore `.crew/inbox/` — it is runtime chatter. `board.md` may be
committed if the project wants the knowledge.

## 1. Entry: revive the crew

On every skill entry, read `memory.json` → `crewmates` and `shared.lessons`.

- Roster exists → bring standing members up (§6). Each member reads
  `.crew/board.md` and its own inbox first. That file read IS the
  catch-up — never paste context the board already holds into a prompt.
- Status shows `running` from a dead session → verify and integrate what
  finished, respawn what didn't, before new work.
- No roster → you are a crew of one. Delegate per §3 and add a seat when a
  role repeats.

## 2. Interview the setup — before the first dispatch

A crew outlives the task that created it, so its shape is the user's
call, not yours. When a job needs a roster (§3 says so), ask one batch
of questions before spawning:

- **The work** — what repeats? Recurring areas earn standing seats;
  one-offs stay temps.
- **The shape** — roles and names they want, or your proposed tree for
  approval.
- **The boundaries** — what stays with you (judgment, user contact),
  what write scopes are off-limits.
- **The defaults** — model, parallelism, how much verification they
  want.

Then propose the roster tree and get approval before spawning standing
members. Coverage check before proposing: walk the scope and map every
piece to a seat or to yourself — a gap in the tree is a gap in the
product. Skip the interview when the task is obviously a temp one-shot
— asking about a crew for a grep is worse than guessing.

## 3. Decide: member, temp, or inline

- **Crew member** — work that repeats, accumulates context (a codebase
  area, a research thread), or carries teammates. Standing seat in the
  roster.
- **Temp one-shot** — a self-contained leaf task you can verify without
  re-doing it. Spawn, contract, done. Never enters the roster.
- **Inline** — dependent steps, small edits where you hold the context,
  judgment calls, anything needing the user mid-task. Work that IS
  communication never delegates.

A seat is earned by a second task: if you would brief the same role twice,
make it a member. One task stays a temp.

## 4. The lead SOP — every dispatch, every level

**Brief.** Order matters; the member sees only this text plus what you
point it at:

```
Task: <one imperative sentence>
Start here: <file/path/endpoint to open first>

Context: <the goal, decisions already made with their why>

Constraints:
- Critical: <rules that must not be violated>
- Required: <must happen; method up to the member>

Scope: <investigate-only vs. make-changes; files/dirs it owns>

Skills: <skills to load first, by name or path — skills don't propagate>

Output contract: <exact return shape, evidence expected, failure report>

Defaults: <every open question gets "Default: X">
```

- Cap ~400 words. Point at files; don't paste them.
- Every open question gets a default. A question with no safe default is a
  blocker you resolve before dispatching.
- The output contract is not optional — specify the shape (verdict +
  evidence, file list, pass/fail per item) and ask for a telegraphic
  report: findings only, no preamble.
- "Read `.crew/board.md` first" replaces context the board already holds.
- Worked examples: `references/delegation-prompts.md`.

**Dispatch.** Independent members go in the same turn. Write scopes stay
disjoint — two members editing one file collide; merge or sequence them.
Log every spawn in roster `status`. Don't poll: work your own tasks while
members run; check only when one seems stuck.

**Verify.** Member output is a claim, not a fact. Check it against the
output contract first — a great answer to the wrong question is a failed
run. Spot-check load-bearing claims: rerun its test, read its diff, open
the file:line it cites.

**Integrate & distill.** What you report upward is a distillation, never a
relay — your lead gets verdict + evidence, not raw worker output. On
failure, fix the brief, not the work: resume with the missing context or
respawn corrected. Post reusable findings to the board; append a lesson
to `shared.lessons` after a failure or a win worth keeping.

## 5. Board and mail

**Board** — `.crew/board.md`, one line per fact under stable sections
(`## Conventions`, `## APIs`, `## Decisions`, `## Open questions`).

- Members post distilled facts, never transcripts. A board dump is a
  re-briefing with extra steps.
- Root lead prunes at session start: cut stale entries, merge dupes. A
  rotting board misleads worse than no board.

**Mail** — `.crew/inbox/<name>.md`.

- Append `- from <sender>: <message>`. Reader clears the file after
  consuming.
- Members write to each other's inboxes directly — cross-member
  coordination does not route through the lead.

**Dispatch-request** — portable recursion (§6): a member that cannot spawn
asks its lead's inbox:

```
- DISPATCH <role>: <task> → report to inbox <requester>
```

## 6. Spawning and portability

Standing members must work where panes exist and where they don't.

- **Herdr** (`HERDR_ENV=1`): members are panes — `herdr agent start
  <name> --kind devin --pane <pane_id>`, re-prompt with `herdr agent
  prompt <name> --wait`. A pane agent can run `herdr agent start` itself,
  so sub-leads spawn their own teammates directly.
- **Plain** (`run_subagent` or equivalent): the spawn returns an agent id
  — record it in roster `status` and `resume`/re-prompt it for follow-ups.
  If a member's harness cannot spawn, it drops a DISPATCH line in your
  inbox; you spawn the worker, which reports to the requester's inbox.
- **Across sessions**: if pane/agent ids don't survive, respawn the
  member — it reads board + inbox and is caught up. The board is the real
  persistence; a live agent is a fast path.

## 7. Roster shape

Free-form tree in `memory.json` → `crewmates.roster`. Node shape:

```json
{"name": "backend-lead", "role": "owns src/api/", "spawn": "standing",
 "teammates": [ {"name": "api-scout", "role": "read-only trace", "spawn": "standing"} ]}
```

Caps: depth ≤ 3, teammates ≤ 5 per lead — past that, coordination costs
more than the parallelism saves. A lead needs ≥ 2 teammates; otherwise
collapse it into one member.

Default leaf template — edit freely: `scout` (read-only explore),
`builder` (writes), `reviewer` (verifies diffs). Example trees for common
project shapes: `references/roster-examples.md`.

## Anti-patterns

- **Theater tree** — depth for its own sake. A two-task job needs one
  member, not a lead with two workers.
- **Wall-of-text relay** — raw worker output passed to the lead. The
  contract said distill.
- **Board hoarding** — transcripts, guesses, stale facts on the board.
  One line, sourced, or cut.
- **Re-briefing the board** — pasting into a brief what the member reads
  for itself.
- **Orphan spawn** — a spawn with no roster `status` entry. A dead
  session leaves it unverifiable.
- **Delegating judgment** — members can't ask the user. Clarifying
  requirements and deciding stay with a lead.

## Memory

`.memory/memory.json` → `crewmates`: roster tree, spawn defaults, member
status. Delegation lessons append to `shared.lessons`. Read at entry,
write at exit, own namespace only — per the `cross-skill-memory`
protocol.

## Reference files (load on demand)

- Need worked member briefs (explore / build / review) → `references/delegation-prompts.md`
- Need example roster trees for a project shape → `references/roster-examples.md`
