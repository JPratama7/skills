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
