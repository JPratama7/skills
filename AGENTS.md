# AGENTS.md — Skill Development Guide

This repo hosts installable agent skills (`skills/<name>/SKILL.md`). This file
guides how to develop, iterate on, and ship skills here. It is the **only**
guide for skill development work in this repo.

## Repo layout

```
skills/
├── <skill-name>/
│   ├── SKILL.md          # required — frontmatter + instructions
│   └── references/       # optional — load-on-demand docs
├── writing-coach/        # reference example of a mature skill
└── doc-builder/          # reference example of a mature skill
.local/                   # gitignored — ALL iteration artifacts live here
AGENTS.md                 # this file
README.md                 # public index of skills
```

**`.local/` is the scratch space.** It is gitignored (`.gitignore` excludes
`.local/*`). Every eval run, workspace, grading script, session summary, and
feedback file goes there — never in the tracked tree. See
[Iteration artifacts](#iteration-artifacts) for the exact layout.

**Rule: nothing eval-related goes inside `skills/<name>/`.** No evals, test
fixtures, workspaces, outputs, grading files, or scratch scripts. The skill
directory ships only `SKILL.md` and `references/` — anything else belongs in
`.local/`. If a run needs fixture files, generate them under the eval's
`.local/` workspace, not beside the skill.

## Skill anatomy

A skill is a directory under `skills/` containing at minimum a `SKILL.md`:

```yaml
---
name: skill-name
description: When to trigger and what it does. This is the primary triggering
  mechanism — include both what the skill does AND specific contexts for when
  to use it. Make it a little "pushy" to combat undertriggering.
---
```

Followed by markdown instructions. Optional bundled resources:

- `references/` — docs loaded on demand. Keep `SKILL.md` under ~500 lines;
  push depth into reference files and index them from `SKILL.md` with a
  "Reference files (load on demand)" section. Each entry is
  `- <trigger condition> → \`references/<file>.md\``. See
  `skills/writing-coach/SKILL.md` and `skills/doc-builder/SKILL.md` for the
  established pattern.

## Writing a skill

1. **Capture intent** — what should this skill enable, when should it trigger,
   what's the expected output. Confirm with the user before drafting.
2. **Draft `SKILL.md`** — frontmatter (`name`, `description`) + instructions.
   Prefer imperative form. Explain the *why* behind rules rather than stacking
   MUSTs. Keep it general, not overfit to example prompts.
3. **Add reference files** only when `SKILL.md` is approaching the ~500 line
   limit or a topic needs depth that would bloat the main file. Index every
   reference file from `SKILL.md` with a clear trigger condition.
4. **Stay lean** — every section earns its place. Remove things that aren't
   pulling their weight. If a rule isn't changing behavior in evals, cut it.

## The eval loop

Skills are improved iteratively: draft → test → review → improve → repeat.
The `skill-generator` skill (`~/.config/devin/skills/skill-generator/`)
drives this loop. The core sequence:

1. **Write evals** — 2-3 realistic test prompts saved to
   `.local/.<skill>-evals/evals.json` — never inside `skills/<name>/`. Each
   eval has `id`, `name`, `prompt`, `expected_output`, `files`, and
   `assertions` (objectively verifiable checks with descriptive names).
2. **Spawn runs in parallel** — for each eval, run two subagents in the same
   turn: one *with* the skill, one *baseline*. For a new skill the baseline is
   no-skill (`without_skill/`); for improving an existing skill the baseline
   is the old version (`old_skill/`), snapshotted before editing. Save outputs
   to `.local/.<skill>-workspace/iteration-<N>/eval-<id>-<name>/{with_skill,baseline}/outputs/`.
3. **Draft assertions while runs are in progress** — don't idle. Write
   quantitative assertions, update `eval_metadata.json` and `evals.json`.
4. **Capture timing** — when each subagent completes, save `total_tokens` and
   `duration_ms` from the notification to `timing.json` in the run directory.
   This data is not persisted elsewhere.
5. **Grade** — evaluate each assertion against outputs. Save to `grading.json`
   in each run directory using fields `text`, `passed`, `evidence` (the viewer
   depends on these exact field names). For programmatically checkable
   assertions, write a script rather than eyeballing.
6. **Aggregate**:
   ```bash
   python ~/.config/devin/skills/skill-generator/scripts/aggregate_benchmark.py \
     .local/.<skill>-workspace/iteration-<N> --skill-name <skill>
   ```
   Produces `benchmark.json` and `benchmark.md`.
7. **Generate the eval viewer** — always do this before self-reviewing:
   ```bash
   python ~/.config/devin/skills/skill-generator/scripts/make_review.py \
     .local/.<skill>-workspace/iteration-<N> --skill-name <skill>
   ```
   Writes a standalone `review.html` into the iteration directory (no
   server needed). For iteration 2+, add
   `--previous-feedback .local/feedback.json` to carry over prior comments.
8. **User reviews** — the user opens `review.html`, clicks through outputs,
   leaves feedback, clicks "Download feedback.json". Copy the downloaded
   file into `.local/` for the next iteration to pick up.
9. **Read feedback, improve, repeat** — empty feedback means the eval was
   fine. Focus on evals with specific complaints. Generalize from feedback
   rather than overfitting to the test cases. Then rerun into
   `iteration-<N+1>/`.

Stop when the user is satisfied, feedback is all empty, or progress stalls.

## Iteration artifacts

All iteration artifacts live under `.local/` (gitignored). Layout for a skill
named `<skill>`:

```
.local/
├── .<skill>-evals/
│   └── evals.json                              # test prompts + assertions
├── .<skill>-workspace/
│   ├── iteration-1/
│   │   ├── benchmark.json                      # aggregate metrics
│   │   ├── benchmark.md                        # human-readable summary
│   │   ├── review.html                         # eval viewer (static)
│   │   └── eval-<id>-<name>/
│   │       ├── eval_metadata.json
│   │       ├── with_skill/
│   │       │   ├── outputs/                    # skill-produced files
│   │       │   ├── grading.json                # assertion results
│   │       │   └── timing.json
│   │       └── without_skill/  (or old_skill/)
│   │           ├── outputs/
│   │           ├── grading.json
│   │           └── timing.json
│   ├── iteration-2/
│   └── ...
├── feedback.json                               # user feedback from viewer
├── grade_iter<N>.py                            # grading scripts (if any)
└── SESSION_SUMMARY.md                          # running notes across sessions
```

**Naming conventions:**
- Eval directories use `eval-<id>-<descriptive-name>` (not just `eval-0`).
- Baseline dir is `without_skill/` for new skills, `old_skill/` for
  improvements.
- Iteration dirs are `iteration-<N>/`, incrementing each loop.

## SESSION_SUMMARY.md

Keep `.local/SESSION_SUMMARY.md` updated across sessions. It is the handoff
document — a new session reads it to pick up where the last one left off.
Include: what's being worked on, workspace locations, what each iteration
found, changes applied, and explicit next steps.

## Description optimization (optional, last step)

After the skill body is finalized, optimize the `description` frontmatter for
triggering accuracy:

1. Generate ~20 trigger queries (8-10 should-trigger, 8-10 near-miss
   negatives — realistic, concrete, some that never name the skill). Save to
   `.local/.<skill>-trigger-eval.json` as
   `[{"query": "...", "should_trigger": true|false}]`.
2. Review the query set with the user before testing.
3. Test candidate descriptions: spawn a fresh subagent per query holding
   only the skill's frontmatter (3 runs per query) and count the trigger
   rate. Split queries 60/40 train/test; pick the winner by test score.
4. Apply the winning description to the frontmatter; show the user
   before/after with scores.

See `~/.config/devin/skills/skill-generator/references/harnesses.md` for the
full procedure.

## Key paths

| Item | Path |
|------|------|
| Skills (repo) | `skills/<name>/SKILL.md` |
| Iteration artifacts | `.local/` (gitignored) |
| skill-generator | `~/.config/devin/skills/skill-generator/` |
| benchmark aggregator | `~/.config/devin/skills/skill-generator/scripts/aggregate_benchmark.py` |
| eval viewer generator | `~/.config/devin/skills/skill-generator/scripts/make_review.py` |
| validate / package | `~/.config/devin/skills/skill-generator/scripts/{quick_validate,package_skill}.py` |
| eval schema reference | `~/.config/devin/skills/skill-generator/references/evals.md` |
| harness + trigger-opt notes | `~/.config/devin/skills/skill-generator/references/harnesses.md` |
