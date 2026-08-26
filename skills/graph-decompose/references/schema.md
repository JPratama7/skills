# JSON Schema — graph-decompose plan

Full field-level reference for the JSON object exported by `scripts/graph.py`. The script is the canonical emitter — do not hand-write this JSON. Use this doc to understand the export contract, to write graders that check a decomposition programmatically, or to hand-edit an exported plan (then re-validate with `graph.py --db <db> validate` if you still have the DB).

## Top-level object

```json
{
  "task": "string",
  "granularity": "single-subagent-call | one-logical-step | one-file-edit",
  "model": "string",
  "skills": ["skill-name"],
  "nodes": [Node],
  "summary": Summary
}
```

| Field | Type | Constraint |
|---|---|---|
| `task` | string | One sentence, the done-when-true statement. Not a restatement of the user's prompt — the sharpened version. |
| `granularity` | enum | Must match what the user requested. Default `single-subagent-call`. |
| `model` | string, optional | Default model for nodes without their own `model`. Echoed verbatim from the user's request (id or tier like `fast`/`cheap`/`strong`). Absent = harness default. |
| `skills` | array of string, optional | Default skills for nodes without their own `skills`. Echoed verbatim from the user's request. Absent = no skill instructions. |
| `nodes` | array | ≥1 node. Every node id unique. |
| `summary` | object | See Summary. Computed from `nodes`, not free text. |

## Node

```json
{
  "id": "string",
  "name": "string",
  "model": "string",
  "skills": ["skill-name"],
  "prompt": "string",
  "deps": ["id"],
  "inputs": ["dep_id:artifact_name"],
  "outputs": ["artifact_name"],
  "verify": "string"
}
```

| Field | Type | Constraint |
|---|---|---|
| `id` | string | Kebab/snake-safe. Unique across `nodes`. Short (`n1`, `read-spec`, `gen-types`). |
| `name` | string | ≤60 chars, human-readable, outcome-oriented ("generate TypeScript types" not "step 2"). |
| `model` | string, optional | Overrides top-level `model` for this node. Free-form (id or tier), echoed verbatim from the user's request. Non-empty when present. |
| `skills` | array of string, optional | Overrides top-level `skills` for this node. Skill names echoed verbatim from the user's request. Every entry non-empty when present. |
| `prompt` | string | **Self-contained and terse.** No references to the parent conversation, no preamble ("you are a..."), no restated task, no pleasantries. Imperative voice, one instruction per line, inline only the context slice the subagent needs. A fresh subagent with only this string + `inputs` must be able to execute it. Prefer 3 lines over 10; every word earns its place. |
| `deps` | array of id | Every id must exist in `nodes`. Empty = ready at wave 0. No cycles (see Validation). |
| `inputs` | array of string | Format `dep_id:artifact_name`. Must line up with `deps` and the dep's `outputs`. A node with a dep but no matching `inputs` entry is a hidden-dep smell — either the input list is wrong or the dep is fake. |
| `outputs` | array of string | Concrete artifact names downstream nodes can reference. `["types.ts", "schema.json"]`, `["decision: use-postgres"]`, `["test-results.json"]`. Not vague ("the result"). |
| `verify` | string | Objective check. Command, test, diff, or structural assertion. Not "looks good" or "review the output". |

## Summary

```json
{
  "node_count": "int",
  "wave_count": "int",
  "critical_path": ["id"],
  "bottlenecks": ["id"],
  "honest_parallelism": "string"
}
```

| Field | Type | Constraint |
|---|---|---|
| `node_count` | int | `len(nodes)`. |
| `wave_count` | int | Longest path length + 1. Number of sequential waves if executed max-parallel. |
| `critical_path` | array of id | The longest dependency chain (one of them if tied). Represents the part that can't be parallelized away. |
| `bottlenecks` | array of id | Nodes with >8 direct dependents, or any node whose removal would disconnect the graph. Honest accounting, not all hubs. |
| `honest_parallelism` | string | One line: did decomposition actually add parallelism vs a naive linear plan? `"4 nodes run in wave 0; critical path is 3 waves vs 7 linear."` or `"Linear chain — no real parallelism gained."`. Never claim parallelism that isn't there. |

## Validation rules

Run these checks before emitting, and again if a grader validates a plan:

1. **Unique ids** — no two nodes share an `id`.
2. **DAG** — `deps` form no cycle. Topological sort succeeds. If it fails, the decomposition is broken; rework before output.
3. **Dangling refs** — every id in every `deps` array exists in `nodes`.
4. **Input/dep alignment** — for each node, every dep has at least one matching `inputs` entry, and every `inputs` entry references a real dep. Mismatches signal hidden deps or fake deps.
5. **Output reachability** — every `outputs` entry of every node is either consumed by a downstream node's `inputs` or is a terminal output of the graph. Dead outputs (produced, never used, not terminal) suggest the node or the output is unnecessary.
6. **Self-contained, terse prompts** — no prompt contains "see above", "as discussed", "per the task", "previously", "you are a", "please", "your task is", or refers to the parent conversation. No preamble before the first imperative instruction. (Grader can grep for these phrases.)
7. **Verify objectivity** — every `verify` is a command, test, diff, or structural assertion. Reject "review", "looks good", "ensure quality".
8. **No dead nodes** — every node either has a downstream consumer or produces a terminal output. Cut the rest.
9. **Bottleneck honesty** — `summary.bottlenecks` lists every node with >8 direct dependents. Don't hide them.
10. **Model sanity** — `model`, where present (top-level or per-node), is a non-empty string. Unknown values are not an error — the executor maps them per harness.
11. **Skills sanity** — `skills`, where present (top-level or per-node), is an array of non-empty strings. Unknown skill names are not an error — the executor passes them as instructions and the subagent harness decides availability.

## Minimal valid example

```json
{
  "task": "Add a /health endpoint to the Express app",
  "granularity": "single-subagent-call",
  "model": "fast",
  "skills": ["ponytail"],
  "nodes": [
    {
      "id": "read-app",
      "name": "Read existing Express app entry",
      "prompt": "Read src/server.js (or src/app.js if present). Report: route-registration pattern, Express version, file path. Output the route-registration snippet verbatim.",
      "deps": [],
      "inputs": [],
      "outputs": ["app-entry-path", "route-registration-pattern"],
      "verify": "Output contains a file path that exists and a code snippet that matches `app.use` or `app.get`."
    },
    {
      "id": "add-route",
      "name": "Add GET /health route",
      "model": "strong",
      "skills": ["tdd"],
      "prompt": "In the Express app at <app-entry-path>, routes are registered like this:\n<route-registration-pattern>\n\nAdd `GET /health` returning `{ status: \"ok\" }`, 200, in the same style as existing routes. Don't touch other routes.",
      "deps": ["read-app"],
      "inputs": ["read-app:app-entry-path", "read-app:route-registration-pattern"],
      "outputs": ["health-route-diff"],
      "verify": "curl -s localhost:<port>/health returns {\"status\":\"ok\"} with 200; git diff shows only the new route."
    }
  ],
  "summary": {
    "node_count": 2,
    "wave_count": 2,
    "critical_path": ["read-app", "add-route"],
    "bottlenecks": [],
    "honest_parallelism": "Linear chain — no real parallelism gained. The task is too small to parallelize; decomposition is for clarity, not speed."
  }
}
```

Note the `honest_parallelism` — the skill admits this task didn't benefit from graphing. That honesty is the point.
