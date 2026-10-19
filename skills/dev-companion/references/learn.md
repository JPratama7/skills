# `/dev-companion learn`

Activate learning mode in the main conversation. Read [learn-behavior.md](learn-behavior.md)
and follow it throughout normal development, not just during this command. The learner owns
the design. Ask for their approach and wait. Keep guidance minimal: give concise feedback on
their reasoning and explain unfamiliar concepts as needed. Offer possible approaches only when
they ask for help or are stuck, then return the decisions to them. Learning and learner control
take priority over build speed. An ordinary build request in this mode retains that loop; only
an explicit request to skip or pause bypasses it. Do not switch to a subagent or require manual
coding by default.

Read the guide files with a file-reading tool instead of printing them with a shell command such
as `cat`. Use a glob or file-search tool to discover optional learner-state files before reading
them. A missing `.dev-companion/` directory is normal first-time setup, not an error. If a shell
check is necessary, handle absence with an explicit conditional that succeeds; don't run `ls` on
a possibly missing directory or hide actual read failures. Keep guide reads separate from optional
state checks so a missing file doesn't make a successful instruction read look like a failed tool
call.

## Locate state

Starting at the current working directory, look upward for `.dev-companion/`, stopping at the
nearest `.git` directory or file (including a worktree root). Use the nearest one within that
boundary. Without Git, check only the current directory; don't search its parents. If there is
none, create `.dev-companion/` at the Git root, or current directory without Git. Do not use
state from a parent repository, another worktree, or the installed skill folder. Do not follow
symlinked state directories or files; explain the issue instead.

`.dev-companion/` is persistent state only. Scratch files (generated exercises,
one-off diagnostics) go in `/tmp/` so they don't accumulate on disk.

If `profile.md` exists, read it and `project-map.md`. Search the entire `progress.md` for pending
decisions, then read their complete sections and other topics relevant to the task. An initial
excerpt is not evidence that nothing is pending. Resume without repeating completed onboarding or
bypassing a pending Design or Implementation checkpoint. Set `Learning mode: active` if the user
is resuming paused learning. If onboarding is incomplete, ask only the unanswered questions.
Missing companion files can be recreated from evidence; never invent learning history or
overwrite existing notes.

If no profile exists, read [learn-onboarding.md](learn-onboarding.md) and run onboarding. Use
[learn-state-templates.md](learn-state-templates.md) when creating state. These files are local
Markdown maintained with normal file tools; there is no service to call.

After setup, continue the user's build task. If none was provided, ask what they want to build or
change. Invoking `/dev-companion learn` again should not reset anything.

## Implementation

After the learner chooses **Implement this step**, run `/dev-companion init` first (it is
idempotent), then write the agreed code following `minimal-coding.md` at the active level. Report
any `AGENTS.md` changes in the Implementation report.

## Harness notes

- If no native question picker exists, ask one plain-text question with its options listed, then end the turn and wait.
- No session hook restores learning mode. `SKILL.md` routes unspecified coding requests to learn while the profile says `Learning mode: active`; `/dev-companion learn` resumes it explicitly. After context compaction, search `progress.md` for a pending decision before acting.
- Present each checkpoint or question once, at the end of the reply, with its options beneath it. Don't restate it in a separate message.

## Third-party notice

Portions of this command's guidance are third-party work under the following license:

MIT License

Copyright (c) 2026 Noah Kim

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
