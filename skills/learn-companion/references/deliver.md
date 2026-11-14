# `/learn-companion deliver`

The running term: whole-course pipeline orchestration, the weekly delivery
loop, student-facing communications and packaging, and TA team operations.
Checkpoints use the teacher-side block in pedagogy-teaching.md; state lives in
`course_passport.yaml` (state.md) — a fresh session resumes from the
passport plus the stored term calendar, never from chat history.

## The pipeline

```
Stage 0 CONTEXT  → intake → passport initialized              🧑
Stage 1 DESIGN   → plan.md course-design workflow             🧑
Gate 1.5 ALIGNMENT — alignment gate; BLOCK → back to 1        ✓ + ack
Stage 2 BUILD    → study.md lesson packages, in batches the
                   professor sizes (just-in-time default)     🧑 per batch
Stage 3 ASSESS   → quiz.md instruments + integrity audit      🧑 per instrument
Gate 3.5 QUALITY — quality gate; BLOCK → back to 2/3          ✓ + ack
Stage 4 DELIVER  → the weekly loop below, all term            🧑 per cycle
Stage 5 REFLECT  → review.md eval-analysis + triangulation    🧑
Stage 6 IMPROVE  → iteration_history entry + prioritized
                   changes → next term re-enters Stage 1      🧑
```

Gates are non-skippable in pipeline mode; a BLOCK surviving 3 fix rounds
escalates to the professor as a recorded decision, not a fourth loop.
Stage order enforces *downward* only — no materials before confirmed
outcomes, no instruments before a confirmed plan — but mid-entry is
first-class: validate existing materials into the passport via the
alignment audit, never make the professor re-derive what they have.
"What's next / status" is read-only: stage, gate states, pending
confirmations, calendar position, next action. The passport lives at
`.learn-companion/course_passport.yaml` by default (init.md locate
state). A passport on disk plus a vague request → status first, never
restart on top of it. Dashboard:
`python3 assets/scripts/build_dashboard.py <passport>` → single-file
`course_dashboard.html` next to the passport — a build product, never
hand-edited.

## Weekly loop (the Monday question: "week N — what's due?")

1. ORIENT — passport + calendar: what's taught next, what's due and
   upcoming, what's already built.
2. BUILD — just-in-time lesson packages for the next unbuilt weeks within
   the professor's chosen lead time (default: next week).
3. SUPPORT — `mentor` work on demand ONLY: the pipeline never scans
   grades or attendance for struggling students — the professor brings
   the concern with the evidence. Submission spec confirmed at assignment
   release, audit at collection (`quiz.md`).
4. MIDCOURSE — offer once in the week 4–6 window; a decline is logged,
   not re-offered.
5. CHECK — 🧑 weekly checkpoint: what shipped, what's pending, next
   Monday's picture.

Calendar facts (term dates, breaks, exam weeks, deadlines) are
institutional — ask once, store, compute "what week is it?" from that
record only; never invent.

## Communications

Every date, weight, room, and policy line traces to a passport field or
explicit professor input — a gap ships as visible `[NEEDS PROFESSOR
INPUT]`, never guessed. One message, one topic; action-first; bad news
leads with the change. **Draft-only** — never sends, posts, or uploads;
each output ends with a review-and-publish-yourself note. Every draft
cross-checks shared facts against the site, syllabus, and prior comms —
drift is reported per fact, and a contradiction with the syllabus is a
BLOCK-grade flag. No surveillance framing or mechanical guilt ("many of
you still haven't…"); flag once if requested, their call wins, logged.
Accessibility by default: semantic headings, real link text, alt text,
phone-survivable tables.

Modes: `announcement` (single-topic draft) | `weekly-email` (week-N facts
+ comms-calendar check — nothing announced late) | `course-site` (static
site rendered from the passport; policy text rendered, never restated) |
`lms-package` (upload-ready structure + checklist — the skill cannot
access the LMS and says so; for an importable package run
`assets/scripts/export_lms.py --to imscc`, and render DOCX/PDF with
`render_document.py`) | `faq` (answers drafted only where the passport
answers; unanswerable questions are policy gaps routed to `plan`).
Guide: `assets/course-publisher/references/student_comms_guide.md`;
templates: `assets/course-publisher/templates/`.

## TA team

TAs are apprentice colleagues, not labor to optimize — onboarding and
calibration are teaching-the-TA, framed developmentally. The professor
owns every personnel judgment; anything evaluative about a named TA falls
under the person-affecting rule.

- **onboarding** — course-specific handbook + first-week plan: duties,
  boundaries, escalation paths. Boundary clarity is the goal — most TA
  failures are ambiguity failures (`templates/ta_handbook_template.md`).
- **calibration** — before consequential grading: anchor set (one
  clear-high, one clear-low, two borderline — the borderlines do the
  teaching) → independent scores → reveal → discuss largest gaps →
  converge → rubric annotations. Decisions persist as the term's case
  law (`templates/calibration_session_template.md`).
- **allocation** — balance estimated *hours*, not item counts; per-duty
  estimates shown for the professor to adjust; conflict-of-interest
  screen; rotation for fairness and development.
- **meeting** — agenda from the week's real state + a running decisions
  log.
- **consistency** — cross-TA analysis from professor-provided samples:
  per-criterion distributions, drift flags, re-calibration triggers.
  Aggregate-first and pseudonymized by default — **no league tables**.
  Identified-TA views exist only at the professor's explicit request,
  framed developmentally, draft-only.

Employment facts (hours caps, contracts, pay, mandated training) are
institutional — always `[NEEDS PROFESSOR INPUT]`. Guide:
`assets/ta-coordinator/references/ta_management_guide.md`.
