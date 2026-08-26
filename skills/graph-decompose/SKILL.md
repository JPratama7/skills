---
name: graph-decompose
version: 3.0.0
description: Decompose a task into a strict DAG of atomic, parallel-executable graph nodes, each one a self-contained subagent prompt. Emit the plan as JSON + Mermaid. Plan only — never executes the graph itself. Trigger ONLY on explicit invoke — the user says "graph-decompose", "/graph-decompose", "decompose this into parallel tasks", "break this into a task graph", "split this into atomic nodes", or "split this into a DAG". Do not auto-trigger on ordinary multi-step work; the user must ask for graph decomposition specifically. To run a produced plan, use the `graph-execute` skill.
---

# Graph Decompose

## Prime directive

Turn one task into a strict DAG of atomic nodes. Each node is a single self-contained prompt that one subagent can execute end-to-end with no further decomposition. Output the plan as JSON (machine-readable) plus Mermaid (visual). Do not execute the plan — that is the `graph-execute` skill's job. After emitting, point the user at `graph-execute` if they want it run.

The value is parallelism: independent nodes run at the same time. A good decomposition maximizes ready-at-time-zero nodes and keeps the critical path short. A bad decomposition is a linear chain that pretended to be a graph.

## When to use

Explicit invoke only. The user must say something like:

- `graph-decompose <task>` / `/graph-decompose`
- "decompose this into parallel tasks"
- "break this into a task graph"
- "split this into atomic nodes"
- "turn this task into a DAG"

If the user just describes a multi-step task without asking for decomposition, do not run this skill — handle the task normally. Overtriggering here produces graphs for work that didn't need them.

## Inputs

Collect before decomposing:

1. **The task** — one sentence of what should be true when done. If the user's framing is fuzzy, sharpen it first: "In one sentence, what's done when this is done?"
2. **Context** — files, repo, prior decisions, constraints. Ask for what you need; don't invent context.
3. **Granularity target** (optional) — default is "one subagent call per node". The user may want coarser (one logical step) or finer (one file edit). Honor it if stated; otherwise use the default.
4. **Model config** (optional) — if the user wants specific nodes run on specific models, capture it in their words: "use a fast model for the extraction nodes, the strong one for codegen". Emit their request verbatim as `model` fields. If the user never mentions models, leave `model` out of the plan entirely — the executor uses its harness default.
5. **Skill config** (optional) — if the user wants nodes to run with specific skills preloaded, capture it: "use the tdd skill for the test node, ponytail for the refactor node". Emit their requests verbatim as `skills` arrays. If the user never mentions skills, leave `skills` out of the plan entirely — the executor runs nodes without skill instructions.

If any input is missing and material, ask for it. One round of questions max before decomposing — better to decompose on partial info and let the user correct than to interview exhaustively.

## Decomposition method

Work through these stages in order. Do not skip ahead to emitting JSON.

### 1. Enumerate subtasks

List every distinct piece of work the task implies. Brainstorm wide first; correctness comes from not missing pieces, not from premature tidiness.

### 2. Make each node atomic

Apply the **atomicity test** to every candidate node:

> A single subagent, given only this node's prompt and the declared inputs from its dependencies, can complete it end-to-end without further decomposition and without reading your conversation history.

If the answer is no, the node is too coarse — split it. Common split signals:

- The prompt contains "and then" or "next" — that's two nodes.
- The prompt needs context you'd have to inline from the parent task — fold that context into the node prompt as a self-contained block, or add a dep that produces it.
- The node touches two unrelated files/concepts with no shared reason to be coupled — split by concern.
- The node has a verify step that's substantial — split into a do-node and a verify-node with a dep edge.

Conversely, collapse nodes that are too fine:

- A node whose entire output is one line that another node immediately consumes — fold it into the consumer unless it's reused by ≥2 nodes (then it's a shared dep, keep it).
- Two nodes that always run sequentially with no branching and no shared consumer — merge into one.

### 3. Build the strict DAG

For each node, list the ids of nodes whose outputs it consumes. Rules:

- **Strict DAG only.** No cycles. If you find a cycle, the decomposition is wrong — rework it, don't paper over it.
- **Edges mean data dependency, not ordering preference.** Add an edge only when node B literally cannot start without node A's output. "It would be nice to do A first" is not a dependency.
- **Empty `deps` = ready at time zero.** Maximize these. If every node depends on the previous one, you've written a list, not a graph — reconsider whether the deps are real or just sequencing bias.
- **No hidden deps.** If a node reads a file another node writes, that's a dep. If a node assumes a decision another node makes, that's a dep. Hidden deps cause parallel races; surface them all.
- **Fan-out warning.** If a single node has >8 direct dependents, flag it as a bottleneck in the plan summary. Don't refuse, but make the bottleneck visible.

### 4. Verify the graph

Before emitting, self-check:

- Walk every node: does its prompt + declared inputs pass the atomicity test? If not, fix.
- Topologically sort mentally: what runs at wave 0, wave 1, ...? Is the critical path shorter than a naive linear plan? If not, the decomposition added no parallelism — say so honestly in the plan summary rather than pretending.
- Are there nodes with no downstream consumers and no terminal output? They're dead — cut them.
- Any cycle? Rework.

## Output format

Do not hand-write JSON. Use the bundled script `scripts/graph.py` — it backs the plan with a SQLite DB, validates each node as you add it, computes the `summary` (wave count, critical path, bottlenecks) deterministically, and emits both JSON and Mermaid in one call. This avoids JSON quoting/escaping errors on multi-line prompts and catches duplicate ids, dangling deps, and cycles at insert time rather than after a giant emit.

### Workflow

```bash
# 1. set plan metadata (task required; model/skills only if the user named them)
python scripts/graph.py init --task "<one-sentence done-when-true>" \
  [--granularity single-subagent-call] [--model fast] [--skills ponytail,tdd]

# 2. add nodes one at a time, in dependency order (deps must already exist)
python scripts/graph.py add-node --id read-spec --name "Extract schema" \
  --prompt "<terse self-contained prompt>" \
  --verify "<objective check: command, test, or diff>" \
  --outputs extracted.md \
  [--deps read-spec] [--inputs read-spec:extracted.md] \
  [--model strong] [--skills tdd]

# 3. validate the whole plan (cycle, dangling refs, input/dep alignment, dead outputs, prompt style, verify objectivity)
python scripts/graph.py validate

# 4. export — refuses to write if validation fails; computes summary from the graph
python scripts/graph.py export --json plan.json [--mermaid plan.mmd]
```

The DB defaults to `./plan.db` (override with `--db`). It is scratch state — the exported `plan.json` + `plan.mmd` are the deliverables; the DB can be deleted after export.

### Field rules (enforced by the script)

- `id` — short, stable, kebab/snake-safe (`n1`, `read-spec`). Unique; `add-node` rejects duplicates.
- `model` — optional, free-form (id like `claude-sonnet-4-5` or tier like `fast`/`cheap`/`strong`). Echo the user's words verbatim. Precedence: node > top-level > harness default. Omit entirely if the user never mentioned models.
- `skills` — optional, comma-separated skill names. Echo verbatim. Precedence: node > top-level > no skill instructions. Omit entirely if the user never mentioned skills.
- `prompt` — **self-contained and terse**. No "see above", no "as discussed", no "you are a helpful assistant", no restating the task. Imperative voice, one instruction per line, inline only the context slice the subagent needs. A fresh subagent with only this string + `inputs` must be able to execute it. 3 lines beats 10. `validate` greps for banned phrases (`see above`, `as discussed`, `per the task`, `previously`, `you are a`, `please`, `your task is`).
- `deps` — ids only. Empty = ready at wave 0. `add-node` rejects deps that don't exist yet (add deps before dependents).
- `inputs` — `dep_id:artifact` per dep. Must line up with `deps`. Catches hidden deps: a node that needs a file but lists no input for it is suspect.
- `outputs` — concrete artifact names downstream nodes reference (`types.ts`, `decision: use-postgres`, `test-results.json`). Not vague.
- `verify` — objective check: a command, test, diff, or structural assertion. `validate` rejects `review`, `looks good`, `ensure quality`, `looks reasonable`.

Full schema with field-level constraints and all validation rules: `references/schema.md`.

### Mermaid

`export` writes the Mermaid alongside the JSON automatically. It uses `graph LR`, labels each node with `id` and short name, draws every dep edge, and styles wave-0 (ready-now) nodes with a `ready` class so parallelism is visible at a glance. You do not write Mermaid by hand.

## After exporting

Tell the user the path of the exported `plan.json` (and `plan.mmd`). Then point at the next step:

> Plan written to `plan.json` (+ `plan.mmd`). To execute it, invoke `graph-execute` and pass it the JSON path. To revise, edit nodes in the DB and re-export, or hand-edit the JSON.

Do not execute the plan. Do not spawn subagents. Do not run nodes. This skill's output is the plan files and nothing more.

## Hard rules

- Never hand-write the plan JSON. Always use `scripts/graph.py` (`init` → `add-node` per node → `validate` → `export`). The script enforces the schema and computes the summary; writing JSON by hand defeats the point.
- Always run `validate` before `export`. `export` refuses to write on validation failure, but running `validate` first gives you the violation list to fix.
- Never execute the plan, never spawn subagents, never run nodes. Plan only.
- Never invent deps to force sequencing, and never omit real deps to fake parallelism. The graph must reflect actual data flow.
- Every node prompt is self-contained — no implicit context from the parent conversation.
- If decomposition produced no real parallelism (a linear chain), the script's `honest_parallelism` will say so. Don't override it to pretend. A skill that fakes parallelism is worse than no skill.
- Cycles are impossible by construction (`add-node` rejects deps that don't exist yet), but `validate` checks as a safety net. If you somehow create one, rework the decomposition.
- One round of input questions max before decomposing. Iteration happens via the user editing the DB and re-exporting, not via longer upfront interview.
- Never invent `model` or `skills` assignments the user didn't request. No mention → no field.

## Anti-patterns

- **List-as-graph**: every node depends on the previous one. Not a graph. Reconsider deps or admit linear.
- **Coarse node**: prompt says "and then" or needs inline parent context. Split.
- **Fine node**: one-line output consumed by exactly one other node. Fold.
- **Hidden dep**: node reads a file another node writes but doesn't declare it. Surface it.
- **Vague verify**: "looks reasonable". Replace with a command, test, or structural check.
- **Bottleneck pretending to be parallel**: one node feeds 12 others and calls it parallelism. Flag the bottleneck honestly.
- **Self-referential prompt**: "as discussed above", "per the task". Inline the context.
- **Verbose prompt**: preamble ("you are a..."), restated task, pleasantries, meta-commentary. Strip to imperative instructions + inline context only.

## Reference files (load on demand)

- Need the full JSON schema with field constraints and validation rules → `references/schema.md`
- Want worked examples of good vs bad decompositions (shown as `graph.py` calls + the resulting exported JSON) → `references/examples.md`

The plan JSON exported by `scripts/graph.py` is the input contract for `graph-execute`. Its schema is `references/schema.md` here; the executor consumes it as-is.
