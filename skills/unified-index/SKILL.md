---
name: unified-index
version: 1.0.0
description: Consolidates everything searchable in a repository — documentation files, source code files (with their symbols), AI-generated comments (inline AI-marked comments, AI review artifacts, AI chat/session exports), and TODOs (inline TODO/FIXME/HACK markers plus standalone todo files) — into a single markdown document with a main index table so anything can be found in seconds. Trigger whenever the user asks to unify, consolidate, index, merge, or gather "all docs", "all code", "all comments", "all TODOs", "all AI feedback", or "everything" into one searchable file, e.g. "consolidate all docs, code, comments and TODOs into one document", "build one index of the whole repo", "give me a single file with everything I should search".
---

# Unified Index

Build a single markdown document that consolidates everything worth
searching in a repository: **documentation**, **source code**, **AI-generated
comments**, and **TODOs**. A main index table at the top makes every entry
reachable in seconds — the user reads one file instead of hunting through
dozens.

The output is a durable, searchable artifact. Speed of *finding* is the
point: the index must be skimmable, every entry must be reachable from
it, and the layout must be stable so the user learns it once.

## What gets consolidated

Four kinds of entries, with distinct ID prefixes:

- **Docs** (`D001`, `D002`, ...) — documentation files: `README*`,
  `docs/**`, and any `*.md` / `*.mdx` in the repo. Full content included,
  one section per document.
- **Code** (`K001`, `K002`, ...) — source and config files by extension:
  python, js/ts, go, rust, java, c/c++, ruby, php, shell, plus
  json/yaml/toml/ini/env configs. Each file gets an entry with its
  language, a one-line purpose, and its top-level symbols (classes and
  functions with line numbers) so code is findable by name. Minified
  files and lockfiles are skipped.
- **AI comments** (`C001`, `C002`, ...) — inline comments carrying an AI
  marker (`AI:`, `AI!`, `AI?`, `Claude:`, `GPT:`, `Copilot:`, `LLM:`,
  `TODO(AI)`, `FIXME(AI)`, ...), AI review artifacts
  (`.ai-reviews/`, `.ai-review/`, `reviews/ai/`, names containing
  `ai-review`), and AI session exports (`*.chat.md`, `*.session.md`,
  `*.ai-session.md`, or files with an `<!-- ai-session -->` marker).
- **TODOs** (`T001`, `T002`, ...) — inline `TODO:`, `FIXME:`, `HACK:`,
  `XXX:` markers in any file (record file:line), plus standalone todo
  files (`TODO.md`, `TASKS.md`, `BACKLOG.md`, `ROADMAP.md`, `tasks/`,
  `todo/`).

Precedence: review artifacts and session exports are **AI comment**
sources, never docs, even though they are markdown. The output document
itself is always excluded from discovery.

## Workflow

1. **Discover.** Scan the repo for the four source types (exact patterns
   in `references/format.md`). Respect config if present. Always skip the
   output document, git internals, dependency and build directories.
2. **Extract.** Turn each source into an entry with: type, verbatim
   text, source path, line number where applicable, and derived status.
   For code entries, also record language and top-level symbols.
3. **Categorize & tag.** Assign a category per entry type (AI taxonomy in
   `references/format.md`; TODOs get bug/feature/refactor/cleanup/...;
   code category is its language). Attach 2–5 tags: type, category, file
   basename, salient keywords.
4. **Build the document.** Assemble: title + metadata header, main index
   table (one row per entry, linking to its anchor), one section per
   entry grouped by type (Docs with full content, Code with language and
   symbols, AI comments verbatim, TODOs with text), and a tag index.
   Exact template in `references/format.md`.
5. **Save and report.** Write to the output path (default `INDEX.md` at
   the repo root) and report: entry counts per type, sources scanned,
   and the output location.

## Document rules

- **Regenerate, don't append.** Re-running overwrites the whole document
  — deterministic, no duplicates.
- **Stable ordering.** Entries sorted by type (Docs → AI comments →
  TODOs), then category order, then source path, then line number, so IDs
  stay stable across runs.
- **Verbatim content.** Docs keep their full original markdown; comments
  and TODOs keep their exact wording. Never paraphrase or editorialize.
- **Every entry reachable.** Every index row links to its section anchor.
  No orphans.
- **Metadata header.** Generation date, per-type counts, total entries,
  and number of files scanned, so the user knows how fresh it is.

## Status

- **AI comments:** `resolved` if the text contains a resolution marker
  (`[x]`, `FIXED:`, `RESOLVED:`, `DONE:`, `CLOSED:`, `WONTFIX:`,
  `WON'T FIX`); otherwise `open`. Per-comment status fields in review
  artifacts win over the heuristic.
- **TODOs:** `done` if the line is a checked checkbox (`- [x]`) or
  contains `DONE:`/`CLOSED:`; otherwise `open`.
- **Docs:** status column is `—`.
- **Code:** status column is `—`.

Support an optional `.ai-comments/status.json` mapping entry IDs to
`open` / `resolved` / `done` / `wontfix`; merge it last so the user can
keep the document honest without editing generated content. Preserve
unknown values as `other` rather than failing.

## Configuration

Works with zero config. Optional `.ai-comments.json` at the repo root:

```json
{
  "output": "INDEX.md",
  "markers": ["AI:", "AI!", "AI?", "Claude:", "GPT:", "Copilot:", "LLM:"],
  "reviewDirs": [".ai-reviews", ".ai-review", "reviews/ai"],
  "sessionGlobs": ["*.chat.md", "*.session.md", "*.ai-session.md"],
  "todoGlobs": ["TODO.md", "TASKS.md", "BACKLOG.md", "ROADMAP.md"],
  "docGlobs": ["**/*.md", "**/*.mdx", "README*", "docs/**"],
  "codeExtensions": [".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".rb", ".php", ".swift", ".kt", ".sh", ".json", ".yaml", ".yml", ".toml", ".ini", ".env"],
  "codeIgnore": ["**/*.min.js", "**/*-lock.json", "**/Cargo.lock", "**/poetry.lock", "**/yarn.lock", "**/vendor/**"],
  "extraFiles": [],
  "excludeDirs": [".git", "node_modules", "dist", "build", ".local"],
  "maxCommentLength": 500
}
```

`extraFiles` adds files the heuristics miss. On malformed config, fall
back to defaults and say so.

## Reference files (load on demand)

- Need exact discovery patterns, the category taxonomies, the document
  template, or the language comment-syntax table →
  `references/format.md`
