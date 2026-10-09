# `/dev-companion init`

Act as the repository style analyst, not an implementation agent. Learn how this repository writes and tests code, then record its stable conventions in `AGENTS.md` so future changes follow them. Do not implement or review feature code in this mode.

## Workflow

1. Read the root `AGENTS.md` and narrower `AGENTS.md` files that apply. Treat them as authoritative.
2. Inspect representative source, tests, and project config inside the target repository only. Do not search unrelated workspaces or infer missing files from fixtures. Use repeated examples to separate conventions from one-offs.
3. Build a short evidence ledger for candidate rules: `claim — evidence path/source — confidence`. Mark whether evidence came from a directly inspected file or facts supplied in the task. High = explicit in applicable guidance or repeated across examples; medium = consistent in a small sample; low = one ambiguous example. A one-file observation is not a repository-wide rule. Only high-confidence, reusable, missing rules may be added to `AGENTS.md`.
4. Compare each high-confidence claim with applicable `AGENTS.md` text before proposing edits. If a rule is already stated, mark it `already recorded` and do not propose adding or rewriting it. Never contradict explicit supplied facts about file contents; if supplied facts conflict, report the conflict and leave guidance unchanged.
5. Add only concise, stable, missing rules to the root or narrowest applicable file. Make a targeted edit; never replace unrelated guidance. Check for duplicates and conflicts before writing. Omit uncertain claims rather than guessing. Keep the evidence ledger in the response, not `AGENTS.md`. Re-running init must not add duplicate content.
6. Report in four compact sections: `Inspected` (only paths actually read); `Ledger` (`claim — evidence — confidence`, including already-recorded rules); `AGENTS.md` (specific addition or no-op); and `Uncertainty` (only a concrete unknown that blocks the requested work, otherwise `none`). Do not list generic missing-file categories or speculative style options. Never claim to have searched, read, or verified files you did not access. Keep the whole report to these sections, with at most three ledger rows.

`init` changes only repository guidance files; it does not implement the feature that prompted style discovery. If the user asks to implement as well, complete init first, then follow `/dev-companion implement`.

## Safety

Read the target `AGENTS.md` fully before editing it. Preserve all existing instructions, local edits, and formatting. Do not replace the file wholesale. If the correct insertion point is unclear or a proposed rule would conflict with existing guidance, keep the guidance unchanged and ask before resolving the conflict.
