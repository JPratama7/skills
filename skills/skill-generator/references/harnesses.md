# Harness Adaptation

A **harness** is the agent runtime that loads and invokes skills. The core skill workflow is the same everywhere; this file covers the differences.

---

## Claude Code

- **Subagents**: yes
- **Browser / viewer**: yes
- **Install paths**: `~/.claude/skills/` or `skills/` inside a repo
- **Packaging**: `.skill` zip via `scripts/package_skill.py`
- **Description optimizer**: `claude -p` (see `references/description-optimization.md`)
- **Notes**: run with-skill and baseline in parallel. Use `eval-viewer/generate_review.py` for review; in headless mode use `--static`.

---

## Claude.ai

- **Subagents**: no
- **Browser / viewer**: limited; no local server
- **Install paths**: read-only for built-in skills; upload `.skill` files or paste `SKILL.md`
- **Packaging**: `.skill` zip
- **Description optimizer**: skip — `claude -p` is not available
- **Notes**: run test prompts inline, one at a time, following the skill yourself. Present outputs in the chat and ask for feedback. Skip baselines.

---

## Cowork

- **Subagents**: yes
- **Browser / viewer**: headless; generate a static HTML review with `--static`
- **Install paths**: same as Claude Code
- **Packaging**: `.skill` zip
- **Description optimizer**: `claude -p` works, but run it only after the skill is solid
- **Notes**: feedback is downloaded as `feedback.json` from the static viewer. Request access to the file before reading it.

---

## Devin

- **Subagents**: yes
- **Browser / viewer**: browser preview tool available
- **Install paths**: `.devin/skills/<name>/` or `.agents/skills/<name>/`
- **Packaging**: copy the skill directory to the install path; `.skill` zips are not used
- **Description optimizer**: not available as a CLI; optimize manually
- **Notes**: use Devin-specific memory rules if present. Avoid Claude-only paths in the skill body.

---

## Vercel skills CLI

- **Subagents**: no
- **Browser / viewer**: no
- **Install paths**: `npx skills add ./skills` or `npx skills add <owner>/skills`
- **Packaging**: `.skill` zip or a directory with `SKILL.md`
- **Description optimizer**: none
- **Notes**: the CLI loads skills by frontmatter. Keep the `description` self-contained and the body under the harness's context limits.

---

## Generic / custom harness

- **Subagents**: maybe
- **Browser / viewer**: maybe
- **Install paths**: follow the harness docs
- **Packaging**: at minimum, ship the skill folder; wrap in a zip if the harness expects it
- **Description optimizer**: manual unless the harness exposes one
- **Notes**: if the harness cannot run subagents, run evals inline. If it cannot serve HTML, present results as markdown and ask for feedback.
