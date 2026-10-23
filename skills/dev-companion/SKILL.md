---
name: dev-companion
version: 1.4.0
description: Command-based development companion for repository style setup, minimal implementation, code review, plain-English explanations, and learner-led development. Use for coding help or `/dev-companion init|implement|review|explain|learn`. Implementation and review support lite/full/ultra minimal-coding modes; TDD is opt-in.
---

# Dev Companion

| Command | Workflow |
|---|---|
| `/dev-companion init` | `references/init.md` |
| `/dev-companion implement [lite|full|ultra]` | `references/init.md` → `references/implement.md` + `references/minimal-coding.md` |
| `/dev-companion review [lite|full|ultra]` | `references/review.md` + `references/minimal-coding.md` |
| `/dev-companion explain` | `references/explain.md` |
| `/dev-companion learn` | `references/learn.md` → `references/learn-behavior.md` (plus onboarding and state-template guides when needed) |

Route unspecified coding requests to `implement`, review requests to `review`, and explanation requests to `explain`. Every implementation must run `/dev-companion init` first, then continue to `/dev-companion implement`, even when `AGENTS.md` already exists. Review and explain remain read-only and do not run init unless explicitly requested. Load only the selected command references. Minimal-coding rules and mode persistence live in `minimal-coding.md`; load `tdd.md` only for explicit TDD/test-first requests. TDD remains opt-in.

Learning mode starts only with `/dev-companion learn`. While it is active, route unspecified coding requests to `learn` instead of `implement`. It is active when the nearest learner profile says `Learning mode: active` (located as `references/learn.md` describes) or when learning was activated earlier in this conversation. An explicit `/dev-companion implement` still runs direct implementation. Learning-mode code follows learn's Implementation step, which also runs init first. Load `learn-behavior.md` whenever learning mode is active; load `learn-onboarding.md` and `learn-state-templates.md` only for onboarding or state creation.

## Memory

`.memory/memory.json` → `dev-companion`: repo conventions summary from
`/dev-companion init` and learning-mode status, shared with `learn-companion`
via the `cross-skill-memory` protocol. Learner profile files stay in
`.dev-companion/`.
