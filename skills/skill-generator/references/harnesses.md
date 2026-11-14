# Harness Adaptation & Description Optimization

Same workflow; mechanics differ. Detect at runtime — capability beats naming.

| Harness | Subagents | Viewer | Install path | Packaging |
|---------|-----------|--------|--------------|-----------|
| Claude Code | yes | server or `--static` | `~/.claude/skills/` or repo `skills/` | `.skill` zip or dir |
| Claude.ai | no | none | upload / paste | `.skill` zip |
| Cowork | yes | `--static` HTML | same as Claude Code | `.skill` zip |
| Devin | yes | browser preview | `.devin/skills/<name>/` or `.agents/skills/<name>/` | copy directory |
| Vercel skills CLI | no | none | `npx skills add <dir-or-owner>/<repo>` | dir with SKILL.md |
| Custom | ? | ? | per harness docs | ship the folder; zip only if required |

- No subagents → inline runs; skip baselines (SKILL.md step 4).
- Token/usage export differs per harness — discover before first run (`evals.md` timing.json); don't assume a harness hides them.
- No filesystem → evals limited to chat output; human review.
- Install = copy folder (minus evals/scratch) to harness path; `scripts/package_skill.py` only for `.skill` targets.

```bash
python SG/scripts/quick_validate.py <skill-dir>
python SG/scripts/package_skill.py <skill-dir> -o <output-dir>   # -> <name>.skill zip
```

`package_skill.py` validates first; excludes `evals/`, caches, `.local/`.

`description` is the primary trigger; optimize after the body is solid.

**1. ~20 queries** as JSON:

```json
[{"query": "realistic user prompt with concrete context", "should_trigger": true}, {"query": "near-miss: same keywords, other workflow", "should_trigger": false}]
```

- Varied phrasings, incl. never-name-it prompts; mix length, typos, casual phrasing.
- Negatives = near-misses: in-domain, different workflow/tool. Bad: "write a fibonacci function" (tests nothing).
- Review the query set with the user — bad queries → bad descriptions. Let them edit, add, remove.
- Test: frontmatter-only agent, 3 runs/query, count trigger rate; no subagents → judge yourself. 60/40 train/test; pick by test score, not train.
- Apply winner; show before/after, scores.
