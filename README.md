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
- `discussion` — challenge assumptions and stress-test decisions before you commit
- `skill-generator` — create, evaluate, and refine agent skills
- `graph-decompose` — break a task into a DAG of parallel-executable nodes (outputs JSON + Mermaid plan)
- `graph-execute` — walk a `graph-decompose` DAG in waves: spawn in parallel, respect deps, verify each wave, stop on failure
- `planning` — plan tasks in coding, personal/task, or agile sprint mode
- `agent-handoff` — transfer work between agents without losing context
- `brainstorming` — take a vague idea and narrow it down into a chosen direction (PRD, system design, one-pager)
- `subagent-manager` — delegate to subagents: briefing, parallel launch, verify before integrate
- `doc-builder` — produce docs via interview: RCAs, reports, requirements, decision records, Jira/GitHub tickets, PR descriptions
- `git-commit` — stage and commit with secret screening, conventional message formatting, and VCS-specific guidance
- `devops` — deploy and operate apps across Docker, Railway, Fly.io, Cloud Run, ECS, Kubernetes, VPS, and static hosts; CI/CD, secrets, health checks, observability
- `layman` — explain jargon in plain English, keep code and commands exact; lite, full, or ultra mode
- `dev-companion` — `/dev-companion init|implement|review|explain`; evidence-based repository conventions, minimal coding, plain-English explanations, and lite/full/ultra modes
- `research` — break questions apart, research in parallel, combine findings into a cited markdown report
- `indexer` — scan a repo for docs, code, symbols, comments, reviews, and TODOs, merge into one searchable file
- `active-recall` — build spaced-repetition flashcard decks from source material; deterministic SM-2 scheduler; export to Anki, Obsidian SR, Mochi, or plain markdown
