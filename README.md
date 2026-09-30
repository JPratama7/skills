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

## Skills

- `writing-coach` — critique blog posts and technical articles
- `discussion` — challenge assumptions and test decisions before you commit
- `skill-generator` — create, evaluate, iterate, and package agent skills for any harness
- `graph-decompose` — decompose a task into a DAG of parallel-executable graph nodes (JSON + Mermaid plan only)
- `graph-execute` — execute a `graph-decompose` plan by walking its DAG in waves: parallel node spawn, dep-respecting, verify-before-fan-out, stop-on-failure
- `planning` — plan tasks in three modes: coding, personal/task, agile sprint; plan only
- `agent-handoff` — pass work from one agent to another without losing context (subagent→parent, parent→subagent, peer, chained)
- `brainstorming` — probe, diverge, converge: turn a vague idea into a chosen direction and artifact (PRD, system design, one-pager)
- `subagent-manager` — when to delegate, how to brief, parallel launch, verify-before-integrate (harness-agnostic)
- `doc-builder` — interview-driven docs: root cause analyses, reports, requirements docs, decision records, Jira/GitHub tickets, PR descriptions
- `git-commit` — stage and commit working-tree changes; secret screening, convention-matched messages, per-VCS command references
- `devops` — deploy and operate apps: deploy-path routing (Docker/compose, Railway, Fly.io, Cloud Run, ECS, Kubernetes, VPS, static hosts), CI/CD pipelines, secrets and environments, health checks and observability
- `layman` — plain-English mode: jargon translated to everyday words, code and commands kept exact; lite/full/ultra intensity levels
- `research` — Graph-of-Thought research: decomposes questions into sub-questions, runs parallel research agents, scores and prunes branches; ships a cited markdown report
- `indexer` — index everything searchable in a repo (docs, code + symbols, AI-marked comments/review artifacts, TODOs) into a single markdown document
- `active-recall` — build spaced-repetition flashcard decks from source material and run in-chat review sessions; deterministic SM-2 scheduler script (init/add/lint/due/grade/export), atomic-card design rules, exports for Anki, Obsidian SR, Mochi, and plain markdown
