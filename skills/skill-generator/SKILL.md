---
name: skill-generator
version: 1.0.0
description: Create, evaluate, iterate, and package agent skills for any harness. Use whenever the user wants to build a new skill, improve an existing one, run skill evals, benchmark performance, optimize a skill description, or package a skill for distribution. Trigger on phrases like "make a skill", "build a skill", "improve this skill", "skill eval", "skill benchmark", "package this skill", or any request involving skill development. Applies to Claude Code, Claude.ai, Cowork, Devin, Vercel skills, and any other harness that loads SKILL.md-based skills.
---

# Skill Generator

A harness-agnostic skill for building, testing, and shipping agent skills.

A **harness** is the agent runtime that loads and invokes skills — Claude Code, Claude.ai, Cowork, Devin, the Vercel skills CLI, or any other system that reads a `SKILL.md` with YAML frontmatter. This skill abstracts the common parts of skill development and tells you how to adapt each step to the harness you are in.

## Core workflow

1. Capture intent
2. Draft or edit `SKILL.md`
3. Write evals in `evals/evals.json`
4. Run test cases (with-skill and baseline)
5. Grade, aggregate, review
6. Improve the skill
7. Package and ship

Repeat 4–6 until the skill is solid. Skip steps the harness cannot support, and load the relevant reference files when needed.

## Capture intent

Ask the user:

1. What should this skill enable an agent to do?
2. When should it trigger? What user prompts or contexts?
3. What output format is expected?
4. Are the outputs objectively verifiable (file transforms, data extraction, code, commands) or subjective (style, advice, design)? Verifiable skills benefit from evals; subjective skills rely on human review.
5. Which harness will run it? If unknown, assume the current one.

Extract as much as possible from the conversation before asking.

## Draft the SKILL.md

### Anatomy

```
skill-name/
├── SKILL.md                  required
├── references/               optional, loaded on demand
├── scripts/                  optional, for deterministic steps
├── assets/                   optional, templates, icons, fonts
└── evals/                    optional, test prompts and assertions
```

### Frontmatter

```yaml
---
name: skill-name
version: 1.0.0
description: When to trigger and what it does. Be pushy.
compatibility: optional — required tools, MCPs, or harness features
metadata:
  author: optional
  license: optional
---
```

- `name` — kebab-case, ≤64 chars.
- `version` — semver, `1.0.0` for first release.
- `description` — the trigger mechanism. Include what it does AND when to use it. Make it pushy to combat undertriggering.
- `compatibility` — only add if the skill needs a specific harness feature (subagents, browser, MCP, filesystem).

### Progressive disclosure

1. **Metadata** — always loaded: `name`, `description`, `version`, `compatibility`.
2. **SKILL.md body** — loaded when the skill triggers. Keep under ~500 lines; push depth into references.
3. **Bundled resources** — loaded only when the skill points to them.

### Body

- Imperative voice.
- Start with the goal, not background.
- Explain the *why* behind rules, not just `MUST`.
- Include example inputs/outputs for non-obvious formats.
- Use a "Reference files" section to index `references/*.md` with clear trigger conditions.

## Test cases

Save to `evals/evals.json`. See `references/schemas.md`.

```json
{
  "skill_name": "example-skill",
  "version": "1.0.0",
  "evals": [
    {
      "id": 1,
      "name": "descriptive-name",
      "prompt": "User's task",
      "expected_output": "What good looks like",
      "files": [],
      "assertions": []
    }
  ]
}
```

Start with 2–3 realistic prompts. Add `assertions` after the first run.

## Running evals

The goal is the same on every harness: compare skill-on vs skill-off and review the results. The mechanics depend on what the harness supports.

### If the harness supports subagents

For each eval, spawn two agents in the same turn:

- **With skill**: skill path + prompt + input files → `iteration-N/eval-<name>/with_skill/outputs/`
- **Baseline**:
  - New skill: no skill → `without_skill/outputs/`
  - Improved skill: snapshot old version → `old_skill/outputs/`

Write `eval_metadata.json` per eval.

While runs execute, draft quantitative `assertions` and update `evals.json` and `eval_metadata.json`.

When each run completes, capture `total_tokens` and `duration_ms` into `timing.json`.

### If the harness does not support subagents

Run test prompts inline one at a time, following the skill instructions yourself. Skip baseline runs. Save outputs to an `iteration-N/eval-<name>/` directory. Human review compensates for the lack of blind comparison.

## Grade, aggregate, review

1. Grade each run. For programmatic assertions, write a script rather than eyeballing. Save `grading.json`. See `references/schemas.md`.
2. Aggregate with `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>` if the script is available; otherwise compute pass rates manually.
3. Review with the harness's viewer. In Claude Code, use `eval-viewer/generate_review.py`. In Cowork or headless, use `--static` to write a standalone HTML. In other harnesses, present the results inline and ask the user for feedback.
4. Read `feedback.json` if it exists.

## Improve

Loop until the user is happy or feedback is empty:

1. Generalize from specific feedback.
2. Remove parts of the skill that are not pulling their weight.
3. Explain the *why* behind instructions.
4. If every test run reinvents the same helper script, bundle it under `scripts/`.

After improving, run a new `iteration-N+1/` and compare with the previous one.

## Description optimization

A skill is useless if it never triggers. After the skill is solid, optimize the `description`.

1. Generate 20 trigger eval queries — 8–10 should-trigger, 8–10 should-not-trigger. Make negatives near-misses. Save as JSON.
2. Review with the user.
3. If the harness has a description optimizer (e.g., `claude -p` in Claude Code), run it in the background. Otherwise iterate manually: test each description against the queries and keep the one that triggers correctly most often.
4. Update the frontmatter with the best description.

## Package and ship

Validate first:

```bash
python scripts/quick_validate.py <skill-directory>
```

Then package:

```bash
python scripts/package_skill.py <skill-directory> [output-dir]
```

This produces a `.skill` file (a zip of the skill folder) suitable for the Vercel skills CLI and harnesses that consume it. For Devin or other harnesses, copy the skill directory into the appropriate path instead of using the zip.

## Reference files (load on demand)

- Need JSON schemas for evals, grading, benchmark, comparison, analysis → `references/schemas.md`
- Need to adapt a step to a specific harness → `references/harnesses.md`
- Need grader/comparator/analyzer prompts → `references/agents.md`
- Need to optimize the description → `references/description-optimization.md`

## What to avoid

- Don't bake in Claude-only mechanics as if they are universal.
- Don't write the skill for the user unless they ask.
- Don't add evals that test subjective quality with boolean assertions.
- Don't commit secrets, hardcoded paths, or harness-specific URLs.
