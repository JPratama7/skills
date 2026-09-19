---
name: git-commit
version: 1.4.0
description: >
  Stage and commit working-tree changes to version control, safely. Use when
  the user says "commit this", "commit my changes", "add and commit", "check
  in these changes", "save this to git", or asks to commit/stage/checkpoint
  work — including right after you finish a coding task for them. Inspects
  the diff, stages only what belongs in the commit, writes a commit message
  that matches the repo's convention, confirms the plan, then commits. Git
  first; adapts to Mercurial, Jujutsu, and Subversion repos.
---

Commit the user's changes as a clean, single-purpose commit — nothing more,
nothing less. The two failure modes this skill exists to prevent: commits
that sweep in unrelated work or secrets, and commit messages that describe
the mechanics of the diff instead of the intent behind it.

## Detect the VCS first

Before the workflow: check the repo root for a marker directory — `.git`,
`.hg`, `.jj`, `.svn`. The workflow below is git-shaped, so git commands
fail confusingly in a non-git checkout:

- `.git` (default) — you know the commands; load `references/git.md` only
  if you need the exact syntax (e.g. the quoting-safe heredoc).
- `.hg` → load `references/mercurial.md` (same rules as git, commands differ)
- `.jj` → load `references/jujutsu.md` (no staging step — the working copy
  is itself a commit)
- `.svn` → load `references/subversion.md` (commits publish immediately, so
  the confirmation step is not optional)

No marker at all → not a repository, see *Boundaries*.

## Workflow

1. **Survey** — before touching anything: what's modified, staged, and
   untracked; what the diff changes; and the repo's message convention.
   Never commit based on file names alone. (Commands: the loaded
   reference.)

2. **Stage deliberately** — add files by path, one logical change:
   - Stage what the task touched. Leave unrelated work-in-progress out —
     a commit that mixes "fix auth bug" with "half-finished refactor" is
     unrevertable and unreviewable.
   - Untracked files: stage only if they belong in the repo. Build output,
     logs, dependency dirs, and editor droppings do not.
   - One file mixing task changes with unrelated edits → stage only the
     relevant hunks (interactive hunk staging).
   - If it's genuinely ambiguous whether a file belongs, ask.

3. **Screen for secrets** — scan the diff and untracked files for API keys,
   tokens, passwords, private keys, `.env` files, connection strings.
   Secrets never get committed, even when the user says "commit everything" —
   rotate-and-leak is not recoverable from history the way code mistakes are.
   Flag what you found, exclude it, and say so. If the user insists, get
   explicit confirmation naming the specific secret before staging it.

4. **Write the message** — apply the rules in *Commit message* below. The
   diff you surveyed is the only source of truth for what the message may
   name; the repo's history sets the format.

5. **Confirm the plan** — before committing, show the user:
   - the files to be staged, with their status (add/modify/delete)
   - anything you're leaving out and why (especially secrets)
   - the exact commit message
   Then wait for approval. No silent commits — the user owns their history.
   If no user can respond (headless run, batch job), present the plan in
   your final report and proceed, noting that confirmation was skipped.

6. **Commit and verify** — pass the message with a heredoc (quoting-safe),
   then confirm status and the last commit's stat. Report the commit hash
   and a one-line summary. (Commands: the loaded reference.)

## Commit message

Default to Conventional Commits — `<type>(<scope>): <description>` — unless
the repo's history clearly uses something else; consistency with the repo
beats the default.

- **Type** is exactly one of `feat`, `fix`, `refactor`, `perf`, `docs`,
  `test`, `build`, `ci`, `chore`, `style` — picked from the change's
  primary intent, not the file types touched (corrected logic → `fix`,
  only test files changed → `test`). `update`, `misc`, `merge` are not
  types.
- **Scope** is the affected module, derived from a file path in the diff —
  never invented. Lowercase; join nested levels with `-` (`api-user`,
  never `api/user`, `api_user`, or `apiUser`).
- **Subject**: imperative, lowercase, no trailing period, ≤50 chars. A
  diff with several unrelated changes gets the dominant one, not a list.
- **Body** when the why isn't inferable from the diff — workarounds,
  non-obvious trade-offs, reverted behavior — or when the diff is large
  (roughly 100+ changed lines), so the reader gets the change without
  scanning the stat. Keep it compact and specific: a few short lines (≤5,
  wrap at 72), what changed and why, no per-file listing, no vague filler
  (all claims grounded — see *Grounding*). Small diff with an inferable
  why → omit the body.
- **Breaking changes**: append `!` after type/scope and add a `BREAKING
  CHANGE:` footer with the migration path — only when the diff explicitly
  removes or renames a public API, changes a signature, or alters a
  config/schema format. Internal refactors and dependency bumps are not
  breaking.
- **Footers** like `Refs: #123` / `Closes: #123` only when that exact
  identifier appears verbatim in the diff or the user's request. Never
  generate or guess an issue number.
- **Grounding**: every file, symbol, endpoint, or behavior named in the
  message must appear verbatim in the diff. If you can't point to the
  line supporting a claim, drop the claim. Empty or unclassifiable diff →
  `chore: unclassifiable changes` (the one scope-less form).
- The message is the message: no commentary, code fences, or quotes
  around it — and never AI attribution or secrets inside it.

## Boundaries

- Never push, force-push, amend, rebase, reset, tag, or delete commits
  unless the user explicitly asks for that exact operation.
- Never use `git stash` to tidy the working tree — changes stashed to "get
  them out of the way" are changes the user will forget about. Leave
  unrelated changes in place and say you left them.
- Nothing to commit? Say so — don't fabricate an empty commit or commit
  files the user didn't ask about just to have something to show.
- Not a repository? Offer to run `git init` and wait for a yes.

## Reference files (load on demand)

- Git repo and need exact command syntax → `references/git.md`
- Detected `.hg` → `references/mercurial.md`
- Detected `.jj` → `references/jujutsu.md`
- Detected `.svn` → `references/subversion.md`
