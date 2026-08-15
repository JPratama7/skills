# Execution — per-harness mechanics

How to walk the DAG on each harness. The wave-based algorithm is the same everywhere; only the "spawn parallel subagents" primitive differs.

## Generic algorithm

```
done = {}        # id -> outputs
failed = None
while len(done) < len(nodes):
    ready = [n for n in nodes if n.id not in done
             and all(d in done for d in n.deps)]
    if not ready:
        if failed: surface failure, ask user
        else: break  # shouldn't happen on a valid DAG
    results = spawn_all_parallel(ready)   # harness-specific
    for id, result in results:
        if verify(result, node[id]):
            done[id] = result.outputs
        else:
            failed = (id, result)
            break  # stop the wave; don't push bad outputs downstream
present_final(done, terminal_nodes)
```

Key invariants:

- **Never start a node whose deps aren't all `done`.** A dep that's still running is not done.
- **Verify before marking done.** A node that produced output but failed `verify` is not done — it's failed.
- **Stop the wave on failure.** Don't fan out a bad output to its dependents. Surface the failure with the node's prompt + output and ask the user: retry / edit prompt / rework graph.
- **Capture outputs by name.** Downstream nodes reference deps by `inputs` (`dep_id:artifact_name`); the executor must be able to hand a downstream subagent the named artifact from each dep.

## Model & skill dispatch

Plans may carry optional `model` and `skills` values (per-node or top-level default from `graph-decompose`). Resolve before spawn:

- Model: `node.model` → `plan.model` → harness default.
- Skills: `node.skills` → `plan.skills` → no skill instructions. Override replaces, never merges — a node with its own `skills` list gets exactly that list.

### Model — honor what the harness allows

| Harness | Model support |
|---|---|
| Headless shell | Full — worker passes `--model <model>` to the agent CLI (e.g., `claude -p --model <model> < prompt`). |
| Devin | None — `run_subagent` has no model parameter. Use the resolved `model` as a hint for profile choice when ambiguous, but do not claim the node ran on that model. |
| Claude Code | `Task` has no model parameter in the standard form. If the harness exposes one, pass it; otherwise treat like Devin. |
| Cowork / other | Whatever the spawn primitive exposes. If it takes a model param, pass the resolved value; if not, treat like Devin. |

When a node's resolved `model` can't be honored, don't silently proceed: mention it once per wave ("nodes n2, n3 requested `strong`; this harness can't select models, running on default") so the user can decide whether the mapping matters. The plan file is never edited for this — the model request stays in the plan.

### Skills — task-text instruction, every harness

No spawn primitive (Devin `run_subagent`, Claude Code `Task`, headless worker) takes a native skill parameter. Every harness passes skills the same way: prepend to the spawned subagent's task text.

```
Invoke these skills before starting: tdd, ponytail

<node prompt + inline inputs>
```

The instruction is a request, not a guarantee — the subagent honors it if its harness has the skill installed. Do not claim the skill ran; just ensure the instruction was given. Skills are not merged: a node with `"skills": ["tdd"]` under a plan with `"skills": ["ponytail"]` gets `tdd` only.

## Harness: Devin

Use `run_subagent` with `is_background=true` for every ready node in the same turn (parallel launch). Then `read_subagent` with `block=true` to wait for each.

- Pass each subagent the node's `prompt` plus the named artifacts from its `inputs` (read those files / paste those snippets into the prompt body).
- Subagent profile: `subagent_general` for nodes that edit code or run commands; `subagent_explore` for read-only research nodes. Match profile to the node's work.
- When a subagent completes, run its `verify` inline (exec a command, read a file, diff). On pass, record outputs. On fail, stop and surface.
- Recompute ready set, launch the next wave.

Do not launch one foreground subagent at a time — that serializes the graph and defeats the purpose. Background + parallel is the whole point.

## Harness: Claude Code

Use the `Task` tool (or `!` subagent dispatch) to spawn parallel subagents. Same wave algorithm.

- One `Task` call per ready node, all in the same assistant turn.
- Each `Task` gets the node's self-contained `prompt` + the named inputs from completed deps.
- Wait for all `Task`s in the wave to return before starting the next wave — dependents need their deps' outputs.
- Run `verify` inline after each returns.

## Harness: headless shell (no subagents)

If the harness has no subagent primitive, the graph can still execute, just without true parallelism inside one process:

- For each ready node, write its `prompt` to a file (`nodes/<id>.prompt.md`).
- Spawn one worker process per node: `python worker.py nodes/<id>.prompt.md > nodes/<id>.out &` for all ready, then `wait`.
- Worker is harness-specific — the skill does not bundle it, but the convention is: worker reads the prompt file, calls the agent CLI (e.g., `claude -p < prompt`), writes stdout to the `.out` file.
- Model: when the node's resolved `model` is set, the worker passes it to the CLI — `claude -p --model <model> < prompt`. This is the only harness where model selection is fully under executor control.
- After `wait` returns, run each node's `verify` (grep a file, run a test, diff). Record outputs. Next wave.

This trades the harness's in-process subagent support for OS-level `&` + `wait`. Slower to set up, works anywhere with a shell.

## Harness: Cowork / other

If the harness exposes a parallel-dispatch primitive, use it the same way: launch all ready nodes in one turn, wait for the wave, verify, repeat. If it doesn't, fall back to headless-shell above.

## Failure handling

A failed `verify` is not a crash — it's information. When a node fails:

1. Stop the current wave. Do not start its dependents.
2. Show the user: the node's `id`, `prompt`, the actual output, and the `verify` check that failed.
3. Offer three paths:
   - **Retry** — re-run the same node (transient failure, e.g., flaky test).
   - **Edit prompt** — fix the prompt and re-run just this node.
   - **Rework graph** — the node is wrong, not the execution. Edit the graph (split, merge, add deps) and re-plan from there.
4. Do not auto-retry more than once without user input. Silent retry loops hide real bugs.

## What execution is NOT

- Not "run all nodes at once ignoring deps". The DAG exists for a reason.
- Not "run nodes in id order". Id order is arbitrary; only dep order matters.
- Not "skip verify if the output looks plausible". Verify is the contract between nodes; skip it and hidden failures fan out.
