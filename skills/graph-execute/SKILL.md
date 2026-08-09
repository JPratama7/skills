---
name: graph-execute
version: 1.0.0
description: Execute a graph-decompose plan by walking its DAG in waves — running ready nodes in parallel, respecting deps, verifying each node before fanning out, stopping on failure. Trigger ONLY when the user explicitly asks to run/execute a plan AND points at where the planner output is. Trigger phrases include "graph-execute", "/graph-execute", "execute this graph", "run this task graph", "walk the DAG", "execute the plan at PATH". Do not trigger on decomposition requests (that is `graph-decompose`) or on ordinary multi-step work. Requires the user to name the planner output location before proceeding.
compatibility: Requires subagent dispatch (e.g., Devin `run_subagent`, Claude Code `Task`) OR a headless shell with `&` + `wait`. Filesystem read access to the plan path and to node output files.
---

# Graph Execute

## Prime directive

Take a plan produced by `graph-decompose` and execute it: walk the strict DAG in waves, spawn all ready nodes in parallel each wave, verify each before fanning out, stop on failure and ask the user. Never execute without the user pointing at the plan's location first.

## When to use

Explicit invoke only, AND the user must state where the planner output lives. Acceptable forms:

- `graph-execute <path>` / `/graph-execute <path>`
- "execute the graph at `plan.json`"
- "run the task graph from `.local/foo/plan.md`"
- "walk the DAG in `out/plan.json`"

If the user invokes the skill but does not name a path, ask exactly once: "Where is the graph-decompose plan? Give me the file path." Do not guess, do not search the workspace for likely plans, do not proceed without an explicit answer. The path is the contract that the user has reviewed the plan and wants it run.

If the user asks to decompose a task (no plan exists yet), do not run this skill — redirect to `graph-decompose`.

## Inputs

Before doing anything else:

1. **Plan path** — required. If not stated in the invoke, ask once and stop.
2. **Read the plan file.** Parse the JSON block. If the file has both JSON and Mermaid (typical `graph-decompose` output), extract the JSON block from the ```json fence. If parsing fails, surface the error verbatim and stop — do not attempt to repair the plan.
3. **Validate the plan** against the schema before execution. The schema lives in `graph-decompose`'s `references/schema.md` — read it if you haven't. Run the validation rules: unique ids, DAG (no cycle), no dangling dep refs, input/dep alignment, no dead nodes. If any check fails, surface it and stop. Do not execute an invalid plan — re-decompose or hand-edit instead.

If the plan is valid, show the user a one-line execution summary: node count, wave count, critical path, bottlenecks. Then ask: "Proceed? (yes / no)". Do not start wave 0 without an explicit yes.

## Execution algorithm

Walk the DAG in waves. The algorithm is the same on every harness; the spawn primitive differs (see `references/execution.md`).

```
done = {}            # id -> captured outputs (by artifact name)
failed = None
while len(done) < len(nodes):
    ready = [n for n in nodes
             if n.id not in done
             and all(d in done for d in n.deps)]
    if not ready:
        if failed: surface(failed); ask user
        else: break  # shouldn't happen on a validated DAG
    # Spawn all ready nodes in parallel — this is the whole point.
    results = spawn_all_parallel(ready)
    for id, result in results:
        if verify(result, node[id]):
            done[id] = result.outputs
        else:
            failed = (id, result)
            break  # stop the wave; do not fan out bad outputs
present_final(done, terminal_nodes)
```

Invariants — never violate these:

- **Never start a node whose deps aren't all `done`.** A dep that's still running is not done. A dep that ran but failed verify is not done.
- **Verify before marking `done`.** A node that produced output but failed `verify` is `failed`, not `done`. Do not push its outputs downstream.
- **Stop the wave on failure.** Do not fan out a bad output to its dependents. Surface the failure with the node's prompt + output, ask the user (retry / edit prompt / rework graph).
- **Spawn all ready nodes in one turn.** Serializing the wave defeats the purpose. Parallel is the entire reason the plan exists.
- **Capture outputs by name.** Downstream node prompts reference deps by `inputs` (`dep_id:artifact_name`). When spawning a dependent, read the named artifact from each completed dep and inline it into the dependent's prompt (or pass the file path if the artifact is a file the subagent can read).

## Per-harness mechanics

The spawn primitive differs by harness. Read `references/execution.md` before executing on a harness you haven't handled — it covers Devin `run_subagent`, Claude Code `Task`, headless shell (`&` + `wait`), and others.

Quick reference:

- **Devin**: `run_subagent` with `is_background=true` for every ready node in the same turn; `read_subagent` with `block=true` to wait. Profile `subagent_general` for code-editing nodes, `subagent_explore` for read-only research nodes.
- **Claude Code**: one `Task` call per ready node, all in the same assistant turn. Wait for the wave to return before starting the next.
- **Headless shell**: write each node's prompt to `nodes/<id>.prompt.md`, spawn `worker.py nodes/<id>.prompt.md > nodes/<id>.out &` for all ready, `wait`, then verify each. Slower to set up, works anywhere with a shell.

## Failure handling

A failed `verify` is information, not a crash. When a node fails:

1. Stop the current wave. Do not start its dependents.
2. Show the user: the node's `id`, its `prompt`, the actual output, and the `verify` check that failed (with the failing command/assertion's output).
3. Offer three paths:
   - **Retry** — re-run the same node (transient failure, e.g., flaky test). One auto-retry max without user input.
   - **Edit prompt** — fix the prompt and re-run just this node. Outputs of completed deps stay cached.
   - **Rework graph** — the node is wrong, not the execution. Stop execution; tell the user to edit the plan (or re-decompose) and re-invoke `graph-execute` on the new plan.
4. Do not silently retry more than once. Hidden retry loops mask real bugs.

## Completion

When all terminal nodes (those with no downstream consumers) are `done`:

1. Present the terminal outputs against the plan's one-sentence `task` from the JSON.
2. Report per-node status: passed, failed, retried. Surface any retries honestly.
3. Do not claim success if any node failed and the user chose to skip it without a rework — say "completed with skipped node `<id>`" and explain what's missing.

## Hard rules

- Never execute without an explicit user yes, AND never execute without the user naming the plan path first.
- Never execute an invalid plan. Validate first; surface failures; stop.
- Never start a node whose deps aren't all `done` and verified.
- Never skip `verify`. Verify is the contract between nodes.
- Never serialize a wave. Spawn all ready nodes in parallel.
- Never silently retry a failed node more than once.
- Never fan out a failed node's outputs to its dependents.
- Never mutate the plan file during execution. If the user wants to rework, stop and re-invoke on a new plan.

## Anti-patterns

- **No-path invoke**: user says "execute the graph" without saying where it is, and you guess. Ask once instead.
- **Skip-validate**: jumping to wave 0 without checking the plan is a valid DAG. Cycle or dangling dep → confusing mid-wave crash. Validate first.
- **Serial wave**: spawning one node at a time "to be safe". Defeats the plan. Parallel or nothing.
- **Verify-skipping**: marking `done` because the node produced *something*. Run the declared check.
- **Silent retry loop**: node fails → you retry → fails → you retry → ... Stop after one auto-retry and ask the user.
- **Bad-output fan-out**: node fails verify but you feed its output to dependents anyway "to keep moving". Stop the wave.
- **Plan mutation**: editing `plan.json` mid-execution to "fix" a failing node. Stop, rework, re-invoke on the new plan.

## Reference files (load on demand)

- About to spawn nodes on a specific harness → `references/execution.md`
- Need to validate the input plan's schema → `../graph-decompose/references/schema.md` (the plan JSON is the contract this skill consumes)

## What this skill is NOT

- Not a decomposer. If there is no plan yet, redirect to `graph-decompose`. This skill runs plans, it does not write them.
- Not a "run arbitrary commands in parallel" tool. It walks a specific DAG with verified deps. Use a shell for unrelated parallel commands.
- Not a workflow engine. No durability, no resume-after-crash, no retries-across-sessions. If you need that, use Temporal / Inngest / BullMQ — the plan format is portable to those.
