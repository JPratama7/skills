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
