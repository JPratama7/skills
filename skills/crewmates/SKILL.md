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
teammates, and any teammate with its own teammates is a lead running
this same SOP one level down. Members persist across prompts, so
context accumulates in the agent and in shared files.

## State layout

```
.memory/memory.json → "crewmates" namespace:
  roster    — member tree: {name, role, spawn, teammates: [...]}
  defaults  — {model, max_parallel, depth_cap: 3, fanout_cap: 5,
               roles: {writes, executes, commits, worktrees}}
  status    — per member: running | waiting:<what> | done | failed

.crew/ → bulk state in the project root:
  board.md           — shared knowledge; kills re-briefing
  inbox/<name>.md    — mail to that member
  handoff/<name>.md  — the member's catch-up note, agent-handoff format
  panes.txt          — session map, one per line: <stable-name>\t<session-id>
```

Exclude `.crew/` and `.memory/` via `.git/info/exclude`; `board.md` may
be committed. Set `waiting:` on every dispatch, report and stall — a
bare `running` hides "idle, waiting on X".

## 1. Entry: revive the crew

Read `memory.json` → `crewmates` and `shared.lessons`.

- Roster exists → boot each standing member: "load your skills → read
  `board.md`, your inbox, your handoff → post one `ready` line". The
  file read IS the catch-up — never re-paste board content into prompts.
- Each member keeps `handoff/<name>.md` current — update on task end,
  stall, or handover. Use the `agent-handoff` skill's format when it is
  installed (load it by name); otherwise prose + `Done / Pending /
  Blocker / Next`. Path stays `.crew/handoff/` — don't follow the
  skill's own default dir.
- `running` from a dead session → verify and integrate what finished,
  respawn the rest, before new work.
- No roster → crew of one; add seats when roles repeat (§3).

## 2. Interview — before the first dispatch

The crew outlives the task, so its shape is the user's call. One batch:

- **Work** — what repeats? Recurring → standing seats; one-offs → temps.
- **Shape** — their roster, or yours for approval.
- **Boundaries** — what stays with you (judgment, user contact),
  off-limit write scopes.
- **Roles** — three separate answers: who *writes* code, who *executes*
  (tests, checks, scripts, DB runs), who *commits* and integrates; plus
  worktrees (one per member vs shared). Store in `defaults.roles`; post
  `ROLES writes=<m> executes=<m> commits=<m> worktrees=<each|shared>` on
  the board — every brief points to it. Write-only builders with
  executing leads are valid but name the cost: every check is a lead
  round-trip → ≈2 builders per lead.
- **Defaults** — model, parallelism, verification depth.

Then propose the tree and get approval. Coverage check: every scope
piece maps to a seat or to you. Skip the interview for obvious
one-shots.

## 3. Decide: member, temp, or inline

- **Member** — repeats, accumulates context, or carries teammates.
  Standing seat in the roster.
- **Temp** — self-contained leaf you can verify without re-doing.
  Spawn, contract, done. Never rostered.
- **Inline** — dependent steps, small edits, judgment calls, anything
  needing the user mid-task. Work that IS communication never delegates.

A seat is earned by a second task: brief the same role twice → member.

## 4. The lead SOP — every dispatch, every level

**Brief** — the member sees only this text plus what you point it at:

```
Task: <one imperative sentence>
Start here: <file/path/endpoint to open first>

Context: <the goal, decisions already made with their why>

Constraints:
- Critical: <rules that must not be violated>
- Required: <must happen; method up to the member>

Scope: <investigate-only vs. make-changes; files/dirs it owns>

Roles: <the member's row of the board ROLES line>

Skills: <skills to load first — skills don't propagate>

Output contract: <exact return shape, evidence, failure report>

Defaults: <every open question gets "Default: X">
```

- ≤400 words. Point at files; don't paste them.
- Open question → `Default: X`. No safe default → resolve before
  dispatching.
- Contract is mandatory: exact shape (verdict + evidence, file list,
  pass/fail per item), telegraphic report. `checks` claims name the
  command that ran — `checks=pass` with no command is a failed report.
- Executing members get Critical: `timeout` long commands, no chained
  heredocs — a hung chain holds the pane for hours.
- Write-only builders get the loop spelled out: builder writes the
  failing test + hands over the exact run command → lead runs it red →
  builder writes code → lead runs it green. Every handover lists files
  written + exact commands — the builder can't see its own red.
- "Read `.crew/board.md` first" replaces context the board already holds.
- Worked examples: `references/delegation-prompts.md`.

**Dispatch.** Independent members in the same turn; disjoint write
scopes (two members on one file collide). Log every spawn in `status`.
Don't poll — the stall-check (§5) finds the stuck ones. A lead that
dispatched owns its builders: check each before going idle.

**Verify.** Output is a claim, not a fact. Check against the contract;
spot-check load-bearing claims — rerun the test, read the diff, open
the cited file:line. Compare failure *lists* against expected, never
counts: "1 failure, the known one" is how a second offence ships behind
a fixed one.

**Integrate & distill.** Upward = verdict + evidence, never raw output.
On failure, fix the brief not the work: resume with missing context or
respawn corrected. Reusable findings → board; lessons →
`shared.lessons`.

**Needs a decision.** A blocker that is the user's call goes up as
`needs-decision: <question>; Default: X; working on it`. Keep working
the default; the root batches these for the user.

**Integrate code** — pick order, baseline diffing, conflict policy,
head-posting → `references/integration.md`.

**Roles change mid-flight.** Re-brief every running task — a role rule
only binds tasks briefed after the change. Root checks each member's
status first: a `blocked` member can't hear a wake — give the user the
pane and the right answer ("No" for a now-forbidden command); never
answer another session's prompt. Leads confirm upward: "roles applied,
running tasks re-briefed."

## 5. Board and mail

**Board** — `.crew/board.md`, one line per fact under `## Conventions`,
`## APIs`, `## Rules`, `## Decisions`, `## Open questions`.

- Distilled facts only — a transcript dump is re-briefing with extra
  steps.
- Decisions: `- <date> @owner: <decision>`; prune once it lands in a
  committed AGENTS.md or plan file.
- Rules ban commands by *effect*, not name — `git switch --merge`
  autostashes, so "no stash" bans it too.
- Root prunes at session start: stale entries out, dupes merged.

**Mail** — `.crew/inbox/<name>.md`. Sending is exactly two steps:

1. Append `- from <sender>: <message>` to the reader's inbox file.
2. Wake the reader — `herdr agent prompt <to> "mail from <me>"` or the
   harness equivalent. Skip the wake only for the root lead, who polls.

Write first, then wake — a wake before the append is a silent no-op:
the reader finds an empty inbox and goes idle while you wait. After
waking, verify the reader started (`herdr agent read <to>` or
equivalent). A reader that wakes to an empty inbox replies "inbox
empty" to the sender — silence is how two members deadlock over nothing.

- Reader clears its inbox after consuming.
- Members mail each other directly — cross-lead traffic doesn't route
  through the root.
- Blocked on a decision → mail the question AND wake. A question in a
  report footer is a question nobody reads.

**Stall-check** — run every turn while members are active and whenever
the user says "all idle". One line per member — `<name>: <signals>`:

- `unread` — inbox file non-empty (file check);
- `no-deliverable` — declared path/SHA absent (file check, only when
  the brief declared one);
- `question` — last turn ended on a `?` or "waiting for X" (tail read);
- `api-error` — last turn ended in an API error (tail read).

Tail reads: `herdr agent read <name>` on panes; the agent's transcript,
resumed output, or last report file on other harnesses. Script the file
checks and fold the tail reads in per member. Run it before telling the
user "waiting on the crew" — idle panes are not finished work.

**Dispatch-request** — a member that can't spawn writes to its lead's
inbox: `- DISPATCH <role>: <task> → report to inbox <requester>`.

## 6. Spawning and portability

- **Herdr** (`HERDR_ENV=1`): `herdr agent start <name> --kind devin
  --pane <pane_id>`; re-prompt `herdr agent prompt <name> --wait`. Pane
  agents can spawn — sub-leads start their own teammates. Herdr names
  survive restarts: they are the stable identity.
- **Session map** — `panes.txt` maps stable name → live session id for
  direct-messaging harnesses. Live ids die on restart. Rebuild order:
  root writes its line first (a stale root id misroutes mail), every
  member re-appends its own, then prompt each member via stable name to
  re-read the file. Look up the address in the file on every send —
  never from memory. No live session ids on the board.
- **Plain** (`run_subagent` or equivalent): record the returned agent
  id in `status`; `resume`/re-prompt for follow-ups. A member that
  can't spawn drops DISPATCH in your inbox.
- **Dead session** → respawn; board + inbox is the catch-up. The board
  is the persistence; a live agent is a fast path.
- **Pane state** — trust `agent_status` and inbox files, never the
  input box: greyed-out prompt suggestions look like unsent orders.
- **`blocked`** — a permission prompt a wake can't pass. Never answer
  another session's prompt (permission laundering); give the user the
  pane + right answer, re-brief once unblocked.
- **Hung command** — kill the parent before the child; killing the
  child lets the parent run whatever was queued behind it.
- **Shared envs** — one `.venv` per worktree; shared venvs leave
  packages half-installed. Failing import → re-sync before trusting it.
- **API errors** — resend the task in full + "check `git status` and
  resume from what's on disk"; never a bare "continue". Two more
  failures → report to your lead.

## 7. Roster shape

Free-form tree in `crewmates.roster`. Node: `{name, role, spawn,
teammates: [...]}`.

Caps: depth ≤3, teammates ≤5 per lead — past that, coordination costs
more than parallelism saves; ≈2 builders per lead when leads execute
all checks. A lead needs ≥2 teammates — otherwise collapse it into one
member.

Default leaves: `scout` (read-only explore), `builder` (writes),
`reviewer` (verifies diffs). Example trees: `references/roster-examples.md`.

## Anti-patterns

- **Theater tree** — depth for its own sake. A two-task job needs one
  member, not a lead with two workers.
- **Wall-of-text relay** — raw worker output passed upward. The
  contract said distill.
- **Board hoarding** — transcripts, guesses, stale facts. One line,
  sourced, or cut.
- **Re-briefing the board** — pasting into a brief what the member
  reads for itself.
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

- Worked member briefs (explore / build / review) → `references/delegation-prompts.md`
- Integrating member code (pick order, conflicts, head-posting, role changes) → `references/integration.md`
- Example roster trees for a project shape → `references/roster-examples.md`
