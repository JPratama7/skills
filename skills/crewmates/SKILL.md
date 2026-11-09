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
  defaults  — {model, kind, max_parallel, depth_cap: 3, fanout_cap: 5,
               roles: {writes, executes, commits, worktrees}}
  status    — per member: running | waiting:<what> | done | failed

.crew/ → bulk state in the project root:
  board.md           — shared knowledge; kills re-briefing
  inbox/<name>.md    — mail to that member
  handoff/<name>.md  — the member's catch-up note, agent-handoff format
  panes.txt          — channel addresses: <stable-name>\t<live session-id>
```

Exclude `.crew/` and `.memory/` via `.git/info/exclude`; `board.md` may
be committed. Set `waiting:` on every dispatch, report and stall — a
bare `running` hides "idle, waiting on X".

## 1. Entry: revive the crew

Read `memory.json` → `crewmates` and `shared.lessons`.

- Map the channel before any boot or dispatch (§6): which of
  `notify`/`tail`/`wait`/`probe`/`signal` does this harness give each
  member? Missing primitives take their file fallback now — a member
  you can't wake has its mail relayed by a lead, not left in a file
  nobody reads.
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
- **Defaults** — model, agent `kind` (claude, devin, …), parallelism,
  verification depth.

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

Tests: <exact test scope — files, dirs, or a -k/-m filter; "full suite"
       only when the user asked. Run through scripts/crew-run; name a
       --class for a heavy objective suite>

Roles: <the member's row of the board ROLES line>

Skills: <skills to load first — skills don't propagate>

Output contract: <exact return shape, evidence, failure report>

Comms: mail your report to <lead>; notify "<name> → <lead>: report <one-line outcome>"

Defaults: <every open question gets "Default: X">
```

- ≤400 words. Point at files; don't paste them.
- Open question → `Default: X`. No safe default → resolve before
  dispatching.
- Contract is mandatory: exact shape (verdict + evidence, file list,
  pass/fail per item), telegraphic report. `checks` claims name the
  command that ran — `checks=pass` with no command is a failed report.
- Executing members get Critical: `timeout` long commands, no chained
  heredocs — a hung chain holds the pane for hours. Every test run goes
  through `scripts/crew-run` (§6 resource budget).
- Write-only builders get the loop spelled out: builder writes the
  failing test + hands over the exact run command → lead runs it red →
  builder writes code → lead runs it green. Every handover lists files
  written + exact commands — the builder can't see its own red.
- "Read `.crew/board.md` first" replaces context the board already holds.
- Worked examples: `references/delegation-prompts.md`.

**Dispatch.** Independent members in the same turn; disjoint write
scopes (two members on one file collide). Log every spawn in `status`.
Confirm each dispatch took — `wait` for the working transition where
the harness has it, `tail` once where it doesn't; a prompt that was
accepted then dropped is an orphan nobody sees. Then don't poll — the
stall-check (§5) finds the stuck ones. A lead that dispatched owns its
builders: check each before going idle.

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
the default; the root batches these for the user — `signal` once with
the count, never once per item.

**Integrate code** — pick order, baseline diffing, conflict policy,
head-posting → `references/integration.md`.

**Retire a member.** The stop point is the command running now — the
member starts nothing new; "finish your run" means that run, not the
series. Before its seat closes it lists the steps it didn't run, for its
lead. The pane closes only when no test process still runs under it —
check with `scripts/stall-check`; a retired member holding a live run is
a zombie burning the machine.

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

**Mail** — the inbox file is the store; the channel is only the
doorbell. Sending is exactly two steps:

1. Append `- from <sender>: <message>` to `.crew/inbox/<name>.md` —
   full body, durable, ordered across senders. Use `scripts/inbox.py`
   for send/consume/list — hand-rolled clears miss lines.
2. `notify` the reader: `<from> → <to>: <subject>` — direction plus
   ≤8 words naming what arrived, never the body. The root's wake-up
   goes through the harness's message tool (SendMessage where the crew
   runs claude), never typed into a pane a person uses — typed input
   lands mid-keystroke and reads as a user message.

Write first, then notify — a notify before the append is a silent
no-op: the reader finds an empty inbox and goes idle while you wait.
After notifying, confirm it landed — `wait`/`probe` for activity where
the harness has it; a channel that accepts-then-drops is worse than
none, so fall back to relay-by-lead when a notify can't be confirmed.
A reader that wakes to an empty inbox replies "inbox empty" to the
sender — silence is how two members deadlock over nothing.

- Reader clears its inbox after consuming — and reads it on every
  wake, not just boot: a notify means mail arrived.
- Members mail each other directly — cross-lead traffic doesn't route
  through the root. No member→member channel → the lead relays.
- Blocked on a decision → mail the question AND notify. A question in a
  report footer is a question nobody reads.

**Wait, don't poll** — where the harness gives `wait`, block on the
state instead of looping on `tail`: `wait blocked` right after a
dispatch catches a permission wall in seconds, not at the next
stall-check. Passive completion notices (subagent results, completion
badges) are inbound mail too — integrate on arrival. No `wait`
primitive → the stall-check is the whole loop.

**Stall-check** — the audit layer under `wait`, and the whole loop on
file-only harnesses. Run every turn while members are active and
whenever the user says "all idle". One line per member — `<name>:
<signals>`:

- `unread` — inbox file non-empty (file check);
- `no-deliverable` — declared path/SHA absent (file check, only when
  the brief declared one);
- `bg-running` — a test or long command still running under the
  member's process, matched by the runner's name (pytest, vitest…),
  never by `uv` alone (process check — "idle" panes hide live runs);
- `question` — last turn ended on a `?` or "waiting for X" (tail read);
- `api-error` — last turn ended in an API error (tail read).

The file and process checks run as `scripts/stall-check`; fold the
tail reads in per member — `tail` per the comms map
(`references/harness-comms.md`), last report file on file-only
harnesses. Run it before telling the user "waiting on the crew" —
idle panes are not finished work.

**Dispatch-request** — a member that can't spawn writes to its lead's
inbox: `- DISPATCH <role>: <task> → report to inbox <requester>`.

## 6. Channel map and portability

The crew needs six primitives — resolve yours before the first
dispatch:

| primitive | job |
|-----------|-----|
| `spawn`   | start a member, deliver its brief |
| `notify`  | deliver a compact message into a member's context |
| `tail`    | read a member's recent output |
| `wait`    | block until a member reaches a state |
| `probe`   | read a member's lifecycle state |
| `signal`  | reach the user out-of-band |

Resolve at entry — capability first, env var second:

1. **Native inventory** — which of the six do your own tools cover? A
   subagent-spawn tool gives spawn/tail/probe/passive-wait; a
   SendMessage-style tool gives notify into any session it can name —
   including members on another substrate (herdr panes running claude).
2. **Gap check** — spawn or notify missing → probe herdr:
   `HERDR_ENV=1` AND a live `herdr` answer (the env var survives dead
   servers). Live → herdr panes fill the missing primitives.
3. **Neither** → file fallbacks per primitive: no `notify` → leads
   relay mail on next contact and members read inbox on every wake;
   no `wait` → the stall-check is the loop; no `tail` → report files.

A member's channel follows its substrate: herdr-spawned → herdr
primitives, builtin-spawned → builtin primitives. Concrete commands
per harness → `references/harness-comms.md`. Store the resolved map in
`status` so a reboot skips detection. If spawn or notify resolved to
a file fallback, put the degraded map in front of the user in the §2
interview — channel quality shapes the whole crew; relay-by-lead is
real coordination cost, and the user may fix the channel instead.

- **Resource budget** — every executor runs tests through
  `scripts/crew-run`: it caps concurrent runs (`CREW_MAX_RUNS`),
  serializes a named heavy class (`--class`), refuses to start under a
  free-RAM floor, and redirects temp files to disk. A check in a script
  beats a rule in a brief — a crew that races unguarded runs has
  already lost the machine to swap and tmpfs.
- **Session map** — `panes.txt` maps stable name → live session id for
  direct-messaging harnesses. Live ids die on restart. Rebuild order:
  root writes its line first (a stale root id misroutes mail), every
  member re-appends its own, then `notify` each member via stable name
  to re-read the file. Look up the address in the file on every send —
  never from memory. No live session ids on the board. When wake-ups
  go through the harness's message tool (SendMessage), it addresses
  members by session name: root's line first, builder names filled in
  from their worktree-named sessions, every other member registering
  its own at boot.
- **Can't spawn** — a member without `spawn` drops DISPATCH in your
  inbox; on spawn-capable harnesses sub-leads run their own teammates.
  Log every returned agent id in `status`.
- **Dead session** → respawn; board + inbox is the catch-up. The board
  is the persistence; a live agent is a fast path.
- **Pane state** — trust `probe` and inbox files, never the input box:
  greyed-out prompt suggestions look like unsent orders.
- **`blocked`** — a permission prompt a notify can't pass. Never answer
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
- **Half-sent mail** — append without the notify, or notify before the
  append. Both sides stall silently (§5).
- **Body-in-channel** — the mail body in the notify. It bypasses the
  durable store, dies with the session, and breaks multi-sender order.
- **Typed wake-up** — `send-keys`/`send-text` into a pane a person
  uses. It lands mid-keystroke and reads as a user message; the root's
  wake-up goes through the message tool.
- **Bare wake** — `mail from me` with no subject. The reader opens the
  file just to triage; say what arrived in ≤8 words.
- **Poll-loop on a wait-capable harness** — tail-sleep-repeat when
  `wait` blocks for free. Burns the lead's turn — and on some channels
  each poll lands as input and burns the member's too.
- **Unmapped channel** — assuming a `notify` the harness lacks. The
  mail sits, the stall-check reads clean, both sides wait.
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

- Per-harness comms maps (spawn/notify/tail/wait/probe/signal commands) → `references/harness-comms.md`
- Worked member briefs (explore / build / review) → `references/delegation-prompts.md`
- Integrating member code (pick order, conflicts, head-posting, role changes) → `references/integration.md`
- Example roster trees for a project shape → `references/roster-examples.md`

## Bundled scripts

- `scripts/crew-run` — test-run gate: concurrency cap, `--class` serialization, RAM floor, disk TMPDIR (§6)
- `scripts/stall-check` — unread/no-deliverable/bg-running signals per member (§5)
- `scripts/inbox.py` — inbox send / `consume --match` / list (§5)
- `scripts/pick.sh` — scripted cherry-pick with lockfile + pyproject conflict resolution (`references/integration.md`)
