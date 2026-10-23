---
name: cross-skill-memory
version: 1.0.0
description: Shared persistent configuration for every installed skill. One
  JSON store at `.memory/memory.json` lets each skill keep configuration and
  state that survives sessions and is visible to other skills. Use whenever
  the user mentions "memory", "persistent config", "skill configuration",
  "remember my preferences", "make it stick", or ".memory/memory.json"; also
  trigger when a skill needs to read or write shared state (learner profile,
  delegation lessons, default model, layman intensity, plan dirs).
---

# Cross-Skill Memory

One JSON file, every skill. Each skill writes its own namespace; everyone
reads the `shared` section. The store is convention, not platform — no
harness provides cross-skill memory, so the file is the contract.

## The store

```
<project-root>/.memory/memory.json     # gitignored runtime state
```

- Project root = the repo root of the working directory (or the working dir
  when there's no repo). Never `/tmp/` — memory must survive reboots.
- Gitignore `.memory/` — it is runtime state, never committed.
- The file is small by design: configuration and pointers, not bulky state.
  Decks, checkpoints, and engagement logs stay in their skill's existing
  dot-folder; the store holds the config and the cross-skill glue.

## Schema

```json
{
  "version": 1,
  "shared": {
    "user_prefs": {},
    "lessons": [],
    "conventions": {}
  },
  "<skill-name>": {}
}
```

- `version` — schema version; currently 1.
- `shared.user_prefs` — preferences any skill may read (output style,
  default model, language). Set once; every skill sees them.
- `shared.lessons` — cross-skill lessons, one object per lesson
  (`{"what": ..., "do_this": ...}`). Skills append; all skills read.
- `shared.conventions` — repo-wide conventions the user has confirmed.
- `<skill-name>` — one object per skill, holding that skill's persistent
  config and state. Key = the skill's `name` from frontmatter.

## Read/write rules

- **Read at entry.** When a skill starts, read the whole file (it is small):
  your namespace plus `shared`. Missing file = defaults; create on first
  write.
- **Write at exit, own namespace only.** Update your key; never rewrite
  another skill's object. Touch `shared` only when the change IS a shared
  lesson or preference.
- **Atomic writes.** Write `memory.json.tmp` then rename over `memory.json`
  — a crash mid-write must not corrupt the store.
- **No locks.** Agents are serialized in practice; read-modify-write and move
  on. If the file changed under you, re-read and merge before writing.
- **Malformed store.** Report it, back it up as `memory.json.broken-<ts>`,
  and start fresh — never silently overwrite.

## Namespace registry

Every skill documents its namespace in its own SKILL.md ("Memory" section).
Keep this table in sync when skills change:

| Skill | Stores |
|---|---|
| active-recall | last deck, default export formats |
| agent-handoff | handoff dir override |
| brainstorming | preferred frameworks, default artifact |
| dev-companion | repo conventions summary, learning mode |
| devops | preferred platform/cloud |
| discussion | none today — calibrates per decision |
| doc-builder | default save dir |
| git-commit | message style override |
| graph-decompose | default granularity, plan dir |
| graph-execute | none today |
| indexer | output override (repo config stays in `.ai-comments.json`) |
| layman | intensity (persists across sessions) |
| learn-companion | active subject, profile dir |
| pentest-toolkit | engagement dir, current engagement |
| planning | plan dir |
| research | default mode/depth, report dir |
| skill-generator | target harness, generator/evaluator models |
| subagent-manager | default model, max parallel (lessons live in `shared.lessons`) |
| writing-coach | recurring issues across sessions |

## Adding memory to a new skill

1. Pick a namespace = the skill's `name`.
2. Add a short "Memory" section to the skill's SKILL.md: what it stores,
   defaults, and a pointer to this protocol.
3. Register the namespace in the table above.

## Hard rules

- The store never holds secrets — credentials belong in the harness secret
  store, not JSON.
- Never commit `.memory/`. It is runtime state.
- Keep entries small and typed; no nested essays.
- Cross-skill state (lessons, prefs) goes in `shared`; skill-private state in
  the skill's namespace.