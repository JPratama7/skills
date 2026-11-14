---
name: skill-generator
version: 2.3.0
description: Create, evaluate, improve, and package SKILL.md-based agent skills. Trigger whenever users ask to build or revise a skill, run evals or benchmarks, optimize its description, or package it for any harness.
---

# Skill Generator

Build and ship skills. Repeatable work goes in deterministic stdlib scripts; model judgment is reserved for subjective decisions.

## Workflow

1. Grill the user into an implementer-ready spec (Capturing intent below).
2. New skill or substantial capability → `references/design.md`; otherwise make the change directly.
3. Draft `SKILL.md`: concise, imperative, why-focused; under ~500 lines — depth goes in indexed on-demand references.
4. Define 2–3 evals per `references/evals.md`: mechanical `assertions` separate from qualitative `review_criteria`; `expected_output` stays evaluator-only.
5. Discover how the harness exports LLM stats (tokens, duration, model id): notifications, transcripts/exports, telemetry config, CLI stats. Verify on a real run; cache the mechanism beside the eval artifacts. Compare candidate vs. baseline (new skill: none; revision: pre-edit snapshot) with fresh isolated agents, identical prompts, writes confined to each run's `outputs/`. Never expose answer keys. Use the requested model exactly — if unavailable, stop rather than substitute. Record model, token, timing data.
6. Run deterministic checks first and preserve their scores; a fresh verifier does independent audits and must not overwrite canonical results. Aggregate, review, fix general causes, repeat until satisfied, feedback empty, or gains stall.
7. Validate/package when requested; update an existing repository index.

## Capturing intent

Spec done = implementer could draft without asking: outcome, deliverable, trigger context, harness, objective vs. subjective criteria, scope, anti-features.

- Ask in rounds with a recommended answer on every question — the user confirms or corrects, and each recommendation exposes your model of their intent to falsification.
- Look up facts yourself first (repo, harness, existing skills); reserve questions for decisions only the user can make.
- Keep the spec in `.local/` scratch so a paused session resumes.

## Objective checks

Documented schema (include empty fields); one supported assertion per objective requirement; assert every required output exists. Flat `{id,type,file}` only; exact headers/rows/values via anchored regex or parsed equality — substrings admit near-misses. Validate JSON, run `scripts/check_outputs.py`. Qualitative criteria stay out of scores; `expected_output` stays out of prompts. Types: `references/evals.md`.

## Grading

State `Role: coordinator.` Never grade your own runs inline when an independent verifier is available. Objective evals: deterministic checks own `grading.json`; fresh verifiers write separate audits, diagnoses, per-config checks. Subjective-only: delegate grading or request human review, labeling judgments clearly. Aggregate via `scripts/aggregate_benchmark.py`; review via `scripts/make_review.py` (or a table if no browser).

Use diagnoses and feedback to fix general causes; update verifier checks when evidence exposes a gap. Snapshot the pre-edit skill before each iteration.

## Memory

`.memory/memory.json` → `skill-generator`: target harness and generator/evaluator model ids. Eval artifacts stay in gitignored `.local/` — config only.

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
