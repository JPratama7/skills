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
