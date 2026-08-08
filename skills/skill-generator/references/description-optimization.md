# Description Optimization

The `description` in `SKILL.md` frontmatter is the main trigger. A skill can be perfect but useless if the harness never invokes it.

## Step 1: Generate trigger eval queries

Create ~20 queries — 8–10 should-trigger, 8–10 should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Rules:

- Use realistic, concrete prompts with file paths, job context, column names, URLs, and casual phrasing.
- Mix lengths, typos, and abbreviations.
- Should-trigger: cover different phrasings of the same intent, including cases where the user does not name the skill.
- Should-not-trigger: make them near-misses — same keywords but actually a different task, or cases where another tool is more appropriate.

Bad negative: `"write a fibonacci function"` for a PDF skill — too easy, does not test anything.
Good negative: a request that mentions PDFs but actually needs a completely different workflow.

## Step 2: Review with the user

Present the eval set. Let the user edit, toggle, add, or remove queries. Bad eval queries produce bad descriptions.

## Step 3: Run the optimization loop

If the harness has a description optimizer (e.g. `claude -p` in Claude Code), run it in the background:

```bash
python -m scripts.run_loop \
  --eval-set <trigger-eval.json> \
  --skill-path <skill-folder> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

The loop should:

1. Split queries into 60% train / 40% test.
2. Run each query 3 times to measure trigger rate.
3. Propose new descriptions based on failures.
4. Re-evaluate on train and test.
5. Return `best_description`, chosen by test score.

If the harness has no optimizer, do it manually: test candidate descriptions against the query set and keep the one with the best trigger rate on held-out negatives.

## Step 4: Apply

Update the skill frontmatter with `best_description`. Show before/after and the scores.
