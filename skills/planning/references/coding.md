# Coding / Engineering Plans

For features, refactors, migrations, bug-fix campaigns, or any plan that touches a codebase. The goal is a plan a fresh agent (or a future session) can execute cold: each step is self-contained, ordered by dependency, and verifiable.

## 1. Research before planning

Never plan against a codebase you haven't read. Before writing a single step:

- **Pre-flight**: check `git status` (clean tree?), the default branch, and whether the project builds/tests today. Record the commands: `npm test`, `cargo test`, `pnpm build`, etc.
- **Read the relevant code**: entry points, the modules the work touches, and any existing similar implementations to pattern-match against.
- **Check for existing plans or memory files** (`plans/`, `.plan/`, CLAUDE.md, AGENTS.md) — reuse or update instead of duplicating.
- **Confirm the conventions**: language, framework, test setup, lint rules. A plan that violates the repo's own conventions will be rewritten the moment execution starts.

If the user described the work without pointing at a repo, find the repo first (ask or locate it) before planning.

## 2. Step sizing

- Break the work into **one-PR-sized steps** — typically 3–12 for a multi-session project. A step should be independently verifiable and leave the codebase in a working state (or a state with a defined rollback).
- **Don't mix refactor and feature in one step** — each step changes one thing, so a failure points at one cause.
- If a step is bigger than a day of work, split it.

## 3. Step anatomy

Each step in the plan includes:

- **Context brief** — 2–4 sentences: what this step does, why it exists, and what it builds on. Self-contained: an executor should not need to read other steps or the planning conversation to do this step.
- **Files / components touched** — explicit paths.
- **Commands** — the exact commands to run (migrations, generators, installs, tests).
- **Verification / exit criteria** — how you know the step succeeded. Concrete: "all existing tests pass", "no `provider` imports remain outside `core/`", "`curl localhost:3000/api/health` returns 200".
- **Risks and rollback** — what could go wrong and how to back out (e.g., "migration is additive-only; revert = remove the new table").

## 4. Ordering and parallelism

- Order steps by dependency: an interface first, then its consumers; a migration before the code that reads the new schema.
- **Detect parallel steps**: steps touching disjoint files with no output dependency can run in parallel (e.g., "implement Anthropic provider" and "implement OpenAI provider" after the provider interface step lands).
- **Invariants**: if the project has global invariants (tests must pass, no secrets in config, lint clean), state them once at the top of the plan and verify after every step, not just at the end.

## 5. Output format

```markdown
# Plan: <feature name>
Date: <date> | Repo: <path> | Branch: <base branch>

## Context
<what we're building, why, and what success looks like>

## Invariants
- <verified after every step, e.g. all tests pass>

## Steps

### Step 1: <action>  (~<time>)
**Context:** <2-4 sentences, self-contained>
**Files:** <paths>
**Do:** <exact steps / commands>
**Verify:** <exit criteria>

### Step 2: <action>  (~<time>)  [parallel with Step 3]
...
```

## Anti-patterns specific to coding plans

- Planning without reading the code — steps will reference files that don't exist or miss the existing abstraction that makes the work trivial.
- Steps that depend on unknown APIs or unconfirmed permissions — surface them as questions in the plan ("confirm we have write access to the vendor registry").
- Verification that's wishful ("make sure it works") — every exit criterion must be a command, a test, or an observable.
- One giant step for the whole feature — it's not a plan, it's a TODO with extra words.
