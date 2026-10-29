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
  defaults  — {model, max_parallel, depth_cap: 3, fanout_cap: 5,
               roles: {writes, executes, commits, worktrees}}
  status    — last known state per member:
              running | waiting:<who/what> | done | failed

.crew/ → bulky state in the project root:
  board.md         — shared knowledge; the memory that kills re-briefing
  inbox/<name>.md  — mail addressed to that member
  panes.txt        — session map: stable name → live session id (§6)
```

Exclude `.crew/` and `.memory/` via `.git/info/exclude`, not
`.gitignore` — runtime state is local to this checkout. `board.md` may
still be committed if the project wants the knowledge. Update `waiting:`
on every dispatch, report and stall — most lost time is "idle, waiting
on X", which a bare `running` hides.

## 1. Entry: revive the crew

On every skill entry, read `memory.json` → `crewmates` and `shared.lessons`.

- Roster exists → bring standing members up (§6). Boot prompt per
  member: load your skills → read `board.md`, your inbox, and your
  handoff file → post one "ready" line. That file read IS the catch-up —
  never paste context the board already holds into a prompt.
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
- **The roles** — three separate questions, not one: who *writes* code,
  who *executes* (tests, checks, scripts, DB runs), who *commits* and
  integrates — plus worktrees (one per member vs shared). Store the
  answers in `crewmates.defaults.roles` and post one `ROLES` line on
  the board that every brief points to. Write-only builders with
  executing leads are a valid split — but name the cost when the user
  picks it: every check becomes a lead round-trip, so fan-out drops to
  ≈2 builders per lead.
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

Roles: <the member's row of the board ROLES line — writes? executes?
       commits? which worktree>

Skills: <skills to load first, by name or path — skills don't propagate>

Output contract: <exact return shape, evidence expected, failure report>

Defaults: <every open question gets "Default: X">
```

- Cap ~400 words. Point at files; don't paste them.
- Every open question gets a default. A question with no safe default is a
  blocker you resolve before dispatching.
- The output contract is not optional — specify the shape (verdict +
  evidence, file list, pass/fail per item) and ask for a telegraphic
  report: findings only, no preamble. A `checks=pass` claim names what
  actually ran — a check that never ran is a failed run, not a pass.
- Members that execute get this Critical: wrap long-running commands in
  `timeout` and never chain heredocs — a hung chain holds the pane for
  hours.
- Write-only builders (leads execute, §2) get the loop spelled out:
  builder writes the failing test and hands over the exact run command →
  lead runs it red → builder writes the code → lead runs it green. Every
  handover lists files written plus exact commands — the builder can't
  see its own red.
- "Read `.crew/board.md` first" replaces context the board already holds.
- Worked examples: `references/delegation-prompts.md`.

**Dispatch.** Independent members go in the same turn. Write scopes stay
disjoint — two members editing one file collide; merge or sequence them.
Log every spawn in roster `status`. Don't poll: work your own tasks while
members run; the stall-check (§5) is how you find the stuck ones. A lead
that dispatched work owns its builders' progress — check every
dispatched member before going idle yourself.

**Verify.** Member output is a claim, not a fact. Check it against the
output contract first — a great answer to the wrong question is a failed
run. Spot-check load-bearing claims: rerun its test, read its diff, open
the file:line it cites. Compare the *list* of failures against the
expected list, never the count — "1 failure, the known one" is how a
second offence ships behind a fixed one.

**Integrate & distill.** What you report upward is a distillation, never a
relay — your lead gets verdict + evidence, not raw worker output. On
failure, fix the brief, not the work: resume with the missing context or
respawn corrected. Post reusable findings to the board; append a lesson
to `shared.lessons` after a failure or a win worth keeping.

**Needs a decision.** A blocker that is the user's call goes up as
`needs-decision: <question>; Default: X; working on it` — state your
default and keep working it. The root batches these for the user
instead of stalling one member per question.

## 4.5 Integrate code

Whoever integrates (§2 roles) keeps one integration branch and a
scripted pick loop — a `pick.sh` that applies a member's commits — so
order and checks stay consistent.

- **Baseline first.** Run the suite once on the base commit, in a
  separate worktree — never check out an old commit in the main tree.
  Diff every batch's failures against that baseline: pre-existing vs
  new.
- **Pick order.** One member's batch at a time, in dependency order;
  run the suite after every batch, not once at the end.
- **Expected conflicts.** Shared registry files conflict by design —
  keep both sides for imports and mounts; for exclusion lists, drop
  what a later pick already ported.
- **Post the head fast.** The moment a batch verifies, mail the new head
  SHA to every lead so they branch from it. Long merge gates land later
  as their own commit on top — never hold a green head hostage while
  leads wait on it.
- **Carry fixes down.** Leads rebase or carry integration fixes onto
  long-lived branches promptly, or a failure already fixed upstream
  keeps firing downstream — and masks the next real one.

**Roles change mid-flight.** Re-brief every running task — a role rule
only binds tasks briefed after the change. The root checks each member's
status first: for a `blocked` one, tell the user which pane and which
answer to give ("No" for a now-forbidden command) — never answer another
session's prompt yourself (permission laundering). Leads confirm
upward: "roles applied, running tasks re-briefed."

## 5. Board and mail

**Board** — `.crew/board.md`, one line per fact under stable sections
(`## Conventions`, `## APIs`, `## Rules`, `## Decisions`,
`## Open questions`).

- Members post distilled facts, never transcripts. A board dump is a
  re-briefing with extra steps.
- `## Decisions`: one line each — `- 2026-10-29 @owner: decision`. Prune
  a decision once it lands in a committed AGENTS.md or plan file.
- `## Rules` bans commands by *effect*, not by name — `git switch
  --merge` autostashes, so a "no stash" rule bans it too.
- Root lead prunes at session start: cut stale entries, merge dupes. A
  rotting board misleads worse than no board.

**Mail** — `.crew/inbox/<name>.md`. Sending is always two steps:

1. Append `- from <sender>: <message>` to the reader's inbox file.
2. Wake the reader — `herdr agent prompt <to> "mail from <me>"` or the
   harness equivalent. Skip the wake only for the root lead, who polls.

Write first, then wake: a wake that lands before the append is a silent
no-op — the reader finds an empty inbox and goes idle while you wait on
its reply. After waking, check (`herdr agent read <to>`) that the reader
actually started. A reader that wakes to an empty inbox replies "inbox
empty" to the sender instead of going quiet — silence is how two
members deadlock over nothing.

- The reader clears its inbox after consuming.
- Members write to each other's inboxes directly — cross-lead
  coordination does not route through the root.
- A member blocked on a decision mails the question *and* wakes its
  lead — a question sitting only in a report footer is a question
  nobody reads.

**Stall-check** — run every turn while members are active and whenever
the user says "all idle". One line per member, checking:

- unread inbox — file non-empty (pure file check);
- expected deliverable missing — file check, only when the brief
  declared a path or SHA;
- last turn ended on a question or "waiting for X" — the member's
  output tail: `herdr agent read <name>` on panes; the agent's
  transcript, resumed output, or last report file on other harnesses;
- last turn ended in an API error — same tail read.

Script the two file checks; on panes the same script can call
`herdr agent read` for the tail signals, elsewhere the tail read is
the lead's per-member routine — either way, one line per member. Run
it before telling the user "waiting on the crew" — idle panes are not
finished work.

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
  so sub-leads spawn their own teammates directly. Herdr names survive
  restarts — they are each member's stable identity.
- **Session map** — `.crew/panes.txt` maps stable name → live session id
  for harnesses with direct session messaging. Live ids do NOT survive
  restarts. After any restart: the root writes its own line first — a
  stale root id routes mail to the wrong agent — then every member
  re-appends its own line, and the root prompts each member (via herdr
  names) to re-read the map. Members look up an address in the file on
  every send, never from memory. Never write a live session id on the
  board.
- **Plain** (`run_subagent` or equivalent): the spawn returns an agent id
  — record it in roster `status` and `resume`/re-prompt it for follow-ups.
  If a member's harness cannot spawn, it drops a DISPATCH line in your
  inbox; you spawn the worker, which reports to the requester's inbox.
- **Across sessions**: if pane/agent ids don't survive, respawn the
  member — it reads board + inbox and is caught up. The board is the real
  persistence; a live agent is a fast path.
- **Reading pane state**: trust `agent_status` and the inbox files, never
  the pane's input box — harnesses show greyed-out prompt suggestions
  that look exactly like an unsent order.
- **Blocked members**: `blocked` means a permission prompt your wake-up
  can't pass. Don't answer another session's prompt — that's the user's
  call (permission laundering). Give the user the pane and the right
  answer, then re-send the brief once unblocked.
- **Hung commands**: if a member's command hangs, kill the parent
  process before the child — killing the child alone lets the parent run
  whatever was queued behind it.
- **Shared envs**: each member runs against its own worktree's `.venv` —
  several agents on one shared venv leave packages half-installed.
  Before trusting a failing import, re-sync.
- **API errors**: retry by re-sending the task in full, plus "check
  `git status` and resume from what's on disk" — never a bare
  "continue". Two more failures → report to your lead.

## 7. Roster shape

Free-form tree in `memory.json` → `crewmates.roster`. Node shape:

```json
{"name": "backend-lead", "role": "owns src/api/", "spawn": "standing",
 "teammates": [ {"name": "api-scout", "role": "read-only trace", "spawn": "standing"} ]}
```

Caps: depth ≤ 3, teammates ≤ 5 per lead — past that, coordination costs
more than the parallelism saves. When leads execute all checks (§2
roles), cap ≈2 builders per lead — every test run is a lead round-trip
and extra builders just queue. A lead needs ≥ 2 teammates; otherwise
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
- **Half-sent mail** — append without the wake, or wake before the
  append. Both sides stall silently (§5).
- **Verdict by count** — "1 failure, the known one" is not a check.
  Compare the offence list; a known red hides new ones.
- **Held green head** — sitting on a verified head while a long gate
  runs stalls every lead waiting to branch. Post the SHA, gate later.
- **Answering another session's prompt** — permission laundering. Give
  the user the pane and the right answer instead.
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
