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

1. For a new skill idea, ground and design the solution before drafting; for an
   existing skill, capture the requested change
2. Draft or edit `SKILL.md`
3. Write evals
4. Run test cases (with-skill vs baseline)
5. Grade, aggregate, review with the user
6. Improve

Repeat 4-6 until the user is satisfied or feedback is empty. Skip steps the
harness cannot support. The design flow applies to new skills and substantial
new capabilities; skip it for narrow edits and eval/packaging requests.

## 1. Capture intent and design new skills

Extract intent from the conversation first and ask only for missing information.
For a new skill, work through these checkpoints before drafting `SKILL.md`:

1. **Ground the problem.** Identify the pain point and request 2-3 concrete
   examples of current inputs, deliverables, or manual workflows. If none are
   available, ask one focused question about the main pain point or help the
   user identify a representative, anonymized or synthetic example. Keep the
   exchange incremental; don't turn the first follow-up into a full requirements
   questionnaire. Pause solution design and drafting until there is a concrete
   example to analyze.
2. **Check existing coverage.** Inspect the names and descriptions of relevant
   skills or tools in the current repository/harness. Identify overlaps and
   gaps without reading unrelated implementations. For each plausibly relevant
   asset, record its role and decide whether to reuse, extend, call, or keep it
   separate; don't imply reuse merely because an adjacent asset exists.
3. **Confirm the gap.** Summarize the problem, existing coverage, and missing
   capability, then ask whether that gap is correct. Stop here until the user
   confirms or corrects it; do not propose approaches or architecture in the
   same turn as this confirmation request.
4. **Analyze examples and separate work by nature.** After confirmation, extract
   repeated steps, decisions, and failure points. Make mechanical, repeatable
   work deterministic (scripts, validators, parsers) where practical; reserve
   skill instructions for judgment, synthesis, and ambiguous cases.
5. **Compare approaches.** Offer 2-3 plausible approaches, lead with a
   recommendation, and state what each makes deterministic, what needs model
   judgment, the trade-offs, and which existing assets each reuses or keeps
   separate. After an approach is selected, define:
   - **Table stakes** — required baseline behaviors.
   - **Differentiators** — value beyond an unassisted model.
   - **Anti-features** — boundaries that prevent scope creep.
6. **Sketch the architecture.** Decide whether this is one skill or needs a
   larger construct supported by the target harness. For each selected asset,
   state its responsibility, how the workflow invokes or composes it, and what
   data it receives and returns. Note important unavailable, malformed, or
   inconclusive-input behavior. Distinguish confirmed interfaces from
   assumptions; don't imply an asset was inspected when only its name or
   description was available. Keep the first version minimal and park
   nonessential ideas as deferred work.
7. **Hand off to drafting.** Recap the agreed problem, examples, scope, and
   architecture as a concise design brief in the conversation or scratch space;
   use it to draft the skill and its evals. Don't create a separate handoff file
   unless it will help resume or coordinate work across sessions.

Keep discussion incremental: ask one focused question at a time when input is
missing, offer choices when the options are clear, and validate major decisions
before proceeding. Keep design summaries brief. For an existing skill revision,
extract the requested outcome and use the eval loop; don't repeat this design
process unless the change introduces a substantially new capability.

For every request, establish the trigger context and desired output, determine
whether results are objectively verifiable or need human review, and identify
the target harness (assume the current one if unspecified).

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

Give each run agent only the skill path, prompt, and input files — never the
expected output or why the eval exists. A fresh agent is only isolation if
the prompt doesn't leak the answer key.

While they run, draft assertions and write `eval_metadata.json` per eval.
When each completes, save `total_tokens`/`duration_ms` to `timing.json`
(nulls if the harness hides them).

**No subagents** — run each prompt inline, following the skill yourself; skip
baselines; save outputs under `eval-<id>-<name>/`. Human review compensates.

## 5. Grade, aggregate, review (grader role)

State your role: "Role: coordinator." If your next action is reading outputs
and writing a pass/fail verdict yourself, stop — you are about to grade
inline. Spawn a fresh verifier subagent instead.

Let `SG` = this skill's directory.

### 5.1 Delegate grading (must be a fresh agent)

Spawn one **independent verifier** per run — a fresh agent that sees only
the prompt, inputs, and outputs, never the skill or expected output
(protocol + prompt template: `references/verification.md`). The agent that
wrote the skill grading its own evals passes its own blind spots. The
verifier writes `grading.json` (`text`/`passed`/`evidence` + `summary`),
a `diagnosis.md` per failure (Actual / Expected / Root cause / Fix), and
persists its checks under `<scratch>/<skill>-verifier/` so they refine
across iterations rather than regenerate. For subjective evals where
executable checks don't apply, use the grader / blind-comparator /
analyzer roles in `references/agent-roles.md`.

### 5.2 Aggregate (deterministic — you may run this directly)

`python SG/scripts/aggregate_benchmark.py iteration-N --skill-name <skill>`
→ `benchmark.json` + `benchmark.md` (or compute pass rates by hand).

### 5.3 Review

`python SG/scripts/make_review.py iteration-N --skill-name <skill>`
→ standalone `review.html` with embedded outputs, grading, and a feedback
download (`feedback.json`). Works headless; no server needed. No browser
at all → present results as markdown tables and collect feedback in chat.

## 6. Improve

Loop until the user is happy or feedback is empty:

- Feed each run's `diagnosis.md` into the revision — it's denser than
  pass/fail: every failure arrives with a root cause and a concrete fix.
- When feedback contradicts a verifier verdict (a pass that's actually wrong,
  or vice versa), update the persisted checks too — they co-evolve with the
  skill.
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
- Independent verification protocol, diagnosis format, persistent checks → `references/verification.md`
- Grader / blind-comparator / analyzer subagent prompts → `references/agent-roles.md`
- Harness install paths, capabilities, packaging → `references/harnesses.md`

## Avoid

- Baking one harness's mechanics in as universal (paths, tools, viewers).
- Writing the skill for the user unless asked.
- Committing secrets, hardcoded paths, or eval artifacts into the skill.
