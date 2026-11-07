---
name: learn-companion
version: 2.0.0
description: Evidence-based learning and teaching companion — guarded tutoring, retrieval practice, spaced review, diagnostics for self-studied material, and learner-owned reasoning with a default-on Feynman teach-back gate, plus teacher-side workflows covering the full course lifecycle (design, materials, assessment, delivery, reflection). Use when the user wants to learn, study, understand, or practice a topic; says "teach me", "help me learn", "study", "quiz me", "review what I know", "test what I learned on my own", "feynman", "teach it back", or invokes `/learn-companion init|plan|study|quiz|review|self-learn|mentor|deliver`. Also for teacher requests: "design a course", "syllabus", "learning outcomes", "lesson plan", "write an exam", "build a rubric", "grade or audit submissions", "student feedback", "recommendation letter", "teaching portfolio", "slide deck", "lab assignment", "lecture script", "accreditation", "TA coordination".
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
| `/learn-companion mentor` | `references/pedagogy.md` → `references/mentor.md` |
| `/learn-companion deliver` | `references/pedagogy.md` → `references/deliver.md` |

Route unspecified learning requests ("teach me X", "help me understand Y", "let's study Z") to `study` once a learner profile exists, and to `init` when none does. Route "I studied/learned X on my own — test me" requests to `self-learn`. Requests phrased as teach-back ("feynman", "teach it back", "explain it back to you", "let me teach you X") go to `study` with the teach-back pass up front. Learning mode is active when the nearest `.learn-companion/profile.md` says `Learning mode: active` or learning was activated earlier in this conversation. Load `pedagogy.md` whenever learning mode is active; load `onboarding.md` and `state.md` only for onboarding or state creation. Plain factual questions need no mode activation — answer them directly.

## Teacher-side routing

The commands are dual-purpose: learner requests run the learner workflow at
the top of each file; teacher requests (the user teaches others) run the
"Teacher side" section of the same file.

| Teacher intent | Command |
|---|---|
| Design/redesign a course, syllabus, learning outcomes, alignment audit, async conversion, program/accreditation mapping, class-readiness diagnostics | `plan` |
| Lesson plans, lecture notes, slide outlines, activities, cases, discussion guides, flipped packages, rendered decks, labs, video scripts, bilingual materials | `study` |
| Exams, quizzes, question banks, rubrics, project/group briefs, integrity audits, item/grade analysis, accommodation variants, checking submissions against a spec | `quiz` |
| Student-evaluation analysis, mid-course feedback, peer observation, teaching portfolio/statement, SoTL | `review` |
| Feedback on student work, struggling students, recommendation letters, difficult emails, office hours, advisee plans, suspected integrity cases | `mentor` |
| Whole-course pipeline, weekly delivery loop, announcements/emails, course site, LMS packaging, FAQ, TA team ops | `deliver` |

Ambiguous ("teach a class on X" vs "teach me X"): if the user delivers the
teaching, it's teacher-side. Teacher-side state is `course_passport.yaml`
(state.md); supporting templates and deep references live under
`references/assets/` (adapted from the MIT-licensed teaching-skills suite —
see `references/assets/LICENSE-teaching-skills`).

## Memory

`.memory/memory.json` → `learn-companion`: `active_subject` + `profile_dir`
(learner side, shared with `dev-companion`'s learning mode via the
`cross-skill-memory` protocol) and `active_course` (teacher side; add
`passport_path` only for passports outside `.learn-companion/`).
Profile, roadmap, and progress stay in `.learn-companion/`; course state
stays in `course_passport.yaml` there too — the store holds pointers,
not bulk. Read at entry, write at exit, own namespace only, atomic
writes.
