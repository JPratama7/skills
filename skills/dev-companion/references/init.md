# `/dev-companion init`

Act as the repository style analyst, not an implementation agent. Learn how this repository writes and tests code, then record its stable conventions in `AGENTS.md` so future changes follow them. Do not implement or review feature code in this mode.

## Workflow

1. Read the root `AGENTS.md` and any narrower `AGENTS.md` files that apply to the target area. Treat existing instructions as authoritative.
2. Inspect a small, representative sample of related source files, tests, and project configuration. Use enough examples to distinguish a repeated convention from a one-off choice. Check how tests are named and run.
3. Summarize only conventions supported by those examples, such as language and module style, formatting, file/test organization, naming, error handling, dependency preferences, and verification commands. Note uncertainty instead of turning it into a rule.
4. Save repo-wide rules in the root `AGENTS.md`; save local rules in the narrowest applicable `AGENTS.md`. If a file exists, append or make a targeted edit without removing or rewriting unrelated guidance. If none exists, create a concise file only when the discovered rules are likely to help future work.
5. Avoid duplicating guidance already present. Do not persist one-off decisions, generated summaries of every inspected file, speculative rules, secrets, or personal assumptions.
6. Report the files inspected, the conventions recorded, and anything that could not be confirmed.

`init` changes only repository guidance files; it does not implement the feature that prompted style discovery. If the user asks to implement as well, complete init first, then follow `/dev-companion implement`.

## Safety

Read the target `AGENTS.md` fully before editing it. Preserve all existing instructions, local edits, and formatting. Do not replace the file wholesale. If the correct insertion point is unclear or a proposed rule would conflict with existing guidance, keep the guidance unchanged and ask before resolving the conflict.
