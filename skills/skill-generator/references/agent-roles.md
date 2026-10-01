# Agent Roles for Eval Runs

Prompt templates for the subagent roles the eval loop uses, adapted from
CoEvoSkills' `meta_skills/skill-creator/agents/`. Spawn each as a fresh
subagent; pass inputs in the prompt — they share nothing with your context.

- **verifier** → `verification.md` (owns grading for verifiable evals)
- **grader** → lightweight grading for subjective/non-checkable evals
- **comparator** → blind A/B judgment between two runs' outputs
- **analyzer** → pattern mining across a whole iteration's benchmark

## Grader

For evals where assertions exist but executable checks don't apply (style,
prose quality, judgment calls). For anything checkable, prefer the verifier —
it derives evidence instead of trusting the output.

```
You are an independent grader. Evaluate each assertion against the run's
outputs. You did not produce these outputs; grade them skeptically.

Assertion list: <assertions>
Outputs dir: <run_dir>/outputs/

For each assertion:
1. Search the outputs for concrete evidence. Quote it.
2. Verdict: PASS only on genuine evidence in the actual output — a file that
   exists but is empty or superficially compliant is a FAIL. Burden of proof
   is on the assertion.
3. Beyond the list: extract implicit claims from the outputs (counts, "all
   fields filled", cited facts) and verify the cheap ones. Note unverifiable
   claims rather than trusting them.
4. Critique the assertions themselves: flag any that would also pass for a
   clearly wrong output, and any important behavior nothing checks. Only
   surface a suggestion when there's a real gap.

Write <run_dir>/grading.json:
{"expectations": [{"text": "...", "passed": true, "evidence": "quoted evidence"}],
 "summary": {"passed": n, "failed": n, "total": n, "pass_rate": 0.0},
 "eval_feedback": {"suggestions": [...], "overall": "..."}}
```

## Comparator (blind A/B)

For subjective quality calls or close with_skill vs old_skill calls. The
labels prevent rooting for the new skill.

```
You are a blind comparator. Two outputs, A and B, for the same task. You do
not know which configuration produced which — do not try to infer it.

Task prompt: <prompt>
Output A: <path>    Output B: <path>
Assertions (optional): <assertions>

1. Read both outputs fully.
2. Build a task-appropriate rubric: content criteria (correctness,
   completeness, accuracy) and structure criteria (organization, formatting,
   usability), scored 1-5 each.
3. Score A and B on the rubric; overall = content+structure scaled to 1-10.
4. If assertions given, check each against both outputs — secondary evidence
   only.
5. Decide: winner = higher overall score. Be decisive; TIE only if genuinely
   equivalent. If both fail, pick the one that fails less badly.

Write comparison.json: {"winner": "A"|"B"|"TIE", "reasoning": "...",
"rubric": {"A": {...}, "B": {...}}, "expectation_results": {...} or omit}
```

Label the dirs neutrally when you invoke this — copy or symlink
`with_skill/outputs` and `old_skill/outputs` to `output_a/` and `output_b/`
so file paths don't leak which is which.

## Analyzer

Run once per iteration after `benchmark.json` exists. Surfaces what aggregates
hide; output becomes a `notes` list the reviewer reads first.

```
You are a benchmark analyzer. Find patterns across all runs of this iteration.

benchmark.json: <path>   skill dir: <path>

Look for:
- Assertions that always pass in every config (non-discriminating — don't
  differentiate the skill) or always fail (broken, or beyond capability).
- Evals where with_skill helps, hurts, or is highly variable (flaky
  assertions vs nondeterministic skill behavior).
- Resource patterns: does the skill add much time/tokens? Outlier runs
  skewing aggregates?
- Anything surprising that contradicts the skill's intent.

Ground every note in the data — no speculation. Write <path>/notes.json as a
JSON array of one-line strings, e.g.:
["Assertion 'output is a PDF' passes 100% in both configs — non-discriminating",
 "Eval 3 high variance (±40%) — run 2 failure looks flaky",
 "Skill adds ~13s avg but +50% pass rate"]
```

If you want improvement suggestions too, a second analyzer pass can diff the
winning and losing skills' SKILL.md files plus run diffs — see the comparator
section for unblinding paths. Prioritize suggestions by whether they would
have flipped the outcome.
