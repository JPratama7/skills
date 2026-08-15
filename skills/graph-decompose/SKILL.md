---
name: graph-decompose
version: 2.2.0
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

Always emit both. JSON first (execution), Mermaid second (review).

### JSON

```json
{
  "task": "<one-sentence task statement>",
  "granularity": "single-subagent-call",
  "model": "<optional default model for nodes that don't specify one>",
  "skills": ["<optional default skills for nodes that don't specify any>"],
  "nodes": [
    {
      "id": "n1",
      "name": "<short human-readable name>",
      "model": "<optional; overrides top-level model for this node>",
      "skills": ["<optional; overrides top-level skills for this node>"],
      "prompt": "<self-contained prompt a subagent can execute with only this + inputs>",
      "deps": [],
      "inputs": [],
      "outputs": ["<what this node produces, in a form downstream nodes can reference>"],
      "verify": "<how to check this node is actually done and correct>"
    }
  ],
  "summary": {
    "node_count": 0,
    "wave_count": 0,
    "critical_path": ["n1", "n2"],
    "bottlenecks": [],
    "honest_parallelism": "<one line: did decomposition actually add parallelism vs a linear plan?>"
  }
}
```

Field rules:

- `id` — short, stable, kebab/snake-safe (`n1`, `n2`, ... or `read-spec`, `gen-types`).
- `model` — optional, free-form string (model id like `claude-sonnet-4-5`, or a tier like `fast`/`cheap`/`strong`). Echo the user's words verbatim — don't normalize, don't guess. Precedence at execution: node `model` > top-level `model` > harness default. Omit entirely if the user never mentioned models.
- `skills` — optional, array of skill names (e.g., `tdd`, `ponytail`). Echo the user's words verbatim. Precedence at execution: node `skills` > top-level `skills` > no skill instructions. Omit entirely if the user never mentioned skills.
- `prompt` — **self-contained**. No "see above", no "as discussed". A subagent that has never seen this conversation should be able to execute it. Include the relevant slice of context inline.
- `deps` — ids only. Empty array if ready at time zero.
- `inputs` — for each dep the node consumes, name what artifact it pulls from that dep. Empty if no deps. This makes the data flow auditable and catches hidden deps (a node that needs a file but lists no input for it is suspect).
- `outputs` — concrete artifacts (files, snippets, decisions, structured data). Downstream nodes reference these by name.
- `verify` — an objective check, not "looks good". Prefer a command, a test, a diff, or a structural assertion.

Full schema with field-level constraints: `references/schema.md`.

### Mermaid

```mermaid
graph LR
  n1["read spec"]
  n2["gen types"] --> depends on
  n3["gen client"]
  n1 --> n2
  n1 --> n3
  n2 --> n4["merge + test"]
  n3 --> n4
```

Use `graph LR`. Label each node with its `id` and short name. Draw every dep edge. Style wave-0 (ready-now) nodes with a distinct class so the user can see parallelism at a glance:

```mermaid
classDef ready fill:#cfe,stroke:#080;
class n1,n3 ready;
```

## After emitting

Save the plan to a file (e.g., `plan.json` with the Mermaid block adjacent or in a sibling `plan.mmd`). Tell the user the path. Then point at the next step:

> Plan written to `<path>`. To execute it, invoke `graph-execute` and pass it this path. To revise, edit the plan and re-decompose or hand-edit.

Do not execute the plan. Do not spawn subagents. Do not run nodes. This skill's output is the plan and nothing more.

## Hard rules

- Always emit both JSON and Mermaid. Always.
- Never execute the plan, never spawn subagents, never run nodes. Plan only.
- Never invent deps to force sequencing, and never omit real deps to fake parallelism. The graph must reflect actual data flow.
- Every node prompt is self-contained — no implicit context from the parent conversation.
- If decomposition produced no real parallelism (a linear chain), say so in `summary.honest_parallelism`. A skill that pretends to parallelize but doesn't is worse than no skill.
- If you hit a cycle, rework the decomposition. Don't ship a cyclic "DAG".
- One round of input questions max before decomposing. Iteration happens via the user editing the emitted plan, not via longer upfront interview.
- Never invent `model` or `skills` assignments the user didn't request. No mention → no field.

## Anti-patterns

- **List-as-graph**: every node depends on the previous one. Not a graph. Reconsider deps or admit linear.
- **Coarse node**: prompt says "and then" or needs inline parent context. Split.
- **Fine node**: one-line output consumed by exactly one other node. Fold.
- **Hidden dep**: node reads a file another node writes but doesn't declare it. Surface it.
- **Vague verify**: "looks reasonable". Replace with a command, test, or structural check.
- **Bottleneck pretending to be parallel**: one node feeds 12 others and calls it parallelism. Flag the bottleneck honestly.
- **Self-referential prompt**: "as discussed above", "per the task". Inline the context.

## Reference files (load on demand)

- Need the full JSON schema with field constraints and validation rules → `references/schema.md`
- Want worked examples of good vs bad decompositions → `references/examples.md`

The plan JSON this skill emits is the input contract for `graph-execute`. Its schema is `references/schema.md` here; the executor consumes it as-is.
