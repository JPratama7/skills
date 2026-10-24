# skills

Agent skills installable via the [skills CLI](https://github.com/vercel-labs/skills).

## Install

```bash
npx skills add ./skills
# or once published:
npx skills add <owner>/skills
```

Claude Code plugins live in `.claude-plugin/plugin.json`. Load them all for a session with:

```bash
claude --plugin-dir ./skills
```

## Shared configuration and memory

Every skill in this collection keeps its persistent configuration in **one
shared JSON store**: `.memory/memory.json` at the project root. It is
gitignored runtime state — never committed — and it survives restarts, so a
skill's settings carry across sessions and are visible to every other skill.

```json
{
  "version": 1,
  "shared": {
    "user_prefs":   { "output_style": "telegraphic" },
    "lessons":      [ { "what": "delegation briefs need an output contract", "do_this": "always name the return shape" } ],
    "conventions":  {}
  },
  "layman":     { "intensity": "ultra" },
  "research":   { "default_depth": "standard" },
  "subagent-manager": { "model": "fast", "max_parallel": 3 }
}
```

- `shared.user_prefs` / `lessons` / `conventions` — cross-skill state any
  skill may read (preferences, delegation lessons, confirmed conventions).
- `<skill-name>` — one object per skill with its own persistent config and
  state (e.g. layman's intensity now persists across sessions).
- Skills read the store at entry, write their own namespace at exit, and
  never touch another skill's section. Writes are atomic (tmp + rename).

Bulky state (flashcard decks, research checkpoints, engagement logs) stays in
each skill's own dot-folder; the store holds configuration and cross-skill
glue. The full protocol — read/write rules, namespace registry, adding a new
skill — lives in the `cross-skill-memory` skill.

## Skills

- `cross-skill-memory` — one shared JSON store (`.memory/memory.json`) for persistent configuration across every skill; each skill gets its own namespace plus a shared `user_prefs` / `lessons` / `conventions` section
- `writing-coach` — critique blog posts and technical articles
- `discussion` — challenge assumptions and stress-test decisions before you commit; first-principles teardown mode (facts vs assumptions, rebuild from fundamentals)
- `skill-generator` — create, evaluate, and refine agent skills
- `graph-decompose` — break a task into a DAG of parallel-executable nodes (outputs JSON + Mermaid plan)
- `graph-execute` — walk a `graph-decompose` DAG in waves: spawn in parallel, respect deps, verify each wave, stop on failure
- `planning` — plan tasks in coding, personal/task, or agile sprint mode; 80/20 Pareto lens for prioritization and standalone "what's the 20% that matters" asks
- `agent-handoff` — transfer work between agents without losing context
- `brainstorming` — take a vague idea and narrow it down into a chosen direction (PRD, system design, one-pager)
- `subagent-manager` — delegate to subagents: briefing, parallel launch, verify before integrate
- `doc-builder` — produce docs via interview: RCAs, reports, requirements, decision records, Jira/GitHub tickets, PR descriptions; anti-AI-slop style rules + a deterministic pre-delivery checker; RCAs are rendered from a typed draft and validated by a structural and judgment checker
- `git-commit` — stage and commit with secret screening, conventional message formatting, and VCS-specific guidance
- `devops` — deploy and operate apps across Docker, Railway, Fly.io, Cloud Run, ECS, Kubernetes, VPS, and static hosts; CI/CD, secrets, health checks, observability
- `layman` — explain jargon in plain English, keep code and commands exact; lite, full, or ultra mode; ELI5 (smart-adult audience, one idea at a time) and first-principles explanation modes (decision teardowns route to `discussion`)
- `dev-companion` — `/dev-companion init|implement|review|explain|learn`; evidence-based repository conventions, minimal coding, plain-English explanations, lite/full/ultra modes, and learner-led development
- `research` — break questions apart, research in parallel, combine findings into a cited markdown report
- `indexer` — scan a repo for docs, code, symbols, comments, reviews, and TODOs, merge into one searchable file
- `active-recall` — build spaced-repetition flashcard decks from source material; deterministic SM-2 scheduler; export to Anki, Obsidian SR, Mochi, or plain markdown; sticky-notes mode for key-fact distillation
- `pentest-toolkit` — full offensive and defensive security toolkit: pentest, web/API/AD/cloud/mobile exploitation, privesc, password attacks, reverse engineering, code audit, AI security, DFIR, threat hunting, detection engineering, plus a 151-tool red team catalog by ATT&CK tactic; domain playbooks in `references/`
- `learn-companion` — `/learn-companion init|plan|study|quiz|review|self-learn`; evidence-grounded tutoring for any subject: attempt-first (guarded) tutoring, retrieval practice, spaced review, mastery gates with a default-on Feynman teach-back pass, diagnostics for self-studied material, persistent learner state
