# skills

Agent skills installable via the [skills CLI](https://github.com/vercel-labs/skills).

## Install

```bash
npx skills add ./skills
# or once published:
npx skills add <owner>/skills
```

## Skills

- `writing-coach` — guides/critiques blog post & technical article writing process
- `jira-ticket` — generate Jira ticket or PR description from compact templates
- `discussion` — technical sparring partner that pressure-tests decisions before you commit
- `skill-generator` — create, evaluate, iterate, and package agent skills for any harness
- `graph-decompose` — decompose a task into a strict DAG of atomic, parallel-executable graph nodes (JSON + Mermaid plan; plan only, does not execute)
- `graph-execute` — execute a `graph-decompose` plan by walking its DAG in waves: parallel node spawn, dep-respecting, verify-before-fan-out, stop-on-failure
- `planning` — turn any goal into a concrete, executable plan; three modes (coding, personal/task, agile sprint); plan-only
- `agent-handoff` — produce a compressed handoff brief for passing work from one agent to another (subagent→parent, parent→subagent, peer, chained) without losing context
