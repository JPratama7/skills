# `/learn-companion plan`

Co-design the learning roadmap with the learner. The goal is a sequence
they understand and chose, not a syllabus handed down — their reasoning
about order and priority is itself practice, and it surfaces assumptions
you'd otherwise have to guess.

## Workflow

1. Read `.learn-companion/` state. If no roadmap exists, start from the
   subject and goal in `profile.md`.
2. Ask how the learner would break the subject down or where they'd start
   — before proposing a structure. Their decomposition reveals what they
   think the subject is made of; a viable ordering needn't be the one you
   would have chosen.
3. Propose a decomposition only after their attempt: ordered topics with
   one-line scopes, flagging prerequisite relationships and places where
   their ordering would make a topic needlessly hard. Challenge gaps and
   assumptions; explain tradeoffs without treating a standard curriculum
   as mandatory.
4. For novices or applied subjects, propose one small guided project — a
   real artifact they'll build or produce across topics. Guided project
   work anchors practice; unguided discovery fails novices. Keep it small
   enough to finish; a project that never ships teaches nothing.
5. Confirm scope per topic cluster, then write `roadmap.md` marking
   learner-chosen order confirmed and your additions proposed. Leave
   unresolved questions in Unknowns rather than guessing.

Roadmaps are editable: revisiting `plan` after progress or a goal change
revises it — keep mastered topics, reorder the rest with the learner.

## Teacher side — course and program design

Teacher requests about a course's structure route here: designing or
redesigning a course, writing outcomes or a syllabus, auditing alignment,
mapping outcomes to program/accreditation criteria, and class-readiness
diagnostics. Checkpoints use the teacher-side block in pedagogy-teaching.md; state
lives in `course_passport.yaml` (state.md).

### Course design

Backward order is non-negotiable (§1): outcomes → assessment plan →
schedule → syllabus. If the professor starts from topics, capture them as
raw material, then redirect to "what should students be able to *do*
afterward?"

1. INTAKE — course facts (size, level, modality, weeks, contact hours),
   who the students are, constraints, term calendar. Missing facts = ask,
   don't guess. Initialize `course_passport.yaml` (template:
   `assets/course-designer/templates/course_passport_starter.yaml`).
   Vague aims → guided dialogue first: surface what the course is *for*,
   then design — a clear spec skips this.
2. OUTCOMES — 3–8 measurable Bloom-tagged outcomes with rationale.
   🧑 checkpoint: highest-leverage decision in the pipeline — present 2
   genuinely different directions where the space forks, not a fait
   accompli. Verb quality and level distribution:
   `assets/course-designer/references/outcome_verbs.md`.
3. EVIDENCE — assessment plan: type, weight, week, outcomes assessed,
   AI-use tier per assessment. 🧑 checkpoint.
4. ARC — week-by-week schedule mapped to outcomes, spacing/interleaving
   (§5) and workload balanced across weeks (estimates per
   `workload_audit` — the constants in the alignment section below are
   adjustable, record what was used). 🧑 checkpoint.
5. AUDIT — the alignment gate below. BLOCK findings loop back to the
   owning phase, max 3 rounds, then escalate as a recorded decision.
6. SYLLABUS — assemble from
   `assets/course-designer/templates/syllabus_template.md`;
   institution-specific policies are `[NEEDS PROFESSOR INPUT]` markers,
   never plausible filler. Checklist:
   `assets/course-designer/references/syllabus_checklist.md`.

Partial requests: outcomes-only, syllabus-only (from an existing design —
ask for missing pieces, don't invent policy). Redesign runs the audit
*first* against the existing course plus a six-question diagnostic (what
students struggled with, whether outcomes still fit, where alignment broke
in practice, what the AI era changes, the highest impact-to-effort change,
what must NOT change), then re-enters at the earliest broken phase.
Async/hybrid conversion redesigns delivery only — self-contained modules,
sync/async split, engagement design, UDL defaults
(`assets/course-designer/references/async_design_guide.md`,
`templates/async_module_template.md`); outcomes and weights untouched.

### Alignment gate (standalone or post-design)

Machine-checkable: `python3 assets/scripts/check_alignment_gate.py
<passport>` (or `check_passport.py` for structure). The checks:

- **A — triangle:** every outcome assessed (A1) and taught (A2); every
  assessment names outcomes (A3); weeks map to outcomes or are tagged
  logistics (A4, WARN); nothing assessed before it's taught (A5, WARN).
- **B — outcome quality:** measurable verbs (B1), `bloom_level` declared
  (B2), sane level distribution (B3), 3–8 outcomes (B4).
- **C — assessment structure:** weights sum to 100 (C1); none >40%
  (C2); a low-stakes item precedes the first ≥20% one (C3); item types
  plausibly cover outcome levels (C4).
- **D — workload:** estimate present (D1); within ±25% of ~2 out-of-class
  hours per contact hour (D2); no two ≥15% deliverables due the same week
  (D3). Estimation: dense reading ~100 wpm, novice problem-set time ≈
  professor's solve-time ×3, writing 0.5–5 hrs/page by genre.

Any BLOCK → fail, back to design. WARNs present with rationale and are
dismissible with a logged reason — never re-raised. Missing data reports
NOT_EVALUABLE, not a silent pass. Findings cite passport ids, not "some
outcomes". The gate checks structure, never editorializes merit.

### Program / accreditation mapping

Extends alignment one level up: course outcomes → program outcomes →
standard criteria. The professor supplies the standard's text verbatim,
current version — no text, no matrix. Build the LO × outcome × criterion
matrix: the professor claims each cell's strength; each cell's evidence
status is verified against the passport (CLAIMED / EVIDENCED / HOLLOW —
never upgraded as a courtesy). Then: evidence index (what exists, with
provenance, what's missing), gap analysis (remediation routes to redesign —
this workflow never edits outcomes to fit a standard), self-study drafts
whose claim strength is capped by evidence status — hollow cells generate
gap statements, not "students demonstrate" prose. Pin the matrix to the
standard's version; a revision invalidates loudly.
Templates: `assets/accreditation-mapper/templates/`; orientation:
`assets/accreditation-mapper/references/accreditation_frameworks.md`.

### Cohort diagnostics (学情分析)

Turn student data the professor holds into cohort-level evidence:

- **instrument** — ungraded pre-test or questionnaire; every item names the
  decision it informs (`assets/cohort-analyst/templates/diagnostic_template.md`,
  `references/diagnostic_design_guide.md`).
- **cohort-profile** — aggregate readiness profile: per-concept
  distributions, misconception prevalence, heterogeneity. Pseudonymize
  rows in-session; the passport receives aggregates only, shown verbatim
  before writing (`templates/cohort_profile_template.md`).
- **lesson-calibration / grouping / progress** — reteach-activate-skip
  adjustments for a specific week; evidence-based grouping by pedagogical
  goal (never learning styles); mid-term trajectory comparison.

Iron rules: cohort-only state writes — no individual-level fact anywhere;
no prediction, no tracking labels; self-reported confidence and measured
ability in separate, labeled sections; instrument-strength caveats in every
report; "which students need help?" routes to `mentor` with the evidence in
hand — never answered from cohort data. Ask only for needed columns;
suggest stripping names before sharing (honesty detail:
`assets/cohort-analyst/references/analytics_honesty.md`).
