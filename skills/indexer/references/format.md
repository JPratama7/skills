# Format, Taxonomy, and Extraction Reference

Everything the skill needs beyond the SKILL.md workflow, in one place.
Load this file when running any consolidation pass or when the user asks
for detail on how entries are classified.

## Document template

Output file layout (default `INDEX.md` at repo root):

```markdown
# Indexer

Generated: 2026-08-12 · Docs: 2 · Code: 3 · AI comments: 6 · TODOs: 4 ·
Total entries: 15 · Files scanned: 34 · Redacted: 1 (code: 1)

## Main Index

| ID | Type | Category | Status | Source | Summary | Tags |
|----|------|----------|--------|--------|---------|------|
| [D001](#d001--readmemd) | Doc | doc | — | README.md | Project overview | readme, setup |
| [K001](#k001--srcauthpy) | Code | python | — | src/auth.py | Token store and session logic | python, auth |
| [C001](#c001--sql-injection-risk) | AI | Security | open | src/auth.ts:42 | SQL injection risk | auth, sql |
| [T001](#t001--add-retry-logic) | TODO | feature | open | src/db.ts:88 | Add retry logic | db, retry |

## Docs

### D001 — README.md

> Full original markdown of README.md, verbatim.

## Code

### K001 — src/auth.py

- **Language:** python
- **Symbols:** `TokenStore` (class, L6) · `lookup` (method, L12) ·
  `fetch_user` (L22) · `refresh` (L30)
- **Tags:** `python`, `auth`, `token-store`

> Handles refresh-token storage, validation, and rotation.

## AI Comments

### C001 — SQL injection risk

- **Source:** `src/auth.ts:42` (AI:)
- **Category:** Security
- **Status:** open
- **Tags:** `auth`, `sql`

> AI: the `WHERE` clause interpolates user input directly. Use
> parameterized queries.

## TODOs

### T001 — Add retry logic

- **Source:** `src/db.ts:88`
- **Status:** open
- **Tags:** `db`, `retry`

> TODO: add retry logic with backoff for transient connection errors

## Tag Index

- `auth` → C001, K001
- `db` → T001
- `sql` → C001
```

## Main index rules

- One row per entry, sorted by type (Docs → Code → AI comments → TODOs),
  then within type by category order, then source path, then line number.
- IDs are `D001...` (docs), `K001...` (code), `C001...` (AI comments),
  `T001...` (TODOs), assigned in sorted order — stable across runs as
  long as the entry set doesn't change.
- `Summary` is the first sentence / first heading of the entry, truncated
  to ~80 chars with `…`; never the whole entry.
- `Source` is the relative path, plus `:line` for inline entries.
- The ID cell links to the entry's anchor: lowercase the heading, drop
  non-alphanumerics, join words with `-` (GitHub-style slugging).
- `Tags` are comma-separated, no backticks in the table cell.
- `Status` for docs and code entries is `—`.

## Category taxonomies

### AI comments

Assign exactly one category. Evaluate in this order — the first matching
rule wins, so security and bugs surface first:

1. **security** — injection, sql, xss, csrf, ssrf, auth, credential,
   password, secret, token, cors, oauth, encryption, owasp, leak,
   permission, sanitize, pii
2. **bug** — null, undefined, crash, error, exception, race, deadlock,
   off-by-one, edge case, infinite loop, memory leak, throws, broken,
   fails, incorrect, wrong result
3. **performance** — n+1, o(n), slow, latency, bottleneck, caching,
   cache, query count, memory, cpu, async, blocking, optimize, hot path,
   pagination
4. **architecture** — coupling, cohesion, refactor, abstraction,
   dependency, module, service, interface, design, solid, dry, layering,
   reuse, tech debt
5. **style** — naming, format, lint, style, convention, readability,
   whitespace, prettier, eslint
6. **docs** — document, comment, readme, example, typo, usage example,
   docstring, explain
7. **ux** — user, ui, accessibility, a11y, error message, button, flow,
   onboarding, screen reader
8. **question** — comment marker is `AI?`, or the text ends with `?` and
   contains no category keywords
9. **other** — anything unmatched; use sparingly

Weak single-keyword hits on a high-priority rule lose to a 3+ keyword
hit on a lower rule. When in doubt, pick the category a developer would
filter on.

### TODOs

Assign one of: **bug** (fix, incorrect, broken, error, crash), **feature**
(add, implement, support, allow, expose), **refactor** (refactor, clean,
simplify, extract, remove, deprecate, restructure), **cleanup** (delete,
tidy, dead code, unused), **question** (ends with `?` or is a "decide /
investigate / check whether" phrasing), else **other**.

### Docs

Category is always `doc`. Differentiation happens through tags (file
basename + keywords from the first heading).

### Code

Category is the file's language, lowercase: `python`, `typescript`,
`javascript`, `go`, `rust`, `java`, `c`, `cpp`, `ruby`, `php`, `shell`,
`yaml`, `json`, `toml`, `ini`. Config files are categorized by their
format (`yaml`, `json`, ...).

## Tagging rules

- Always include the type and the category as tags.
- Always include the source file basename (without extension).
- Add 1–3 salient keywords from the text (nouns, not verbs; e.g. `auth`,
  `cache`, `query-builder`), lowercased, `-`-joined.
- For docs, prefer the first heading's topic words as keywords.
- For code, add the top 1–2 symbol names as tags alongside the language.
- Drop stopwords: `the`, `a`, `this`, `should`, `use`, `need`, `make`.

## Discovery: docs

- **Defaults**: `README*`, `docs/**`, `**/*.md`, `**/*.mdx` (configurable
  via `docGlobs`).
- **Excluded**: the output document itself (so re-runs stay clean),
  review artifacts and session exports (they belong to AI comments),
  todo files (they belong to TODOs), dependency/build dirs.
- A doc entry's text is the full file content, verbatim, including
  headings and code blocks. Very large docs are still included in full —
  the summary in the index is what keeps the table skimmable.

## Discovery: code

- **Extensions** (configurable via `codeExtensions`): programming
  languages (py, js, ts, tsx, jsx, go, rs, java, c, cpp, h, rb, php,
  swift, kt, sh, ...) plus config formats (json, yaml, yml, toml, ini).
  `.env` is intentionally excluded from defaults — env files typically
  hold secrets and are covered by `sensitiveGlobs` instead.
- **Ignored** (configurable via `codeIgnore`): minified files
  (`*.min.js`), lockfiles (`*-lock.json`, `Cargo.lock`, `poetry.lock`,
  `yarn.lock`), vendored/third-party trees. Never index the output
  document or files already claimed by another type (review artifacts,
  session exports, todo files).
- **Purpose summary**: one or two sentences — prefer the module docstring
  or file-level comment; otherwise infer from the class/function names
  and top-level structure. Never invent details.
- **Symbols**: top-level declarations with their 1-based line numbers.
  Declaration patterns per language family:

  | Language family | Patterns |
  |-----------------|----------|
  | python | `class X`, `def x`, `async def x` |
  | js/ts | `class X`, `function x`, `export function x`, `const x = (`, `interface X`, `type X` |
  | go | `type X struct`, `type X interface`, `func x` |
  | rust | `struct X`, `enum X`, `trait X`, `fn x`, `impl X` |
  | java/c/cpp | `class X`, `interface X`, `enum X`, return-type+name signatures |
  | config formats | none — mark the entry as `config file, no symbols` |

  Methods inside a class are listed as `name (method, L<line>)`. Nested
  or private helpers are skipped unless they are the only content.
- Config entries carry no symbols line; the summary comes from the file's
  top-level keys (e.g. "Server ports and feature flags").

## Discovery: AI comments

### Inline code comments

- **Marker detection** (configurable via `markers`): a comment starting
  with `AI:`, `AI!`, `AI?`, `Claude:`, `GPT:`, `Copilot:`, `LLM:`, or
  containing `TODO(AI)`, `FIXME(AI)`, `HACK(AI)`. Match case-insensitively
  after the comment token.
- **Comment syntaxes** to strip per language family:

  | Syntax | Languages |
  |--------|-----------|
  | `//` | js, ts, go, rust, java, c, c++, swift, php |
  | `#` | python, ruby, shell, yaml, toml, makefile, dockerfile |
  | `--` | sql, haskell, lua |
  | `/* ... */` | js, ts, go, rust, java, c, c++, css, sql |
  | `<!-- ... -->` | html, xml, svg, vue |
  | `;` | lisp, clojure, scheme |

- Record the 1-based line number of the comment's first line. Multi-line
  block comments become one record with the first line number.
- The originating tool is the marker word (`Claude:`, `GPT:`, ...); show
  it in parentheses after the source path.

### Review artifacts

- **Directories** (default): `.ai-reviews/`, `.ai-review/`, `reviews/ai/`.
- **Files**: any name containing `ai-review` / `ai_review`, plus markdown
  and JSON files inside the review directories.
- **Markdown**: each list item or blockquote that reads as a finding
  (contains a file path, a severity word like `critical`/`warning`/`nit`,
  or an actionable sentence) becomes one comment. Skip headers,
  navigation, template text.
- **JSON**: flatten common shapes defensively — arrays of objects with
  `file`/`path` + `comment`/`message`/`text` (+ optional `line`,
  `severity`, `status`). For unrecognizable shapes, extract string values
  containing paths or keywords rather than failing. Never throw.
- **Status**: honor per-comment `status`/`state` fields when present.

### AI session exports

- **Matching** (default globs): `*.chat.md`, `*.session.md`,
  `*.ai-session.md`, or any file containing `<!-- ai-session -->`.
- Each user/AI exchange is one comment: the AI response (or the Q + A
  pair) is the text. Prefix the source with the exchange index, e.g.
  `notes/session-1.chat.md (exchange 3)`.
- Raw logs with message-type markers (`## User`, `## Assistant`,
  `human:`, `assistant:`) split on those markers.

## Discovery: TODOs

- **Inline markers** — in any file, lines containing `TODO:`, `FIXME:`,
  `HACK:`, `XXX:` (case-insensitive). Record file:line. The entry text is
  the marker plus the rest of the line (multi-line comments: include
  continuation lines until the comment block ends).
- **Standalone todo files** (configurable via `todoGlobs`) — `TODO.md`,
  `TASKS.md`, `BACKLOG.md`, `ROADMAP.md`, and files under `tasks/` or
  `todo/`. Each checklist line (`- [ ]` / `- [x]` / `* item`) or numbered
  item becomes one TODO entry. Heading text can serve as the summary.
- **Status**: checkbox `- [x]` or `DONE:`/`CLOSED:` in the text → `done`;
  otherwise `open`.

## Status overrides

Optional `.ai-comments/status.json`:

```json
{ "C003": "resolved", "T002": "done", "C007": "wontfix" }
```

Merged after heuristic status derivation; unknown IDs and unknown status
values are preserved as-is (render as `other`) rather than dropped, so the
user's file is never silently mangled.

## Config precedence

`extraFiles` are appended to the source set after discovery. `excludeDirs`
apply to every discovery pass. `sensitiveGlobs` apply to every discovery
pass and to `extraFiles` — a file matching a sensitive glob is refused
from `extraFiles` unless `allowSensitive: true` is set. If
`.ai-comments.json` is malformed, log a warning, use defaults, and
continue — a config typo must not block the consolidation.

## Secret redaction

Two layers: file-level skips (`sensitiveGlobs`) and inline value
detection (this section). Both always run. See SKILL.md § Secret
redaction for the policy; this section is the pattern reference.

### File-level skips

Default `sensitiveGlobs` (configurable, but cannot be emptied — only
extended):

```
**/.env
**/.env.*
**/*.pem
**/*.key
**/*.p12
**/*.pfx
**/id_rsa*
**/id_ed25519*
**/.aws/**
**/.ssh/**
**/credentials
**/secrets/**
```

Files matching these are never discovered, never read, never appear in
the output. The report counts them under `Files skipped (sensitive)` —
not under `Files scanned`. A file in `extraFiles` that matches a
sensitive glob is refused with a warning naming the glob that matched
(not the file's contents), unless `allowSensitive: true` is set
explicitly in config.

### Inline value patterns

After extraction, scan every entry's verbatim text for these patterns.
On any match, drop the whole entry from the index and increment the
per-type `redacted` counter. Do not redact in place — drop the entry.
Never record the dropped entry's source path in the report.

Patterns (case-insensitive where noted; match against the full verbatim
text of the entry):

| Name | Pattern | Notes |
|------|---------|-------|
| AWS access key ID | `AKIA[0-9A-Z]{16}` | case-sensitive |
| AWS secret assignment | `aws_secret_access_key\s*[:=]\s*\S+` | case-insensitive |
| GitHub PAT | `gh[pousr]_[A-Za-z0-9]{36,}` | |
| GitHub fine-grained | `github_pat_[A-Za-z0-9_]{82}` | |
| GitLab PAT | `glpat-[A-Za-z0-9_-]{20}` | |
| Slack token | `xox[abp]-[A-Za-z0-9-]+` | |
| Google API key | `AIza[0-9A-Za-z_-]{35}` | |
| JWT | `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` | three-part dot-delimited |
| Private key block | `-----BEGIN [A-Z ]*PRIVATE KEY-----` | covers RSA, EC, OPENSSH, PGP, etc. |
| Generic credential assignment | `(password\|passwd\|pwd\|token\|api_key\|apikey\|secret\|access_key\|private_key)\s*[:=]\s*["']?[^\s"']{8,}` | case-insensitive; min 8-char value |
| High-entropy with context | `[A-Za-z0-9_-]{32,}` within 50 chars of a key name matching `token\|key\|secret\|password\|cred` | heuristic; higher false-positive rate, acceptable per policy |

The generic-assignment and high-entropy rules are the broadest. They
will catch most real leaks and some false positives. Per SKILL.md
policy, false positives are acceptable — dropping a non-secret entry is
a nuisance, leaking a real secret is a breach. Users blocked by a false
positive can add the offending file to `excludeDirs` and re-run, or
report it for pattern tuning.

### Report format

The save-and-report step (SKILL.md workflow step 6) emits one
redaction line:

```
Redacted: <total> (docs: <n>, code: <n>, ai-comments: <n>, todos: <n>)
```

The metadata header in the output document carries the same counts
compactly (see the document template above). No source paths, no
matched values, no pattern names — counts only.
