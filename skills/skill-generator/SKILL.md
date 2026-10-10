---
name: skill-generator
version: 2.2.4
description: Create, evaluate, improve, and package SKILL.md-based agent skills. Trigger whenever users ask to build or revise a skill, run evals or benchmarks, optimize its description, or package it for any harness.
---

# Skill Generator

Build and ship skills. Keep repeatable work deterministic in stdlib scripts; reserve model judgment for subjective decisions.

## Workflow

1. Capture the requested outcome, output, target harness (default: current), and objective vs. subjective criteria; ask only for missing information.
2. For a new skill or substantial capability, use `references/design.md`; otherwise make the requested change directly.
3. Draft `SKILL.md` in concise, imperative, why-focused language. Keep it under ~500 lines; move depth to indexed, on-demand references.
4. Define 2–3 evals using the documented schema. Separate mechanical `assertions` from qualitative `review_criteria`; keep `expected_output` evaluator-only.
5. Before launching runs, discover how the target harness exports LLM statistics (tokens, duration, model id) — run notifications, transcript/export files, telemetry config, CLI stats commands; verify on a real run and cache the mechanism beside the eval artifacts (see `references/evals.md`). Then compare candidate with baseline (new skill: no skill; revision: pre-edit snapshot) using fresh isolated agents, identical prompts, and writes limited to each run's `outputs/`. Never expose answer keys. Use the requested model exactly; if unavailable, stop rather than substitute. Record model, token, and timing data.
6. Run deterministic checks first and preserve their scores. Use a fresh verifier for independent audits; never let it overwrite canonical results. Aggregate and review, then fix general causes and repeat until satisfied, feedback is empty, or gains stall.
7. Validate/package when requested or appropriate; update an existing repository index.

## Objective checks

Before runs, use the documented schema (include empty fields) and define one supported assertion per objective requirement. Assert each required output exists. Use flat `{id,type,file}` checks only. For exact headers, rows, and values, use anchored regex or parsed equality; substrings admit near-misses. Validate JSON and run `scripts/check_outputs.py`. Keep qualitative criteria out of scores and `expected_output` out of prompts. Full schema and types: `references/evals.md`.

## Grading

State `Role: coordinator.` Never grade your own runs inline when an independent verifier is available. For objective evals, deterministic checks own `grading.json`; fresh verifiers write separate audits, diagnoses, and per-config checks. For subjective-only evals, delegate grading or request human review, labeling judgments clearly. Aggregate with `scripts/aggregate_benchmark.py`; build a review with `scripts/make_review.py`, or show a table if no browser is available.

Use diagnoses and feedback to fix general causes; update verifier checks when evidence exposes a gap. Snapshot the pre-edit skill before each iteration.

## References (load on demand)

- New skills or substantial capabilities → `references/design.md`
- Eval schema, assertion types, run layout, grading → `references/evals.md`
- Blind verifier protocol and diagnosis → `references/verification.md`
- Subjective grader/comparator/analyzer prompts → `references/agent-roles.md`
- Harness install/package details and trigger queries → `references/harnesses.md`

## Avoid

- Treating one harness's mechanics as universal.
- Encoding subjective quality as boolean assertions or silently changing deterministic scores.
- Writing a skill for the user unless asked.
- Committing secrets, hardcoded paths, or eval artifacts into the skill.
