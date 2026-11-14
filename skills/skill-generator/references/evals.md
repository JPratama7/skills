# Eval Pipeline — Layout, Schemas, Grading

Field names matter — scripts and the review viewer depend on them. `<scratch>` = gitignored `.local/`; eval workspaces are iteration checkpoints and must survive reboots. `/tmp/` only for disposable files.

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

Multiple runs per configuration: `run-1/`, `run-2/` inside the config dir.

## evals.json

One skill-level set at `<scratch>/<skill>-evals/evals.json`; parsed with Python stdlib.

```json
{"skill_name":"example-skill","version":"1.0.0",
 "evals":[{"id":1,"name":"descriptive-name","prompt":"The user's task prompt",
   "expected_output":"Evaluator-only description of a correct result",
   "files":["path/to/input.file"],
   "assertions":[{"id":"result-json","type":"json_valid","file":"result.json"},
     {"id":"status","type":"json_value_eq","file":"result.json","path":"status","expected":"complete"}],
   "review_criteria":[]}]}
```

- `skill_name`/`version` must match the skill's frontmatter.
- `files` — optional input fixtures, copied into each run's workspace.
- `assertions` — objective, mechanically decidable checks defined before execution. Never encode prose quality or judgment calls as booleans.
- `review_criteria` — optional qualitative criteria for human/independent model review; keep separate from deterministic pass rates.

## Deterministic assertion contract

Pass the assertion array as a `.json` file to `scripts/check_outputs.py` with the run's `outputs/` dir. Each assertion: unique `id`, `type`, relative `file`. Checker rejects malformed contracts, unsupported types, and paths outside `outputs/`. Writes canonical `grading.json`; exit 0 = all pass, 1 = check failed, 2 = invalid contract or execution error.

| Type | Additional fields | Check |
|---|---|---|
| `file_exists` | — | File exists (directories do not count) |
| `text_contains` | `text` | UTF-8 text contains the exact substring |
| `regex` | `pattern` | Python regular expression matches UTF-8 text |
| `json_valid` | — | File parses as JSON |
| `json_value_eq` | `path`, `expected` | Dot-separated keys / list indexes resolve to exactly equal JSON value |
| `csv_row_count` | `expected`, optional `header` (default `true`) | Number of CSV data rows equals `expected` |

```bash
python SG/scripts/check_outputs.py assertions.json run/outputs -o run/grading.json
```

Rules:

- One assertion per requirement or small invariant group → partial results stay interpretable.
- Prefer exact values from fixtures, schema parsing, row counts, bounds, invariants over vague checks like "looks correct". Every check must be falsifiable — an obviously wrong artifact fails it.
- Record inputs/expected values in the eval definition, never in agent-facing run prompts.
- Deterministic checker output is the reproducible score; verifier findings are a separately labeled audit — may reveal missing assertions, must not silently rewrite deterministic scores.
- No supported check fits → decide if the requirement is objective and scriptable; otherwise move it to `review_criteria` and report the judgment separately — don't fake determinism.

## eval_metadata.json (per eval dir)

```json
{"eval_id":1,"eval_name":"descriptive-name","prompt":"...","assertions":[{"id":"...","type":"...","file":"..."}]}
```

## timing.json (per run)

```json
{"total_tokens":84852,"duration_ms":23332}
```

Before the first run of an iteration, discover how the harness exports LLM stats (tokens, durations, model ids). Cheapest first: run/subagent completion notifications; transcript or export-flag files with final token metrics; CLI stats/usage commands; telemetry config (e.g. OpenTelemetry exporters); usage APIs. Verify on a real run — inspect actual fields, don't trust docs — then write the mechanism next to the eval artifacts so later iterations reuse it. Never guess field names.

Nulls acceptable only after discovery finds no usable source; record what was tried. Record the model id when available. Benchmark reads `total_tokens` from timing metadata; if missing, legacy output-character metrics are the fallback and must not be described as token counts.

## grading.json (per run)

```json
{"expectations":[{"text":"The output includes the name 'John Smith'","passed":true,"evidence":"Found in outputs/result.csv line 3"}],
 "summary":{"passed":1,"failed":0,"total":1,"pass_rate":1.0}}
```

`expectations[]` requires exactly `text`, `passed`, `evidence` — the viewer depends on them. `summary` is what aggregate_benchmark.py reads. Optional extras: `execution_metrics`, `timing`, `claims`, `eval_feedback`.

Tolerated variants: `checks` for `expectations`, per-check `name` for `text`, `summary` as a plain string, null timing — stats then derive from the check list. Prefer the canonical schema; fallbacks exist so a verifier's output never crashes aggregation.

Grading discipline: burden of proof is on the expectation — pass only on genuine evidence in outputs, not surface compliance. Flag assertions that would also pass for clearly wrong outputs.

## benchmark.json

Written by aggregate_benchmark.py:

```json
{"metadata":{"skill_name":"...","timestamp":"...","evals_run":[1,2],"runs_per_configuration":1},
 "runs":[{"eval_id":1,"eval_name":"...","configuration":"with_skill","run_number":1,
   "result":{"pass_rate":0.85,"passed":6,"failed":1,"total":7,"time_seconds":42.5,"tokens":3800,"errors":0},
   "expectations":[{"text":"...","passed":true,"evidence":"..."}]}],
 "run_summary":{"with_skill":{"pass_rate":{"mean":0.85,"stddev":0.05}},
   "without_skill":{"pass_rate":{"mean":0.35,"stddev":0.08}},"delta":{"pass_rate":"+0.50"}}}
```

Keep `configuration` (not `config`); nest metrics under `result`.

## Role separation eval assertion

Add one assertion per eval checking the trace for the main agent grading its own runs without delegation; passes only if all grading was done by a fresh verifier subagent — catches role-confusion drift the SKILL.md instruction alone won't prevent. On failure, don't patch the output — re-run step 5 with a delegated verifier.

```json
{"text":"main-agent-never-graded-inline","passed":true,
 "evidence":"All 3 evals graded by a fresh verifier subagent, confirmed by trace"}
```

## Grading procedure

Default: spawn an **independent verifier** per run — fresh agent seeing only the prompt, inputs, and `outputs/` (never the skill or `expected_output`), deriving its own executable checks persisted under `<scratch>/<skill>-verifier/`. Protocol: `verification.md`.

Fallback (inline or grader subagent — `agent-roles.md`): read `eval_metadata.json` and `outputs/`; per assertion find concrete evidence → PASS/FAIL (a "looks right" file fails without real evidence); verify cheap implicit claims; flag weak assertions and coverage gaps; write `grading.json`. For programmatic assertions, grade with a script, not by eye.

## Optional: blind comparison and analysis

No human in the loop → spawn a comparator subagent (unlabeled A/B outputs, eval prompt, assertions → winner with reasoning), then an analyzer pass over `benchmark.json` + losing config's run diffs for prioritized suggestions. Templates: `agent-roles.md`. Skip both when a human reviews — their feedback is the higher-signal path.
