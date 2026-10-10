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

Use one skill-level eval set at `<scratch>/<skill>-evals/evals.json`. JSON is
parsed with Python's standard library, so evaluation adds no package dependency.

```json
{
  "skill_name": "example-skill",
  "version": "1.0.0",
  "evals": [{
    "id": 1,
    "name": "descriptive-name",
    "prompt": "The user's task prompt",
    "expected_output": "Evaluator-only description of a correct result",
    "files": ["path/to/input.file"],
    "assertions": [
      {"id": "result-json", "type": "json_valid", "file": "result.json"},
      {"id": "status", "type": "json_value_eq", "file": "result.json",
       "path": "status", "expected": "complete"}
    ],
    "review_criteria": []
  }]
}
```

- `skill_name`/`version` must match the skill's frontmatter.
- `files` — optional input fixtures, copied into each run's workspace.
- `assertions` — objective, mechanically decidable checks. Define these before
  execution when the requirement is already objectively stated; never encode
  prose quality or other judgment calls as boolean assertions.
- `review_criteria` — optional qualitative criteria for human or independent
  model review. Keep these separate from deterministic pass rates.

## Deterministic assertion contract

Pass the eval's assertion array in a `.json` file to
`scripts/check_outputs.py` with the run's `outputs/` directory. Each assertion
has a unique `id`, `type`, and relative `file` path. The checker rejects
malformed contracts, unsupported types, and paths outside `outputs/`. It writes
canonical JSON `grading.json`; exit status is 0 when all checks pass, 1 when a
check fails, and 2 for an invalid contract or execution error.

Supported types:

| Type | Additional fields | Check |
|---|---|---|
| `file_exists` | — | File exists (directories do not count) |
| `text_contains` | `text` | UTF-8 text contains the exact substring |
| `regex` | `pattern` | Python regular expression matches UTF-8 text |
| `json_valid` | — | File parses as JSON |
| `json_value_eq` | `path`, `expected` | Dot-separated object keys / list indexes resolve to an exactly equal JSON value |
| `csv_row_count` | `expected`, optional `header` (default `true`) | Number of CSV data rows equals `expected` |

Example:

```bash
python SG/scripts/check_outputs.py assertions.json run/outputs -o run/grading.json
```

Use one assertion per requirement or small invariant group so partial results
remain interpretable. Prefer exact values derived from input fixtures, schema
parsing, row counts, bounds, and invariants over vague checks like "looks
correct". A check must be falsifiable: ensure an obviously wrong artifact would
fail it. Record inputs and expected values in the eval definition, not in
agent-facing run prompts. Deterministic checker results are the reproducible
score; independent verifier findings are a separately labeled audit and may
reveal missing assertions, but must not silently rewrite deterministic scores.

If no supported check fits, first decide whether the requirement is actually
objective and can be checked with a small script. Otherwise move it to
`review_criteria` and report the judgment separately; do not pretend it is a
deterministic result.


## eval_metadata.json (per eval dir)

```json
{"eval_id": 1, "eval_name": "descriptive-name", "prompt": "...", "assertions": [{"id": "...", "type": "...", "file": "..."}]}
```

## timing.json (per run)

```json
{"total_tokens": 84852, "duration_ms": 23332}
```

Before the first run of an iteration, discover how the harness exports LLM
statistics — token totals, durations, model ids. Candidate sources, cheapest
first: run/subagent completion notifications; session transcript or
export-flag files carrying final token metrics; CLI stats/usage commands;
telemetry config blocks (e.g. OpenTelemetry exporters); usage APIs. Verify the
chosen source on a real run — inspect actual output fields rather than
trusting docs — then write the working mechanism next to the eval artifacts so
later iterations reuse it instead of rediscovering. Do not guess field names.

Nulls are acceptable only after that discovery pass finds no usable source;
record what was tried. Record the model identifier when available. The
benchmark reads `total_tokens` from timing metadata; if unavailable, legacy
output-character metrics remain a fallback and must not be described as token
counts.

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

The tooling tolerates common variants: a check list named `checks` instead
of `expectations`, per-check `name` instead of `text`, a `summary` written
as a plain string, and null timing values. Stats are then derived from the
check list. Prefer the canonical schema above; the fallbacks exist so a
verifier's output never crashes aggregation.

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

## Role separation eval assertion

Add one assertion per eval that checks the conversation log or agent trace for
any instance of the main agent grading its own runs without delegation. The
assertion passes only if all grading was performed by a fresh verifier
subagent. Purpose: catch role-confusion drift that the SKILL.md instruction
alone won't prevent.

Example:
```json
{
  "text": "main-agent-never-graded-inline",
  "passed": true,
  "evidence": "All 3 evals graded by a fresh verifier subagent, confirmed by trace"
}
```

When this assertion fails, the fix is not to patch the output — it is to
re-run step 5 correctly with a delegated verifier.

## Grading procedure

Default: spawn an **independent verifier** per run — a fresh agent that sees
only the prompt, inputs, and `outputs/` (never the skill or
`expected_output`), derives its own executable checks, and persists them
under `<scratch>/<skill>-verifier/`. Full protocol, boundaries, and the
`diagnosis.md` format: `verification.md`.

Fallback (inline or lightweight grader subagent — see `agent-roles.md`):

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

When a human is not in the loop, spawn a comparator subagent: give it both
outputs unlabeled (A/B), the eval prompt, and the assertions; ask for a
winner with reasoning. Follow with an analyzer pass over `benchmark.json`
plus the losing config's run diffs for prioritized improvement suggestions.
Prompt templates: `agent-roles.md`. Skip both when a human reviews — their
feedback is the higher-signal path.
