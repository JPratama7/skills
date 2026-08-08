# Grader, Comparator, and Analyzer Agents

Use these prompts when spawning specialized agents. If the harness does not support subagents, run the same logic inline.

---

## Grader Agent

Evaluate expectations against an execution transcript and outputs.

### Inputs

- `expectations`: list of assertions
- `transcript_path`: path to the execution transcript
- `outputs_dir`: directory with output files

### Process

1. Read the transcript and note the prompt, steps, and final result.
2. List and examine each output file relevant to the assertions.
3. For each expectation, search for evidence and determine PASS or FAIL. The burden of proof is on the expectation.
4. Extract implicit claims from the outputs and verify them.
5. Read `user_notes.md` if it exists.
6. Critique the evals — flag assertions that would pass for clearly wrong outputs or important gaps.
7. Read `metrics.json` and `timing.json` if present.
8. Write `grading.json` to `{outputs_dir}/../grading.json`.

### Output

```json
{
  "expectations": [
    {"text": "...", "passed": true, "evidence": "..."}
  ],
  "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0},
  "execution_metrics": {},
  "timing": {},
  "claims": [],
  "user_notes_summary": {},
  "eval_feedback": {}
}
```

Pass only when the evidence reflects genuine task completion, not surface compliance.

---

## Blind Comparator Agent

Compare two outputs without knowing which skill produced them.

### Inputs

- `output_a_path`
- `output_b_path`
- `eval_prompt`
- `expectations` (optional)

### Process

1. Examine both outputs.
2. Build a rubric with content and structure dimensions.
3. Score each output 1–5 per criterion.
4. Check expectations if provided.
5. Pick a winner based on rubric, then expectations, then tie.
6. Write `comparison.json`.

### Output

```json
{
  "winner": "A",
  "reasoning": "...",
  "rubric": {"A": {...}, "B": {...}},
  "output_quality": {"A": {...}, "B": {...}},
  "expectation_results": {"A": {...}, "B": {...}}
}
```

Ties should be rare.

---

## Post-hoc Analyzer Agent

After the comparator picks a winner, figure out why and how to improve the loser.

### Inputs

- `winner`: "A" or "B"
- `winner_skill_path`
- `winner_transcript_path`
- `loser_skill_path`
- `loser_transcript_path`
- `comparison_result_path`
- `output_path`

### Process

1. Read the comparison result.
2. Read both skills and both transcripts.
3. Compare structural differences, instruction following, tool usage, and error handling.
4. Identify winner strengths and loser weaknesses.
5. Generate prioritized, categorized improvement suggestions.
6. Write `analysis.json`.

### Output

```json
{
  "comparison_summary": {...},
  "winner_strengths": [...],
  "loser_weaknesses": [...],
  "instruction_following": {"winner": {...}, "loser": {...}},
  "improvement_suggestions": [
    {"priority": "high", "category": "instructions", "suggestion": "...", "expected_impact": "..."}
  ],
  "transcript_insights": {...}
}
```

---

## Benchmark Notes Agent

Review all benchmark run results and produce freeform observations.

### Inputs

- `benchmark_data_path`: path to `benchmark.json`
- `skill_path`
- `output_path`

### Process

1. Read `benchmark.json`.
2. For each assertion, check whether it always passes, always fails, or is highly variable across runs.
3. Look for cross-eval patterns and metric outliers.
4. Write a JSON array of strings to `output_path`.

Do not suggest skill improvements here — only report patterns.
