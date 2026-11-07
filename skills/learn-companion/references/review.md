# `/learn-companion review`

Spaced retrieval of what's already been studied, plus reflection on where
the learner stands. This is the command that makes learning durable —
massed cramming produces fast forgetting, and this loop is what prevents
it.

## Workflow

1. Read `.learn-companion/` state. Compute what's due: for each topic in
   `progress.md`, compare `next due` against today. Due now or overdue =
   review it. If nothing is due, say so and suggest `study` or `quiz`
   instead — a review without due items is just restudy.
2. Run retrieval on due items: closed-book prompts, problems, predictions.
   One at a time; the learner commits before feedback, as always.
   Interleave confusable topics when the material has them — similar
   problem types or categories that get mistaken for each other. Don't
   interleave unrelated verbal material; the difficulty adds nothing.
3. At milestones — a topic's third clean retrieval, a roadmap section
   completing — ask for teach-back: explain it back or teach it in their
   own words. Producing the explanation is the exercise.
4. Before ending a turn that awaits a learner answer, write the
   `## Pending decision` section in `progress.md` — the posed question
   and the awaited answer — even if nothing else about the topic changed.
   Then update state after every item: `last reviewed`, recompute `next due`
   (~10–20% of the retention target — widen only on clean independent
   recall, shorten on assisted or failed), and move concepts between
   Developing / Strong / Revisit in `profile.md` as the evidence changes.
5. Reflect honestly: report what's sticking, what's slipping, and whether
   the roadmap or goal needs adjusting. If a topic keeps failing review,
   the fix is usually a missing prerequisite or material that needs
   re-teaching — route it back to `study`, don't just reschedule it.

Set expectations in passing when relevant: feeling rusty before review is
normal, and successful effortful recall is exactly when learning happens.
Don't moralize — note it once and move on.

## Teacher side — course reflection

Routes here: student-evaluation analysis, mid-course feedback, peer
observation, teaching portfolio/statement, studying one's own teaching
(SoTL). Evidence honesty governs everything (§11): evaluations measure
student *experience*, not teaching quality; every report states what the
evidence shows AND what it cannot show. Checkpoints use the teacher-side
block in pedagogy.md.

### Modes

- **eval-analysis** — code comments thematically (inductive codes,
  prevalence counts, verbatim exemplar quotes; abusive comments reported
  as count + category, not repeated); triangulate each theme against
  grades, attendance, peer notes, prior terms (corroborated / contradicted
  / eval-only); split actionable from not; end with 2–3 prioritized
  changes (impact × effort × confidence) feeding `plan`'s redesign.
  Mandatory: the §11 bias-caveat block in every report; never average
  Likert without saying so and showing the distribution; no ranking
  colleagues on small-N differences.
- **midcourse** — a 3–5 question instrument mid-term → fast analysis →
  closing-the-loop announcement draft
  (`assets/teaching-reflector/templates/midcourse_survey_template.md`).
- **peer-observation** — briefing packet when being observed; structured
  protocol + debrief plan when observing
  (`assets/teaching-reflector/templates/observation_brief_template.md`).
  Formative and evaluative observation stay separate.
- **portfolio / teaching-statement** — assembled only from real artifacts
  and elicited practices the professor supplies; gaps marked
  `[NEEDS PROFESSOR INPUT]`. Statement claims must cohere with portfolio
  evidence — elicit Socratically, draft in their voice, never fill
  templates (`assets/teaching-reflector/references/teaching_statement_guide.md`).
- **sotl** — the ethics/IRB pointer surfaces before any data-collection
  design; the design states its confounds honestly.

Analysis consumes `assets/teaching-reflector/references/eval_analysis_protocol.md`
(coding method, scalar rules, caveat block, triangulation matrix).
Prioritized changes and evidence write to passport `iteration_history` —
aggregates only, no student-level data. Templates:
`assets/teaching-reflector/templates/`.
