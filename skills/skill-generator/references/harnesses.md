# Harness Adaptation and Description Optimization

## Harness capabilities

The workflow is identical everywhere; only these mechanics differ. Detect at
runtime rather than assuming — capability beats naming.

| Harness | Subagents | Viewer | Install path | Packaging |
|---------|-----------|--------|--------------|-----------|
| Claude Code | yes | server or `--static` | `~/.claude/skills/` or repo `skills/` | `.skill` zip or dir |
| Claude.ai | no | none | upload / paste | `.skill` zip |
| Cowork | yes | `--static` HTML | same as Claude Code | `.skill` zip |
| Devin | yes | browser preview | `.devin/skills/<name>/` or `.agents/skills/<name>/` | copy directory |
| Vercel skills CLI | no | none | `npx skills add <dir-or-owner>/<repo>` | dir with SKILL.md |
| Custom | ? | ? | per harness docs | ship the folder; zip only if required |

Rules of thumb:

- No subagents → inline runs, skip baselines (see SKILL.md step 4).
- No filesystem → evals are limited to what the model can produce in chat;
  rely on human review.
- Install = copy the skill folder (minus evals/scratch) to the harness's
  skill path. Use `scripts/package_skill.py` only when the target harness
  consumes `.skill` zips.

## Packaging

```bash
python SG/scripts/quick_validate.py <skill-dir>     # frontmatter + naming checks
python SG/scripts/package_skill.py <skill-dir> -o <output-dir>   # -> <name>.skill zip
```

`package_skill.py` validates first and excludes `evals/`, caches, and
`.local/` from the zip.

## Description optimization

The frontmatter `description` is the primary trigger. Optimize only after the
skill body is solid.

**1. Generate ~20 trigger queries** and save as JSON:

```json
[
  {"query": "realistic user prompt with concrete context", "should_trigger": true},
  {"query": "near-miss prompt that shares keywords but needs a different workflow", "should_trigger": false}
]
```

- Should-trigger: varied phrasings of the intent, including prompts that
  never name the skill; mix lengths, typos, casual phrasing.
- Negatives: near-misses. Bad negative: "write a fibonacci function" (tests
  nothing). Good negative: mentions the skill's domain but actually needs a
  different workflow or a different tool entirely.

**2. Review the query set with the user** — bad queries produce bad
descriptions. Let them edit, add, remove.

**3. Test candidate descriptions.** With subagents: run each query against a
fresh agent holding only the skill's frontmatter (3 runs per query), count
trigger rate. Without: judge each query yourself against the description.
Split 60/40 train/test when optimizing; pick by test score, not train.

**4. Apply** the winning description to the frontmatter; show before/after
and the scores.
