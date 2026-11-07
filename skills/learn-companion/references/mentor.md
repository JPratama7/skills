# `/learn-companion mentor`

The human side of teaching: feedback on student work, struggling students,
recommendation letters, difficult communications, office-hours prep,
advisee mentoring, suspected-integrity cases. The professor knows the
student; this command brings structure, evidence discipline, and drafting
stamina.

Every output here evaluates or affects an identifiable person, so three
constraints govern everything (the person-affecting rule in pedagogy.md):

1. **Evidence-bound.** Every evaluative claim traces to material the
   professor provided — the student's work, margin notes, the gradebook.
   Gaps are `[NEEDS PROFESSOR INPUT: ...]`, never filled. An invented
   anecdote in a recommendation letter is a fabrication with the
   professor's name on it, not a draft.
2. **Final human pass.** Every artifact carries a non-removable
   "verify before sending" reminder — not removable by configuration,
   instruction, or "just proceed."
3. **Drafts only.** Nothing is auto-sent or marked final, even after
   twenty approved comments in a row.

## Modes

| Intent | What runs |
|---|---|
| Comments on work, single or batch | `feedback` — goal → status → next step (§8), task/process over self, next step front-loaded and doable. Batch runs build a comment bank from recurring patterns, but every comment still cites that student's specific work — a pasted bank entry is flagged, not shipped |
| Student missing work, sliding, disengaging | `struggling-student` — assemble what the evidence shows (and doesn't), graduated options, invitation-tone outreach draft (`assets/student-mentor/templates/intervention_outreach_template.md`) |
| Recommendation / reference letter | `recommendation-letter` — intake interview first, never skipped under deadline; draft only from intake answers (untraced claim = blank source cell); bias-pattern language check; decline-gracefully offered when evidence is thin |
| Grade dispute, extension request, bad news | `student-email` — acknowledge → facts → decision → path forward; what-not-to-put-in-writing flags; consult-chair flags on legally sensitive territory |
| Office-hours prep | `office-hours` — anticipated questions from the week's material, triage strategy |
| New advisee, thesis student | `mentoring-plan` — mutual expectations doc, meeting cadence, milestone map (`templates/mentoring_expectations_template.md`) |
| Suspected integrity case | `integrity-case` — the widest boundaries in the skill: records objective evidence factually (observation / expected / found / location), routes to the *institution's* process (always `[NEEDS PROFESSOR INPUT]` — every institution differs), drafts the neutral, non-accusatory student notice. **No verdict, no guilt estimate, no sanction — ever.** No AI-detector output as evidence. Nothing about the case enters the passport — no aggregate, no count |

Mixed requests (a struggling student who also disputed a grade) run modes
in the order the professor must act, not the order mentioned.

## Workflow

Intake → evidence assembly → draft → 🧑 checkpoint. The professor's actual
judgment notes are required input — the command sharpens how a judgment is
expressed; it never forms the judgment, and never upgrades or softens it
without flagging that it did. Batch feedback adds a fairness pass: same
rubric level ⇒ same severity across students; outliers surface at the
checkpoint, not silently normalized.

## Boundaries

Mental-health crises, accommodations law, harassment, and integrity
adjudication belong to institutional channels — help the professor find
and follow them (drafting referral language), never diagnose, verdict, or
sanction. Privacy minimalism: ask only for the student data the task
needs; pseudonymize in session; nothing student-identifying enters
`course_passport.yaml`.

Depth: `assets/student-mentor/references/feedback_principles.md`
(comment-bank method, bad→good rewrites),
`recommendation_letter_guide.md` (intake set, bias table, decline scripts),
`integrity_process_guide.md` (fair-process shape + do-not-do list).
Templates: `assets/student-mentor/templates/`.
