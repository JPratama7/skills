# Roster examples

Free-form trees, as they sit in `memory.json` → `crewmates.roster`. The root
node is you — `teammates` are your direct reports; a member with its own
`teammates` is a sub-lead running the same SOP.

## Small feature crew (depth 1)

The everyday shape: three standing leaves reporting to you.

```json
{"name": "main", "role": "root lead", "spawn": "standing", "teammates": [
  {"name": "scout",    "role": "read-only explore, codebase maps", "spawn": "standing"},
  {"name": "builder",  "role": "writes under src/ and tests/",      "spawn": "standing"},
  {"name": "reviewer", "role": "verifies every diff before merge",  "spawn": "standing"}
]}
```

Write scopes never overlap: scout and reviewer touch nothing, builder owns
the tree. Reviewer sees every diff before it lands.

## Full-stack feature (depth 2)

Two write-heavy domains that would collide as one crew — each gets a
sub-lead.

```json
{"name": "main", "role": "root lead", "spawn": "standing", "teammates": [
  {"name": "backend-lead", "role": "owns src/api/", "spawn": "standing", "teammates": [
    {"name": "api-scout",   "role": "trace existing route patterns", "spawn": "standing"},
    {"name": "api-builder", "role": "routes, services, migrations",  "spawn": "standing"}
  ]},
  {"name": "frontend-lead", "role": "owns src/ui/", "spawn": "standing", "teammates": [
    {"name": "ui-builder", "role": "components, styles", "spawn": "standing"}
  ]},
  {"name": "reviewer", "role": "verifies diffs from both leads", "spawn": "standing"}
]}
```

`frontend-lead` has one teammate — borderline. If ui work stays
single-track, collapse it: make `ui-builder` your direct report and drop
the lead. Leads earn their seat by coordinating ≥ 2 members.

Temps hang off this tree without entering it: a one-shot to rename a prop
across 40 files is a `run_subagent` call, not a seat.

## Test team (heavy suite)

For a project whose test runs are heavy enough to need a budget: a test
lead owns `crew-run` and answers VERIFY requests from the integrator
(`references/integration.md`), with two testers executing scoped runs.

```json
{"name": "main", "role": "root lead", "spawn": "standing", "teammates": [
  {"name": "builder",   "role": "writes under src/ and tests/", "spawn": "standing"},
  {"name": "test-lead", "role": "owns crew-run, answers VERIFY requests", "spawn": "standing", "teammates": [
    {"name": "tester-1", "role": "executes scoped runs", "spawn": "standing"},
    {"name": "tester-2", "role": "executes scoped runs", "spawn": "standing"}
  ]},
  {"name": "reviewer",  "role": "verifies diffs before merge", "spawn": "standing"}
]}
```

Two testers ≈ `crew-run`'s default cap of 3 runs — the lead's own
verification run gets the third slot. A bigger test team just queues
longer; don't grow it past what the machine budget allows.

## Research / writing project (depth 1, mixed spawn)

```json
{"name": "main", "role": "root lead", "spawn": "standing", "teammates": [
  {"name": "researcher", "role": "accumulates source knowledge on the topic", "spawn": "standing"},
  {"name": "editor",     "role": "knows the voice, reviews drafts",           "spawn": "standing"}
]}
```

`researcher` is where standing pays off: it holds the source map across
sessions via the board. Fact-checks stay temps — a fresh pair of eyes per
claim batch, spawned and gone.

## When to grow a seat

- Second task repeats a role → temp becomes standing.
- One member's queue holds two independent domains → split into two
  members or give it teammates (sub-lead).
- A member's briefs keep needing "read board section X first" → that
  section is its context; confirm the board section exists and stays
  pruned.
