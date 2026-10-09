# Independent Verification

Adapted from CoEvoSkills (Zhang et al., COLM 2026): grading is done by a fresh
agent that never sees the skill, the expected output, or the conversation that
produced the run. Independence is the point — a grader that wrote the skill
tends to pass its own blind spots.

## When to verify

Spawn one verifier per run after `outputs/` exists. For subjective evals where
executable checks don't apply, use the grader/comparator roles in
`agent-roles.md` or human review instead.

## Information boundary

Give the verifier **only**:

- The eval prompt, verbatim
- Input file paths (the eval's `files`)
- The run's `outputs/` dir
- The assertion list (the minimum contract — it may check more)

Never give it, and forbid it from reading if it finds them:

- The skill directory or anything in it
- `expected_output` — that is the protected-answer analog
- The run transcript, this conversation, prior grading verdicts

It judges the output, not the implementation. Evidence derived from the skill's
own claims ("the script validates X") is confirmation bias, not verification.

## Verifier workflow

Encode this in the subagent prompt (template below).

1. **Requirements** — before opening outputs, write a numbered R1..Rn list of
   every verifiable requirement in the prompt and assertion list. Be
   exhaustive: if the prompt says it, it gets a number.
2. **Inputs** — inspect input files. Derive checkable properties
   independently: entity names/IDs, counts, value ranges, formats,
   invariants. These are the sources of truth for expected values.
3. **Outputs** — read the produced artifacts.
4. **Audit checks** — first run the eval's deterministic assertion suite
   unchanged and preserve its results as the canonical machine score. Then
   derive additional checks independently and write them to
   `<scratch>/<skill>-verifier/eval-<id>/<config>/checks.py` (one directory
   per run configuration — never share a checks file across arms). Where
   assertions are executable, reuse the deterministic checker rather than
   reimplementing it; add new checks only for uncovered requirements. Layer
   checks: existence → parse → schema → stated constraints → recompute from
   inputs → completeness → anti-fabrication. Map each requirement to a check.
5. **Run** — execute the checks read-only. Never alter outputs. Report
   deterministic suite results separately from verifier-added audit findings.
6. **Reflect** — re-read the prompt. Identify uncovered requirements and
   assertions that accept clearly wrong outputs. Recommend contract changes
   for future eval runs; do not change the current machine score retroactively.
7. **Diagnose** — for each failed check, a 3–5 line block:

   ```markdown
   ## <check name>
   - **Actual**: what the output contains (quote the value)
   - **Expected**: correct value, derived from inputs — not from the assertion text
   - **Root cause**: why it's wrong
   - **Fix suggestion**: one concrete action
   ```

   Write these to `<run_dir>/diagnosis.md`. This file is the feedback channel
   the improve step consumes — specific beats vague.

Fail closed: if a check can't be performed read-only, fail it with the reason
stated. Never modify outputs to make verification easier.

## Outputs

- `<run_dir>/verifier_audit.json` for objective evals — findings the verifier
  derived beyond the deterministic suite, clearly labeled as audit checks.
  Do not overwrite or revise deterministic `<run_dir>/grading.json`.
- `<run_dir>/grading.json` for subjective-only evals — standard schema
  (`expectations[]` with `text`/`passed`/`evidence` + `summary`), with each
  judgment criterion identified as subjective.
- `<run_dir>/diagnosis.md` — only when something failed.
- `eval_feedback` in the audit or subjective grading — critique weak or missing
  assertions for a future iteration; do not back-edit this run's score.

## Co-evolving checks

Persist verifier checks across iterations at `<scratch>/<skill>-verifier/`:

```
.<skill>-verifier/
├── eval-<id>/<config>/checks.py  # per run configuration, refined each iteration
└── notes.md               # known blind spots of the checks
```

The two arms of one eval (e.g. with_skill / old_skill) keep separate
checks: a shared path races, and the second verifier inherits checks
calibrated for the wrong arm's expected behavior.

- Iteration 1: verifier writes checks from scratch.
- Iteration N+1: it loads the persisted checks and revises where the task
  changed or a prior verdict was wrong — never regenerates blindly.
- When user feedback or a canonical check contradicts a verifier verdict (a
  "pass" that's actually wrong, or vice versa), treat it as a verifier bug:
  update the checks so they would have caught it. The checks co-evolve with
  the skill — this is what stops the loop from quietly accepting
  reward-hacked outputs.

## Subagent prompt template

```
You are an independent verifier. Grade only the output artifacts. Do not open
or read the skill that produced them, any expected_output description, or any
prior grading — those are off-limits and would bias your verdict.

Task prompt (verbatim):
<prompt>

Input files: <paths>
Outputs to verify: <run_dir>/outputs/
Assertion contract (minimum — derive additional checks yourself):
<assertions>

Prior checks to refine (do not restart from scratch): <verifier dir>/eval-<id>/<config>/checks.py
(<config> = this run's configuration: with_skill / without_skill / old_skill)
or: none — write them fresh.

Workflow: enumerate every requirement → inspect inputs and derive expected
properties → inspect outputs → write/run checks under <verifier dir>/eval-<id>/<config>/
→ reflect that each requirement has a check → for each failure write a
diagnosis block (Actual / Expected / Root cause / Fix suggestion).

Write:
- objective eval: <run_dir>/verifier_audit.json (your derived audit findings;
  never overwrite deterministic grading.json)
- subjective-only eval: <run_dir>/grading.json (expectations[{text,passed,evidence}]
  + summary; identify judgment criteria as subjective)
- <run_dir>/diagnosis.md (only if failures)
- updated checks at <verifier dir>/eval-<id>/<config>/checks.py
```
