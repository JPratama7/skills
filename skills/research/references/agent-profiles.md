# Agent profiles — harness-agnostic spawn specs

Two portable profiles: `research-branch` explores one graph node;
`claim-verifier` checks load-bearing claims. A profile = *capabilities* +
*spec text*. Capabilities tell you which built-in subagent kind to pick;
the spec always travels in the prompt — a harness profile grants tools,
never behavior.

## Instantiating a profile

1. Harness has typed subagent profiles/agent kinds → pick the closest
   match on capabilities, then include the spec verbatim in the brief.
2. Harness takes a role/system preamble → spec goes there; the task
   details (Node, depth, defaults) stay in the brief.
3. Neither → prepend the spec to the task brief.

Never drop the spec because a built-in profile has a matching name — the
name selects tools, the spec produces the contract. Conversely, never
pick a writable agent kind for a read-only profile: a branch that edits
is a failed spawn.

A headless one-shot worker takes the spec inside its task brief, and its
report IS its stdout — the spawn recipe redirects the stream to the
findings file rather than asking the agent to write files itself. A
captured stream can't be half-written.

## research-branch

**Capabilities:** web search + page fetch (or doc/source readers).
Read-only — no writes, no edits, no children of its own. If the closest
available kind lacks fetch, it still qualifies if it can read cited pages
some other way; if it can only search, do the branch inline instead.

**When to spawn:** branches needing independent multi-source exploration.
A branch resolvable with one or two direct fetches is an inline lookup —
the spawn costs more than the fetch.

**Spec (paste verbatim):**

> You are a research-branch agent: one node in a research graph run by a
> coordinator. Investigate only your assigned sub-question — sibling
> agents cover the rest; don't wander into their territory.
>
> Sources: primary only — official docs, specs, source code, first-party
> APIs, papers. A blog citing the docs is a pointer: follow it to the
> docs. Fetch every URL you cite — a search snippet is not evidence.
>
> Report telegraphic, ≤10 finding lines (≤5 on quick depth), ≤2 sources
> per line:
>
>     Node: <sub-question>
>     Findings: claim — primary source URL — strong|weak
>     New questions: <child-node candidates, or none>
>     Contradictions: <conflicts found, or none>
>
> strong = primary + corroborated; weak = single or secondary source
> only. Stop when the question is answered, dead-ended, or exhausted —
> return what you have; don't pad.

## claim-verifier

**Capabilities:** page fetch. Read-only. No search — URLs arrive with the
assignment; add one only when a cited URL is dead and the claim is
load-bearing, and say you did.

**When to spawn:** batch spot-checks of claims that decide the root
answer — three or more, or sources needing real re-reading. Also for
re-checking a suspect branch (all-weak findings, contradicted by a
sibling). One or two claims = verify inline.

**Spec (paste verbatim):**

> You are a claim-verifier agent. You do not explore — you check specific
> claims against their cited sources and report whether each holds.
>
> For each assigned claim, fetch the cited URL, compare, report one line:
>
>     verdict — claim — URL — note
>
> verdict: confirmed | refined | refuted | unreachable.
> refined = the source supports a narrower or different version — state
> it in the note. unreachable = the fetch failed — say why. One note
> sentence max: evidence, not commentary.

## Delivery — push, not poll

A spawned worker's report is two parts, always in this order:

1. **Findings file** — the durable store. For a headless worker it is
   captured stdout, redirected by the spawn recipe; for a resident
   agent it is the path named in its brief.
2. **Ping** — one line on the coordinator's push channel:
   `<branch> → <lead>: findings at <path>` (or `failed — <reason>`).
   The ping names the path; the body never rides the channel.

Integrate each report when its ping lands. Never poll a worker —
repeated reads spend your turn to learn nothing the push won't
deliver. The one exception is liveness: a branch silent past its
expected window earns a single probe (a state read or a file check),
and a dead one gets respawned or folded — a live one gets left alone.
A harness with no push channel blocks once on its `wait` primitive;
a read loop is the only wrong answer.

## Resolving the push channel

Nothing here names a substrate — the Workers checkpoint item picks one,
then you learn its push channel once and cache it. Five primitives:

| primitive | job |
|-----------|-----|
| `spawn`   | start the worker and hand it the brief |
| `deliver` | land findings at a durable path — stdout redirect or an agent-written file |
| `push`    | a worker-initiated signal that reaches your context |
| `probe`   | a liveness read, for the silent-branch exception only |
| `wait`    | optional — the single blocking fallback when `push` doesn't exist |

A channel counts as `push` only when the worker side fires it and it
lands in your context without you running a read — a completion
notification, a message-injection tool, a prompt/pane command the
worker's shell can invoke, a wake hook. A file the worker writes is
`deliver`, not `push`: files don't wake anyone, so a deliver-only
recipe lands in fallback 3 below, no matter how it's spawned.

Resolution order:

1. **Harness's own subagent tool** — a completion notice is a
   ready-made push. Background/parallel spawning only; a foreground
   spawn blocks your turn, and that IS sequential mode.
2. **The substrate the user picks** — a headless agent CLI, a pane or
   process mechanism, another harness entirely. Inventory its docs or
   `--help` for a channel that can address you; learn your address on
   it (session name, pane id, agent name — whatever the channel
   targets). Whatever it can't do falls to the generic shape below.
3. **Nothing can wake you** — the findings file is the channel. Block
   once on `wait` where the harness has one; without it, check files
   when your turn returns to the run — never on a timer.

The generic worker shape, when the substrate has a shell:

```sh
worker-cmd "$brief" > <findings-path> 2> <err-path> ; \
  notify-cmd <you> "branch-N → <lead>: findings at <findings-path>"
```

`;`, not `&&` — the ping fires even on a dead run, with whatever the
file holds. A `timeout` in front of `worker-cmd` is the dead-man's
switch that makes "silent past its window" mean something. One caveat:
a worker that buffers its report until exit leaves an empty file when
killed — where the substrate streams a log (a session file, a json
event stream, a transcript), point `deliver` at that instead so partial
findings survive the dead-man's switch.

**Prove a new channel before fan-out.** First use of a resolved recipe
buys one canary: a trivial branch on quick depth whose whole job is to
land its file and ring the doorbell. It passes only if the ping reaches
you unasked — a canary you had to go read means the recipe is
`deliver`-only; reclassify it before spending real branches on it.

Cache the learned recipe under `research.worker` in memory:
`{substrate, model, spawn-shape, push-channel, push-target,
verified-at}`. A verified cache skips the canary next run; an
unverified or changed pick doesn't.

## Per-spawn checklist

- Spec verbatim + the variable part in the brief: Node question, depth,
  defaults for open questions (or the claim list for a verifier).
- Delivery resolved before spawn: findings path + your push target
  (agent name or pane id); the ping names the path, never the body.
- Concurrency: at most 5 spawned agents in flight — queue the rest and
  launch as slots free (a slot is an arrived ping).
- Scope: a branch never sees sibling findings; a verifier never sees the
  graph, only its claims.
- One verifier context can check a whole claim list — batch, don't spawn
  per claim.
