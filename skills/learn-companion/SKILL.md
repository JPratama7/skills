---
name: learn-companion
version: 1.1.0
description: Evidence-based learning companion for any subject — guarded tutoring, retrieval practice, spaced review, diagnostics for self-studied material, and learner-owned reasoning. Use whenever the user wants to learn, study, understand, or practice a topic; says "teach me", "help me learn", "study", "quiz me", "review what I know", "test what I learned on my own", or invokes `/learn-companion init|plan|study|quiz|review|self-learn`.
---

# Learn Companion

| Command | Workflow |
|---|---|
| `/learn-companion init` | `references/init.md` → `references/onboarding.md` + `references/state.md` |
| `/learn-companion plan` | `references/pedagogy.md` → `references/plan.md` |
| `/learn-companion study` | `references/pedagogy.md` → `references/study.md` |
| `/learn-companion quiz` | `references/pedagogy.md` → `references/quiz.md` |
| `/learn-companion review` | `references/pedagogy.md` → `references/review.md` |
| `/learn-companion self-learn` | `references/pedagogy.md` → `references/self-learn.md` |

Route unspecified learning requests ("teach me X", "help me understand Y", "let's study Z") to `study` once a learner profile exists, and to `init` when none does. Route "I studied/learned X on my own — test me" requests to `self-learn`. Learning mode is active when the nearest `.learn-companion/profile.md` says `Learning mode: active` or learning was activated earlier in this conversation. Load `pedagogy.md` whenever learning mode is active; load `onboarding.md` and `state.md` only for onboarding or state creation. Plain factual questions need no mode activation — answer them directly.
