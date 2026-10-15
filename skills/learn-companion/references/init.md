# `/learn-companion init`

Activate learning mode in the main conversation and set up local learner
state. Read [pedagogy.md](pedagogy.md) and follow it throughout learning
work, not just during this command.

Read the guide files with a file-reading tool instead of printing them with
a shell command such as `cat`. Use a glob or file-search tool to discover
optional learner-state files before reading them. A missing
`.learn-companion/` directory is normal first-time setup, not an error. If a
shell check is necessary, handle absence with an explicit conditional that
succeeds; don't run `ls` on a possibly missing directory or hide actual read
failures. Keep guide reads separate from optional state checks so a missing
file doesn't make a successful instruction read look like a failed tool
call.

## Locate state

Starting at the current working directory, look upward for
`.learn-companion/`, stopping at the nearest `.git` directory or file
(including a worktree root). Use the nearest one within that boundary.
Without Git, check only the current directory; don't search its parents. If
there is none, create `.learn-companion/` at the Git root, or current
directory without Git. Do not use state from a parent repository, another
worktree, or the installed skill folder. Do not follow symlinked state
directories or files; explain the issue instead.

If `profile.md` exists, read it, `roadmap.md`, and `progress.md`. Search all
of `progress.md` for a pending decision or attempt, then read the complete
relevant topic sections. An initial excerpt is not evidence that nothing is
pending. Resume without repeating completed onboarding or bypassing a
pending Attempt or Advance checkpoint. Set `Learning mode: active` if the
learner is resuming paused learning. If onboarding is incomplete, ask only
the unanswered questions. Missing companion files can be recreated from
evidence; never invent learning history or overwrite existing notes.

If no profile exists, read [onboarding.md](onboarding.md) and run
onboarding. Use [state.md](state.md) when creating state. These files are
local Markdown maintained with normal file tools; there is no service to
call.

After setup, continue the learner's study task. If none was provided, ask
what they want to learn or review. Invoking `/learn-companion init` again
should not reset anything.

## Harness notes

- If no native question picker exists, ask one plain-text question with its
  options listed, then end the turn and wait.
- No session hook restores learning mode. `SKILL.md` routes unspecified
  learning requests to `study` while the profile says
  `Learning mode: active`; `/learn-companion init` resumes it explicitly.
  After context compaction, search `progress.md` for a pending decision
  before acting.
- Present each checkpoint or question once, at the end of the reply, with
  its options beneath it. Don't restate it in a separate message.
