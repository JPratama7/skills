# Eval Pipeline — Layout, Schemas, Grading

Field names matter — the bundled scripts and the review viewer depend on them.

## Run directory layout

```
<scratch>/<skill>-workspace/
└── iteration-N/
    ├── benchmark.json / benchmark.md       # from aggregate_benchmark.py
    ├── review.html                         # from make_review.py
    └── eval-<id>-<name>/
        ├── eval_metadata.json
        ├── with_skill/   { outputs/, grading.json, timing.json }
        └── old_skill/ or without_skill/   { outputs/, grading.json, timing.json }
```

Multiple runs per configuration use `run-1/`, `run-2/` inside the config dir.

## evals.json

Skill-level eval set, one per skill: `<scratch>/<skill>-evals/evals.json`.

```json
{
  "skill_name": "example-skill",
  "version": "1.0.0",
  "evals": [
    {
      "id": 1,
      "name": "descriptive-name",
      "prompt": "The user's task prompt",
      "expected_output": "What a good result looks like",
      "files": ["path/to/input.file"],
      "assertions": ["The output file exists", "The output contains X"]
    }
  ]
}
```

- `skill_name`/`version` must match the skill's frontmatter.
- `files` — optional input fixtures, copied into each run's workspace.
- `assertions` — objective checks; add after the first run.

## eval_metadata.json (per eval dir)

```json
{"eval_id": 1, "eval_name": "descriptive-name", "prompt": "...", "assertions": ["..."]}
```

## timing.json (per run)

```json
{"total_tokens": 84852, "duration_ms": 23332}
```

Nulls are fine when the harness hides them.

## grading.json (per run)

```json
{
  "expectations": [
    {"text": "The output includes the name 'John Smith'",
     "passed": true,
     "evidence": "Found in outputs/result.csv line 3"}
  ],
  "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0}
}
```

`expectations[]` requires exactly `text`, `passed`, `evidence` — the viewer
depends on these names. `summary` is what aggregate_benchmark.py reads.
Optional extras: `execution_metrics`, `timing`, `claims`, `eval_feedback`.

Grading discipline: burden of proof is on the expectation — pass only on
genuine evidence in outputs, not surface compliance. Flag assertions that
would also pass for clearly wrong outputs.

## benchmark.json

Written by aggregate_benchmark.py. Shape:

```json
{
  "metadata": {"skill_name": "...", "timestamp": "...", "evals_run": [1, 2],
               "runs_per_configuration": 1},
  "runs": [
    {"eval_id": 1, "eval_name": "...", "configuration": "with_skill",
     "run_number": 1,
     "result": {"pass_rate": 0.85, "passed": 6, "failed": 1, "total": 7,
                "time_seconds": 42.5, "tokens": 3800, "errors": 0},
     "expectations": [{"text": "...", "passed": true, "evidence": "..."}]}
  ],
  "run_summary": {
    "with_skill": {"pass_rate": {"mean": 0.85, "stddev": 0.05}},
    "without_skill": {"pass_rate": {"mean": 0.35, "stddev": 0.08}},
    "delta": {"pass_rate": "+0.50"}
  }
}
```

Keep `configuration` (not `config`) and nest metrics under `result`.

## Grading procedure (inline or as a subagent prompt)

1. Read the run's `eval_metadata.json` (prompt + assertions) and `outputs/`.
2. For each assertion, search outputs for concrete evidence → PASS/FAIL.
   A hallucinated file that "looks right" is a FAIL if the evidence is not in
   the actual output.
3. Verify implicit claims (counts, formats, cited facts) where cheap.
4. Critique the eval: flag assertions that would pass for wrong outputs, and
   important behaviors no assertion covers.
5. Write `grading.json`.

For programmatic assertions (file exists, value present, format matches),
write a grading script instead of judging by eye.

## Optional: blind comparison and analysis

When a human is not in the loop, spawn a comparator agent: give it both
outputs unlabeled (A/B), the eval prompt, and the assertions; ask for a
winner with reasoning. Follow with an analyzer pass on the loser's skill +
transcript to produce prioritized improvement suggestions. Skip both when a
human reviews — their feedback is the higher-signal path.
