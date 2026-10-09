---
name: dev-companion
version: 1.3.0
description: Command-based development companion for repository style setup, minimal implementation, code review, and plain-English explanations. Use for coding help or `/dev-companion init|implement|review|explain`. Implementation and review support lite/full/ultra minimal-coding modes; TDD is opt-in.
---

# Dev Companion

| Command | Workflow |
|---|---|
| `/dev-companion init` | `references/init.md` |
| `/dev-companion implement [lite|full|ultra]` | `references/init.md` → `references/implement.md` + `references/minimal-coding.md` |
| `/dev-companion review [lite|full|ultra]` | `references/review.md` + `references/minimal-coding.md` |
| `/dev-companion explain` | `references/explain.md` |

Route unspecified coding requests to `implement`, review requests to `review`, and explanation requests to `explain`. Every implementation must run `/dev-companion init` first, then continue to `/dev-companion implement`, even when `AGENTS.md` already exists. Review and explain remain read-only and do not run init unless explicitly requested. Load only the selected command references. Minimal-coding rules and mode persistence live in `minimal-coding.md`; load `tdd.md` only for explicit TDD/test-first requests. TDD remains opt-in.
