# Skill Generator — Schemas

This document defines the JSON schemas used by the eval pipeline. Field names matter — scripts and viewers depend on them.

---

## evals.json

Skill-level eval set. Located at `evals/evals.json`.

```json
{
  "skill_name": "example-skill",
  "version": "1.0.0",
  "evals": [
    {
      "id": 1,
      "name": "descriptive-name",
      "prompt": "User's task prompt",
      "expected_output": "What a good result looks like",
      "files": ["evals/files/sample.pdf"],
      "assertions": [
        "The output file exists",
        "The output contains the expected value"
      ]
    }
  ]
}
```

- `skill_name` and `version` must match the skill's frontmatter.
- `evals[].id` — unique integer.
- `evals[].name` — short slug used for directory names.
- `evals[].prompt` — the task.
- `evals[].expected_output` — human-readable success criteria.
- `evals[].files` — optional input files, relative to the skill root.
- `evals[].assertions` — objective checks used by the grader.

---

## eval_metadata.json

Per-eval snapshot, saved inside the run directory.

```json
{
  "eval_id": 1,
  "eval_name": "descriptive-name",
  "prompt": "User's task prompt",
  "assertions": ["The output file exists"]
}
```

---

## timing.json

Per-run timing.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

---

## metrics.json (optional)

Executor metrics, written by the runner if the harness provides them.

```json
{
  "tool_calls": {"Read": 5, "Write": 2},
  "total_tool_calls": 15,
  "total_steps": 6,
  "files_created": ["out.csv"],
  "errors_encountered": 0,
  "output_chars": 12450,
  "transcript_chars": 3200
}
```

---

## grading.json

Output from the grader agent.

```json
{
  "expectations": [
    {
      "text": "The output includes the name 'John Smith'",
      "passed": true,
      "evidence": "Found in transcript Step 3: 'Extracted names: John Smith, Sarah Johnson'"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 0,
    "total": 1,
    "pass_rate": 1.0
  },
  "execution_metrics": {
    "tool_calls": {"Read": 5, "Write": 2},
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450,
    "transcript_chars": 3200
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "The form has 12 fillable fields",
      "type": "factual",
      "verified": true,
      "evidence": "Counted 12 fields in field_info.json"
    }
  ],
  "user_notes_summary": {
    "uncertainties": ["Used 2023 data, may be stale"],
    "needs_review": [],
    "workarounds": ["Fell back to text overlay for non-fillable fields"]
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "The output includes the name 'John Smith'",
        "reason": "A hallucinated document would also pass — consider checking it appears as the primary contact."
      }
    ],
    "overall": "Assertions check presence but not correctness."
  }
}
```

Required fields in `expectations[]`: `text`, `passed`, `evidence`.

---

## benchmark.json

Output from the aggregate benchmark script.

```json
{
  "metadata": {
    "skill_name": "example-skill",
    "skill_path": "/path/to/skill",
    "executor_model": "model-id",
    "analyzer_model": "model-id",
    "timestamp": "2026-01-15T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },
  "runs": [
    {
      "eval_id": 1,
      "eval_name": "descriptive-name",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 42.5,
        "tokens": 3800,
        "tool_calls": 18,
        "errors": 0
      },
      "expectations": [
        {"text": "...", "passed": true, "evidence": "..."}
      ],
      "notes": ["note"]
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 45.0, "stddev": 12.0, "min": 32.0, "max": 58.0},
      "tokens": {"mean": 3800, "stddev": 400, "min": 3200, "max": 4100}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08, "min": 0.28, "max": 0.45},
      "time_seconds": {"mean": 32.0, "stddev": 8.0, "min": 24.0, "max": 42.0},
      "tokens": {"mean": 2100, "stddev": 300, "min": 1800, "max": 2500}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0",
      "tokens": "+1700"
    }
  },
  "notes": ["Skill adds 13s but improves pass rate by 50%."]
}
```

Important: keep `configuration` (not `config`) and nest `pass_rate` under `result`. Viewers depend on these exact paths.

---

## comparison.json

Output from the blind comparator.

```json
{
  "winner": "A",
  "reasoning": "Output A is complete and properly formatted. Output B is missing the date field.",
  "rubric": {
    "A": {
      "content": {"correctness": 5, "completeness": 5, "accuracy": 4},
      "structure": {"organization": 4, "formatting": 5, "usability": 4},
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {"correctness": 3, "completeness": 2, "accuracy": 3},
      "structure": {"organization": 3, "formatting": 2, "usability": 3},
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {"score": 9, "strengths": ["Complete"], "weaknesses": ["Minor style issue"]},
    "B": {"score": 5, "strengths": ["Readable"], "weaknesses": ["Missing date"]}
  },
  "expectation_results": {
    "A": {"passed": 4, "total": 5, "pass_rate": 0.80, "details": [{"text": "...", "passed": true}]},
    "B": {"passed": 3, "total": 5, "pass_rate": 0.60, "details": [{"text": "...", "passed": false}]}
  }
}
```

---

## analysis.json

Output from the post-hoc analyzer.

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner",
    "loser_skill": "path/to/loser",
    "comparator_reasoning": "Brief summary"
  },
  "winner_strengths": ["Clear step-by-step instructions"],
  "loser_weaknesses": ["Vague instruction led to improvisation"],
  "instruction_following": {
    "winner": {"score": 9, "issues": []},
    "loser": {"score": 6, "issues": ["Skipped validation step"]}
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Replace vague step with explicit steps.",
      "expected_impact": "Would eliminate ambiguity."
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Read skill -> Followed 5 steps -> Validated",
    "loser_execution_pattern": "Read skill -> Tried 3 methods -> No validation"
  }
}
```

---

## history.json

Tracks version progression in Improve mode.

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "example-skill",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```
