---
name: learn-companion
version: 2.1.0
description: Evidence-based learning and teaching companion — guarded tutoring, retrieval practice, spaced review, diagnostics for self-studied material, learning grounded in the user's own PDFs/slides/notes, and learner-owned reasoning with a default-on Feynman teach-back gate; plus teacher-side workflows for the course lifecycle (design, materials, assessment, delivery, reflection). Use when the user wants to learn, study, understand, or practice a topic; says "teach me", "help me learn", "study", "quiz me", "test what I learned", "learn from these PDFs/slides/notes", "feynman", "teach it back", or invokes `/learn-companion init|plan|study|quiz|review|self-learn|mentor|deliver`. Also for teacher requests: "design a course", "syllabus", "lesson plan", "write an exam", "build a rubric", "grade or audit submissions", "student feedback", "recommendation letter", "teaching portfolio", "slide deck", "lab assignment", "accreditation", "TA coordination".
---

# Learn Companion

| Command | Workflow |
|---|---|
| `/learn-companion init` | `references/init.md` → `references/onboarding.md` + `references/state.md` |
| `/learn-companion plan` | `references/plan.md` |
| `/learn-companion study` | `references/study.md` |
| `/learn-companion quiz` | `references/quiz.md` |
| `/learn-companion review` | `references/review.md` |
| `/learn-companion self-learn` | `references/self-learn.md` |
| `/learn-companion mentor` | `references/mentor.md` |
| `/learn-companion deliver` | `references/deliver.md` |

Learner requests also load `references/pedagogy.md`; teacher requests load
`references/pedagogy-teaching.md` and run the command file's "Teacher
side" section instead. Load `pedagogy.md` whenever learning mode is
active; `onboarding.md` and `state.md` only for onboarding or state
creation.

| Trigger | Also load |
|---|---|
| Learner supplies their own materials — PDFs, slides, docs, webpage exports, pasted notes — to learn from | `references/materials.md` |
| Generating learning-content files, citing sources, or high-stakes / fast-moving subjects | `references/reliability.md` |

Route unspecified learning requests ("teach me X", "help me understand Y", "let's study Z") to `study` once a learner profile exists, and to `init` when none does. Route "I studied/learned X on my own — test me" requests to `self-learn`. Requests phrased as teach-back ("feynman", "teach it back", "explain it back to you", "let me teach you X") go to `study` with the teach-back pass up front. Learning mode is active when the nearest `.learn-companion/profile.md` says `Learning mode: active` or learning was activated earlier in this conversation. Plain factual questions need no mode activation — answer them directly.

## Teacher-side routing

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
