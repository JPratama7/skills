---
name: skill-generator
version: 2.0.0
description: Create, evaluate, iterate, and package agent skills for any harness. Use whenever the user wants to build a new skill, improve an existing one, run skill evals, benchmark skill performance, optimize a skill description, or package a skill for distribution. Trigger on phrases like "make a skill", "build a skill", "improve this skill", "skill eval", "skill benchmark", "package this skill", or any request involving skill development. Works in any harness that loads SKILL.md-based skills.
---

# Skill Generator

Build, test, and ship agent skills. A **skill** is a directory with a `SKILL.md`
(YAML frontmatter + instructions) plus optional `references/`, `scripts/`,
`assets/`. A **harness** is any runtime that loads skills. This skill is
self-contained: every tool it needs ships in its own `scripts/` (stdlib-only
Python, no installs).

## Workflow

1. Capture intent
2. Draft or edit `SKILL.md`
3. Write evals
4. Run test cases (with-skill vs baseline)
5. Grade, aggregate, review with the user
6. Improve

Repeat 4-6 until the user is satisfied or feedback is empty. Skip steps the
harness cannot support.

**Artifact rule:** evals, workspaces, grading scripts, and feedback live in a
gitignored scratch dir (`.local/` if present) — never inside the skill folder.
A shipped skill contains only `SKILL.md`, `references/`, `scripts/`, `assets/`.

## 1. Capture intent

Extract from the conversation first; ask only what is missing:

- What should the skill enable? When should it trigger (realistic prompts)?
- What does a good output look like?
- Are outputs objectively verifiable (files, code, data) or subjective
  (style, advice)? Verifiable → evals are worth it; subjective → rely on
  human review.
- Target harness? If unknown, assume the current one.

## 2. Draft the SKILL.md

Frontmatter — `name` and `description` required, rest optional:

```yaml
---
name: kebab-case-name        # <=64 chars
version: 1.0.0               # semver
description: What it does AND when to trigger. Pushy — this is the trigger mechanism.
compatibility: only if the skill needs subagents, browser, MCP, or filesystem
---
```

Body rules:

- Imperative voice; goal first; explain the *why* behind rules, not just MUST.
- Keep under ~500 lines; push depth into `references/*.md` and index each with
  a trigger condition under "Reference files (load on demand)".
- Show example inputs/outputs for non-obvious formats.
- If a deterministic step repeats across runs, bundle it as `scripts/*.py`.

## 3. Write evals

Save 2-3 realistic test prompts to `<scratch>/<skill>-evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "version": "1.0.0",
  "evals": [
    {
      "id": 1,
      "name": "descriptive-name",
      "prompt": "The user's task",
      "expected_output": "What good looks like",
      "files": [],
      "assertions": []
    }
  ]
}
```

Start without assertions; add objective, quantitatively checkable ones after
the first run. Never test subjective quality with boolean assertions. Field
reference: `references/evals.md`.

## 4. Run test cases

Goal on every harness: compare skill-on vs skill-off.

**Harness has subagents** — for each eval, spawn two agents in the same turn:

- with_skill: skill path + prompt + input files →
  `<scratch>/<skill>-workspace/iteration-N/eval-<id>-<name>/with_skill/outputs/`
- baseline: new skill → no skill (`without_skill/`); improved skill → the
  pre-edit snapshot (`old_skill/`)

While they run, draft assertions and write `eval_metadata.json` per eval.
When each completes, save `total_tokens`/`duration_ms` to `timing.json`
(nulls if the harness hides them).

**No subagents** — run each prompt inline, following the skill yourself; skip
baselines; save outputs under `eval-<id>-<name>/`. Human review compensates.

## 5. Grade, aggregate, review

Let `SG` = this skill's directory.

1. Grade each run against its assertions. Prefer a script over eyeballing.
   Save `grading.json` in the run dir; each assertion needs `text`, `passed`,
   `evidence`.
2. Aggregate: `python SG/scripts/aggregate_benchmark.py iteration-N --skill-name <skill>`
   → `benchmark.json` + `benchmark.md` (or compute pass rates by hand).
3. Review: `python SG/scripts/make_review.py iteration-N --skill-name <skill>`
   → standalone `review.html` with embedded outputs, grading, and a feedback
   download (`feedback.json`). Works headless; no server needed.
4. No browser at all → present results as markdown tables and collect
   feedback in chat.

## 6. Improve

Loop until the user is happy or feedback is empty:

- Generalize from specific feedback; don't overfit to test prompts.
- Cut sections that don't change behavior in runs.
- Prefer explaining *why* over stacking rules.
- Snapshot the pre-edit skill as the next iteration's baseline, then rerun.

## 7. Description optimization (optional, last)

A skill that never triggers is useless. Generate ~20 trigger queries
(8-10 should-trigger, 8-10 near-miss negatives), review them with the user,
then test candidate descriptions against the queries — spawn a fresh agent
per query if the harness allows, else judge inline — and keep the best
trigger rate on held-out negatives. Query format: `references/harnesses.md`.

## 8. Package and ship

```bash
python SG/scripts/quick_validate.py <skill-dir>          # frontmatter + naming checks
python SG/scripts/package_skill.py <skill-dir> -o <out>  # -> <name>.skill zip
```

Harnesses that read skill folders directly (e.g. Devin) get the directory
copied to their install path instead; `.skill` zips are only for harnesses
that consume them. Update the repo README index if one exists.

## Reference files (load on demand)

- Eval JSON schemas, run directory layout, grading format → `references/evals.md`
- Harness install paths, capabilities, packaging → `references/harnesses.md`

## Avoid

- Baking one harness's mechanics in as universal (paths, tools, viewers).
- Writing the skill for the user unless asked.
- Committing secrets, hardcoded paths, or eval artifacts into the skill.
