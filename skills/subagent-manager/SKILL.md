---
name: subagent-manager
description: Delegate work to subagents correctly — when to delegate, how to brief, parallel launches, verify before integrating. Use whenever you might spawn a subagent, face parallelizable work, or need exploration that would flood context — even if the user never says 'subagent'. For DAG decomposition plans, use graph-decompose instead.
---

# Subagent Manager

You are the manager. Subagents are reports who are stateless, can't see your
conversation, and can't ask clarifying questions until they're already minutes
deep. Every delegation failure is context loss — the brief lacked needed state,
or the result came back unusable. Apply this SOP automatically whenever
delegation is on the table; the user should not have to ask.

## 1. Decide: delegate or do it inline

Delegation is a bet that briefing + verification costs less than doing it
yourself.

Delegate when:

- **Independent tasks can run in parallel** — no shared state or overlapping
  files.
- **Exploration would flood your context** — "find where X lives" in unfamiliar
  code. The subagent burns its context on the search; you get the distilled
  answer.
- **The task is self-contained and verifiable** without re-doing it.
- **A chain has resolved far enough to fan out** — once a shared dependency is
  frozen, downstream branches may be independent. E.g. after a new module's API
  is fixed, its tests are independent of the caller updates — delegate the
  branch, keep the trunk inline.

Do it inline when:

- **Steps depend on each other** — sequential subagents add latency and lose
  context at every handoff.
- **The task is small and you already hold the context** — a brief costs more
  than the edit.
- **Judgment calls or user interaction are needed mid-task** — the subagent
  can't ask, so it guesses or stalls.
- **The work IS communication** — clarifying requirements or debating design
  with the user stays in the main thread.

## 2. Brief: the delegation prompt

The brief is the entire world the subagent sees. Order matters — it reads top
to bottom:

```
Task: <one imperative sentence — what to do>
Start here: <the file/path/endpoint to open first>

Context: <the goal restated, decisions already made with their why,
          relevant state the subagent can't see>

Constraints:
- Critical: <1-3 rules that must not be violated>
- Required: <things that must happen, method up to the agent>

Scope: <investigate-only vs. make-changes; which files/dirs it owns>

Skills: <optional — skills the subagent must load before starting,
         by name or path>

Output contract: <exactly what to return — format, evidence expected,
                  what to report on failure>

Defaults: <every open question gets "Default: X" so the agent moves
           instead of guessing>
```

- **Cap at ~400 words** — longer means you're dumping context. Push detail into
  files the subagent reads on demand; point at them by path.
- **One sentence for the task** — if you can't, the task isn't decomposed
  enough; split it first.
- **Constraints before narrative** — a buried rule gets missed.
- **Every open question gets a default** — a question with no safe default is a
  blocker you resolve before spawning.
- **The output contract is not optional** — "report back" returns a wall of
  text. Specify the shape: verdict + evidence, file list, pass/fail per item.
- **Ask for a compressed report** — subagent output lands in your context
  verbatim, so telegraphic style costs you half the tokens: facts, paths,
  verdicts; no preamble, hedging, or restating the task. E.g. *"Report
  telegraphic: findings only, no filler."*
- **State whether it writes or only reads** — an explore agent that edits is a
  failure.
- **Skills don't propagate — load them explicitly.** A subagent starts clean;
  a skill in your context is not in theirs. Use the `Skills:` field when the
  task needs one: name the skill if the harness resolves names (e.g.
  *"Invoke the `tdd` skill first"*), or give a path if it doesn't (*"Read
  `~/.config/devin/skills/tdd/SKILL.md` and follow it"*). If you only need one
  rule from a skill, paste the rule instead — a whole SKILL.md costs the
  subagent context for nothing.

If the `agent-handoff` skill is available, it covers brief format in more
depth — use it for unusually complex delegations. For worked examples see
`references/delegation-prompts.md`.

## 3. Launch

- **Independent agents go in the same turn** — sequential launches serialize
  what should be parallel.
- **Disjoint write scopes** — two agents editing the same file collide. Merge
  or sequence such tasks.
- **Background for parallel fan-out; foreground when you need the answer**
  before your next step.
- **Human-readable titles** so completion notifications stay legible.
- **Cheapest capable profile** — a read-only agent that needs to write is dead
  on arrival.

## 4. Monitor

Don't poll — wait for the completion notification; check only when an agent
seems stuck. Never idle while agents run: prep integration, draft checks, or
continue the work you kept inline.

## 5. Integrate: verify before trusting

Subagent output is a claim, not a fact — verification is what you pay for not
re-doing the work.

- **Check against the output contract first** — a great answer to the wrong
  question is a failed run.
- **Spot-check load-bearing claims** — rerun its tests, read its diff, open the
  file:line it cites.
- **Distill, don't relay** — the user never sees raw subagent output.
- **On failure, fix the brief, not the work** — resume with the missing context
  or respawn with a corrected brief. Take over inline only when the remainder
  is trivial.

## Anti-patterns

- **"Go look at this" delegation** — no context, no contract; the agent guesses.
- **Sequential subagents for dependent work** — context dropped at every
  handoff, zero parallelism gain.
- **Transcript dump** — your whole conversation pasted into the brief.
- **Trust without verification** — merging a diff or relaying a conclusion
  unchecked.
- **Delegating communication** — subagents can't ask the user or make your
  judgment calls.

## Reference files (load on demand)

- Need worked delegation prompts (explore / build / review) → `references/delegation-prompts.md`
