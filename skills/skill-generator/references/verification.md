# Verification

Grading by a fresh agent that never saw the skill, expected output, or the producing conversation (CoEvoSkills, Zhang et al., COLM 2026) — a grader that wrote the skill passes its own blind spots.

One verifier per run, after `outputs/` exists. Subjective evals with no executable checks: grader/comparator roles in `agent-roles.md` or human review.

## Boundary

Give **only**: eval prompt (verbatim), input paths (`files`), the run's `outputs/` dir, assertion list (minimum contract).

Never give — nor allow reading: skill directory, `expected_output` (protected-answer analog), run transcript, this conversation, prior verdicts. Judges output, not implementation; skill's self-claims ("the script validates X") are confirmation bias, not verification.

## Workflow

Encode in the subagent prompt (template below).

1. **Requirements** — before opening outputs, numbered R1..Rn of every verifiable requirement in prompt + assertions. Prompt says it → gets a number.
2. **Inputs** — inspect files; independently derive checkable properties: entity names/IDs, counts, ranges, formats, invariants. Sources of truth for expected values.
3. **Outputs** — read the artifacts.
4. **Audit checks** — run the deterministic assertion suite unchanged first; keep its results as the canonical machine score. Derive extra checks to `<scratch>/<skill>-verifier/eval-<id>/<config>/checks.py` (one dir per config — never share a checks file across arms). Executable assertions → reuse the deterministic checker; add checks only for uncovered requirements. Layer: existence → parse → schema → stated constraints → recompute from inputs → completeness → anti-fabrication. Map every requirement to a check.
5. **Run** — read-only; never alter outputs. Report deterministic results separately from verifier-added audit findings.
6. **Reflect** — re-read prompt; find uncovered requirements and assertions that accept clearly wrong outputs. Recommend contract changes for future runs; never change this run's machine score retroactively.
7. **Diagnose** — per failed check, 3–5 line block:

   ```markdown
   ## <check name>
   - **Actual**: what the output contains (quote the value)
   - **Expected**: correct value, derived from inputs — not from the assertion text
   - **Root cause**: why it's wrong
   - **Fix suggestion**: one concrete action
   ```

   Write to `<run_dir>/diagnosis.md` — improve-step feedback channel. Specific beats vague.

Fail closed: unperformable read-only → fail with reason stated. Never modify outputs to ease verification.

## Outputs

- `<run_dir>/verifier_audit.json` (objective) — verifier-derived findings beyond the deterministic suite, labeled audit checks. Never overwrite/revise deterministic `<run_dir>/grading.json`.
- `<run_dir>/grading.json` (subjective-only) — schema `expectations[]` (`text`/`passed`/`evidence`) + `summary`; judgment criteria identified as subjective.
- `<run_dir>/diagnosis.md` — only on failure.
- `eval_feedback` in audit/subjective grading — weak/missing assertions for next iteration; do not back-edit this run's score.

## Co-evolving checks

Persist at `<scratch>/<skill>-verifier/`: `eval-<id>/<config>/checks.py` (per config, refined per iteration), `notes.md` (blind spots). Arms (with_skill / old_skill) keep separate checks — a shared path races; the second verifier inherits wrong-arm-calibrated checks.

- Iteration 1: from scratch. Iteration N+1: load persisted checks, revise where task/verdicts changed — never blindly regenerate.
- User feedback or canonical check contradicting a verdict ("pass" actually wrong, or vice versa) = verifier bug: update checks to catch it. Checks co-evolve with the skill — stops the loop from accepting reward-hacked outputs.

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
