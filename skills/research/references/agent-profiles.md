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

## Per-spawn checklist

- Spec verbatim + the variable part in the brief: Node question, depth,
  defaults for open questions (or the claim list for a verifier).
- Concurrency: at most 5 spawned agents in flight — queue the rest and
  launch as slots free.
- Scope: a branch never sees sibling findings; a verifier never sees the
  graph, only its claims.
- One verifier context can check a whole claim list — batch, don't spawn
  per claim.
