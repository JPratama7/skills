# `/learn-companion quiz`

Formative retrieval practice across current topics. This diagnoses what's
actually retained and understood — it exists to find weak spots before
they compound, not to assign a grade. Scheduled long-term spacing lives in
`/learn-companion review`; this command answers "do you know it now."

## Workflow

1. Read `.learn-companion/` state and resolve any `## Pending decision`
   first. Select topics: the learner's request, or in-progress and
   recently-mastered roadmap topics — those are where retrieval evidence
   is worth collecting.
2. Generate questions that require production, not recognition: problems,
   explanations, predictions, "why does X follow from Y." Mix formats
   within the selected topics; interleave confusable categories when the
   material has them.
3. One question at a time, open-ended by default. The learner commits each
   answer before feedback — never reveal the answer with the question or
   evaluate a question they haven't attempted.
4. Feedback after each answer: correct errors specifically, not
   generically. An assisted or wrong answer updates the topic's Needs
   reinforcement and shortens its next-due gap; a clean independent
   answer is evidence toward mastery.
5. Follow up on wrong answers within the same session — a re-derived
   answer or a corrected explanation converts the miss into learning.
   Don't advance past an uncorrected error.
6. Before ending a turn that awaits a learner answer, write the
   `## Pending decision` section in `progress.md` — the posed question
   and the awaited answer. Report by topic: demonstrated, shaky, or
   absent. Update `progress.md` retrieval attempts with dates, adjust
   roadmap statuses that the evidence changed, and set or shorten
   `next due` on every topic touched.

Keep the tone factual: no praise, no hype. A quiz that always goes well is
probably too easy — if everything is clean retrieval, push one step
harder or toward transfer.

## Teacher side — assessment instruments

Routes here: exams, quizzes, question banks, rubrics, project briefs, group
assessments, accommodation variants, integrity audits, answer keys, item
and grade analysis — plus checking student submissions against a spec.
Checkpoints use the teacher-side block in pedagogy.md.

**Blueprint first, always (§10).** No item is written before the professor
confirms the content × Bloom blueprint built from the outcomes — a hurry
gets a fast minimal blueprint, not a skipped one. Workflow:

1. INTAKE — the passport assessment entry (weight, week, outcomes, AI
   tier) or standalone context. Missing = ask, don't guess.
2. BLUEPRINT — content × level matrix, point and time budgets
   (`assets/assessment-architect/templates/test_blueprint_template.md`).
   🧑 checkpoint — coverage and difficulty are decided here.
3. ITEMS — drafted cell by cell, each tagged with LO id + level; an item
   mapping to no outcome is a defect, not a bonus. Distractors from known
   misconceptions (`assets/assessment-architect/references/item_writing_rules.md`).
4. KEY — produced by *solving* every item, not transcribing intent.
   Worked-vs-intended discrepancies are flagged to the checkpoint, never
   reconciled silently.
5. INTEGRITY — the audit below against the declared tier.
6. ASSEMBLE — instrument + logistics: versions, exam-day instructions,
   accommodation variant derivable (extra-time/reduced-length), points
   match blueprint. 🧑 checkpoint → passport `artifact_ref` +
   `ai_resilience` updated.

Other modes: `rubric` (analytic/holistic/single-point; observable
descriptors, TA calibration anchors —
`assets/assessment-architect/references/rubric_patterns.md`),
`project-brief` (TILT:
`assets/assessment-architect/templates/project_brief_template.md`),
`question-bank` (tagged parallel variants), `group-assessment`
(interdependence + individual accountability + peer instrument —
`assets/assessment-architect/references/peer_assessment_guide.md`,
`assets/assessment-architect/templates/group_project_template.md`),
`answer-key` (regenerate by re-solving), `item-analysis`
(difficulty/discrimination/distractors from a results table),
`grade-analysis` (distribution + what-if cutoff comparator, counts only —
the professor sets cutoffs;
`assets/assessment-architect/references/grade_analysis_guide.md`),
`accommodate` (operationalize an
*already-granted* accommodation, equivalent rigor; eligibility is never
decided here, the condition is never named). `[VERIFY]` on uncertain facts —
a confident wrong key is the worst artifact this side can produce.

### Integrity audit

Per assessment: (1) classify vulnerability — could a frontier model
complete it to passing in ≤3 prompts with no course context (high/med/low);
(2) the professor's tier — **P**rohibited / **D**isclosed / **O**pen;
(3) coherence — a high-vulnerability take-home marked P is incoherent:
flag with redesign options; a Tier-O item needs grading criteria that
reward the human contribution; (4) set `ai_resilience`: `reviewed`,
`redesigned`, or `reviewed` + accepted-risk note — no instrument is called
AI-proof. Detectors are never the mechanism (§12). Resilience patterns,
strongest first: supervised components > process evidence > personalized
inputs > class-context coupling > defense sampling > AI-aware tasks
(critique an AI answer, grade the disclosure quality).

### Quality gate (post-build, pre-delivery)

`python3 assets/scripts/check_quality_gate.py <passport>` +
`check_content_markers.py --strict` before student-facing finalization.

- **Q integrity:** `ai_use_policy` states per-category tiers with reasons
  (Q1, BLOCK); every assessment `ai_resilience` set (Q2, BLOCK); ≥20%
  items carry a resilient component or accepted-risk note (Q3); nothing
  depends on detectors (Q4).
- **T transparency:** Purpose/Task/Criteria on briefs (T1, BLOCK); rubric
  for ≥10% items (T2); syllabus states grading, late policy, help routes
  (T3); no unresolved markers in student-facing finals (T4).
- **U accessibility:** heading structure, alt-text, captions, palette
  (U1); alternative participation route (U2); accommodation plan (U3).
- **I inclusion:** exclusionary framing flagged, never silently rewritten
  (I1); support-oriented policy tone (I2).
- **W workload:** re-run the alignment workload checks against *built*
  artifacts — built problem sets run long.

Same mechanics as the alignment gate: BLOCK loops back (max 3 rounds),
WARNs dismissible with a logged reason. U/I checks never block — those
calls belong to the professor and institution.

### Checking submissions against a spec

**Spec before audit.** Compile the professor's standard (template,
requirements doc, rubric, exemplar) into checkable requirements: every
check classified deterministic vs judgment; `NOT_CHECKABLE` items listed,
not dropped — 🧑 spec checkpoint before any submission is touched. Then
audit: every finding cites its location ("§3 Results, p.2: figure has no
caption"); judgment findings quote the evidence and are labeled JUDGMENT —
"a finding without a location does not exist." Batch runs add a fairness
pass (same defect ⇒ same severity; drift spot-checked) and a class pattern
report (defect frequencies, common misses, spec ambiguities). Audit, don't
grade — compliance findings, never scores, unless the professor maps
checks to points (computed as a draft, mapping shown). Off-spec
observations go to a separate note, once — scope creep in an audit is
unfairness in disguise. Modes: spec | audit | batch-audit | self-check
(student-facing checklist, deterministic checks only) | calibrate.
Depth: `assets/submission-auditor/references/spec_design_guide.md`;
templates: `assets/submission-auditor/templates/`. Person-affecting rules
apply to every report — drafts, verify-before-release, pseudonymized.
