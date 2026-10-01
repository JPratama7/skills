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
4. **Checks** — where outputs allow it, write an executable check script to
   `<scratch>/<skill>-verifier/eval-<id>/checks.py`; otherwise a structured
   checklist. Layer the checks:
   existence → format parses → structure/schema → stated constraints →
   derived correctness (recompute from inputs) → completeness →
   anti-fabrication (output traces to real input, not invented).
   One check per item or small group, so partial correctness produces a
   partial score. Put a requirement→check mapping comment at the top.
5. **Run** — execute, fix errors until the suite runs clean.
6. **Reflect** — re-read the prompt end to end. Any requirement with no
   check? Add it. Any assertion that would pass for clearly wrong output?
   Note it in `eval_feedback` — that's a non-discriminating assertion.
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

- `<run_dir>/grading.json` — standard schema (`expectations[]` with
  `text`/`passed`/`evidence` + `summary`). Checks the verifier derived beyond
  the assertion list go in as extra expectations, text prefixed `verifier:`.
- `<run_dir>/diagnosis.md` — only when something failed.
- `eval_feedback` field in grading.json — critique of weak or missing
  assertions.

## Co-evolving checks

Persist verifier checks across iterations at `<scratch>/<skill>-verifier/`:

```
.<skill>-verifier/
├── eval-<id>/checks.py    # refined each iteration, not regenerated
└── notes.md               # known blind spots of the checks
```

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

Prior checks to refine (do not restart from scratch): <verifier dir>/eval-<id>/checks.py
or: none — write them fresh.

Workflow: enumerate every requirement → inspect inputs and derive expected
properties → inspect outputs → write/run checks under <verifier dir>/eval-<id>/
→ reflect that each requirement has a check → for each failure write a
diagnosis block (Actual / Expected / Root cause / Fix suggestion).

Write:
- <run_dir>/grading.json  (expectations[{text,passed,evidence}] + summary;
  your own derived checks as expectations prefixed "verifier:")
- <run_dir>/diagnosis.md  (only if failures)
- updated checks at <verifier dir>/eval-<id>/checks.py
```
