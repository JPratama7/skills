---
name: session-debrief
description: "Conduct a session debrief on an agent coding session and propose environment improvements. Trigger ONLY on an explicit user request for a session debrief — 'debrief this session', 'run a session debrief', 'do a retrospective on this session', '/session-debrief'. Never trigger on casual 'retro' or 'retrospective' usage (retrofit, retro-style, retro gaming, art retrospectives), on session summaries or recaps, on code reviews, on incident postmortems, or on planning chats: those are not this skill."
disable-model-invocation: true
triggers:
  - user
---

The user has asked for a **retrospective**. You are suggesting improvements to the coding agent's **environment** to improve future runs.

## Steps

1. Read [`references/writing-for-agents.md`](references/writing-for-agents.md) for the writing style guide (and [`references/skill-mechanics.md`](references/skill-mechanics.md) if the session touched a skill or a proposed change is a skill). [`references/evidence.md`](references/evidence.md) holds the research behind the categories below — draw on it when a finding needs backing or the user pushes back.

2. Read the primary sources for the session the user specifies. This may mean searching through session logs on this machine. If the user doesn't specify a session, default to the current one. Ground every claim in artifacts — commands run, tool outputs, diffs, check results. An agent's written reasoning is not a faithful log of why it acted (evidence: unfaithful self-reports); a debrief built on self-narration optimizes a story, not the environment.

3. Look for candidates for improvement in these categories.

- **Missing guardrails**: automated checks that would have caught an observed error — linting, typing, tests, filesystem linters. External feedback is the one reliably-supported correction mechanism; asking an agent to check its own work with no external signal is expected to fail or regress (evidence: external feedback). Read the repo's own check command first (its `package.json`/build-tool `lint`/`check` scripts, its CI workflow), so a check that already exists but sits unwired or silently broken is the finding, not a reinvention. A repo with no **guardrail** (no pre-commit hook and no CI job running its lint/typecheck/test command) is itself a finding: an un-linted repo is a standing missed opportunity, not a neutral default. _Use when_ the agent made a mistake an automated check could have caught, or the repo has no guardrail at all.
- **Coding standards placement**: should the **reviewer agent** be given a new rule, or should an existing rule become a check? Classify the violation first: a **mechanical** one (a fixed syntactic pattern, a banned API, an import shape, a file-location rule) gets a deterministic check, full stop — a custom rule in the repo's own linter, a new pre-commit hook, or a new CI job, whichever the repo's language and existing guardrail make cheapest. Reserve `CODING_STANDARDS.md` for genuine **judgement calls** (cross-file consistency, "matches the surrounding style," anything no guardrail could substitute for). Persona and biographic prose in steering files or agent briefs is dead load — personas don't reliably improve objective performance and can hurt (evidence: personas). _Use when_ the reviewer agent failed to catch a mistake, or steering files carry persona prose.
- **Navigation & placement**: how easy was it for the agent to find the right files? Are there hidden dependencies between files? Would a **navigation pointer** help? Agents use information at the start and end of context well and the middle poorly (evidence: position bias) — put must-do rules at the edges of steering files and push reference material into disclosed docs rather than burying it mid-file. _Use when_ the session took a long time to find a piece of information.
- **Context load & no-ops**: instructions in steering files that don't modify behavior, or material loaded every turn that only some runs need. Every always-loaded line spends attention whether or not it fires, and irrelevant text measurably degrades output (evidence: context load). Global `AGENTS.md` bloat is the usual suspect — steering that belongs in checks, standards, or docs should move there. _Use when_ steering files are large and unwieldy.
- **Tool & effort economy**: expensive tool calls that could be streamlined, token-inefficient CLIs or MCPs, and reasoning-effort mismatches — easy steps burning extended thinking, or steering text dense with doubt-cues ("double-check", "wait", "re-verify") that causally inflate reasoning tokens (evidence: overthinking). Reasoning *quantity* is best set by the harness's effort parameters; prompting owns reasoning *direction* — criteria, decomposition, the done-definition. _Use when_ the agent made expensive tool calls or over-thought routine work.
- **Spec & delegation quality**: task and subagent briefs missing goal, constraints, output contract, or termination condition — the top empirically-observed agent failure modes, alongside absent output verification (evidence: spec failures). Free-form chat between agents that should be structured artifacts (files, docs, JSON). _Use when_ a delegated or multi-agent step drifted, looped, or ended without verification.
- **Interface & tool feedback**: tools and scripts that accept malformed input silently or return walls of unparseable text. A constrained action space, rejection of malformed calls, and short specific error feedback change outcomes as much as prompt wording (evidence: interface design). _Use when_ the agent fumbled a tool call and the error output didn't help it recover.
- **Information access**: opportunities to increase the agent's access to information — teed dev-server logs, read-only access to third-party services, an externalized memory file rather than history stuffed into context (evidence: externalized memory). _Use when_ a crucial piece of information was not available to the agent.
- **Skill quality**: for any skill the session touched — created, edited, invoked, or followed — grade the skill's own text against [`references/writing-for-agents.md`](references/writing-for-agents.md) and [`references/skill-mechanics.md`](references/skill-mechanics.md). The description must match the invocation choice: a model-invoked skill's description carries its trigger branches; a user-invoked one is a one-line summary with triggers stripped. Every always-loaded line must earn its context load — cut no-ops, restatements of the environment, persona prose (evidence: personas, context load). Completion criteria must be checkable; reference material goes behind pointers, must-do rules at the edges (evidence: position bias). A skill the session only followed is a weaker finding than one it authored. _Use when_ the session created or edited a skill, or followed one whose text fought it.

4. Present the candidates to the user, in order of severity. For each: the session evidence for it (or "standing risk" for absent guardrails), the concrete environment change, and its evidence class. Mark phrasing- and format-level changes as **hypotheses**: prompt wording is model- and task-specific and gains don't transfer (evidence: prompts are empirical), so recommend a way to measure the change rather than promising the improvement.

## Reference

### Implementation vs Review

Remember that all work goes through two stages: implementation and review. The implementation agent has the most **context pressure**. They are responsible for exploration, writing code, and debugging failures.

The review agent has the least context pressure - it receives a diff, so no exploration needed. It often does not need to write code or debug.

This means that the review agent should be responsible for imposing coding standards, not the implementation agent.

### Files

You have access to several files in the repo:

- `CLAUDE.md`/`AGENTS.md`: these files are pushed to the context window of any agent working in this repo. They should be used incredibly sparingly, usually only for **navigation pointers** to other files.
- `CODING_STANDARDS.md`: this file is read during review, not implementation. Add **navigation pointers** to docs folders if the standards file gets more than 1,000 lines long.
- Docs: use docs as references files, pointed to by other files. Look for existing docs before writing new ones.
- Skills: use skills for docs (since their description goes into the agent's context window), or for user-invoked commands. Follow the advice in [`references/writing-for-agents.md`](references/writing-for-agents.md).

## Reference files (load on demand)

- Style guide for any proposed doc, steering-file, or standards edit → `references/writing-for-agents.md`
- The session touched a skill, or a proposed change creates or modifies one → `references/skill-mechanics.md`
- Research backing for a category, or a user challenging a recommendation → `references/evidence.md`
