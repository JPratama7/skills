# Local state templates

Create only these three files in the chosen workspace's `.learn-companion/`
directory. Use the directory selected by init.md. Replace bracketed values
with actual evidence or "Not specified." Keep the two status lines
unformatted and near the top; the resume check in init.md reads them. Do not
replace existing state with a fresh template.

## profile.md

```markdown
# Learner Profile

Learning mode: active
Onboarding: complete

## Subject
Learning: [subject]
Situation: [New to it / Some foundation / Returning]
Level: [Beginner / Intermediate / Advanced, or Not specified]

## Goals
Primary: [specific learning goal — what they'll be able to do or explain]
If-then plan: [when <trigger>, I will <study action>; or Not specified]

## Preferences
Checkpoint frequency: Normal
Question style: Open-ended
Guidance level: Explanations on demand

## Strong Concepts
No demonstrated understanding recorded yet.

## Developing Concepts
None recorded yet.

## Revisit
None recorded yet.
```

## progress.md

```markdown
# Learning Progress

No learning events recorded yet.
```

As learning occurs, add a `## Topic` with concise bullets under Introduced,
Retrieval attempts, Demonstrated understanding, and Needs reinforcement.
Record reasoning evidence, not quotations of a whole exchange. Date each
retrieval attempt and mark assisted answers — assistance is fine, but it
isn't independent recall. Keep learner-produced reasoning distinct from
concepts the tutor explained. Consolidate repeated entries. Keep each topic
independently readable so it can be loaded without the whole file.

Each topic also carries scheduling fields the review command reads:
`last reviewed: <date>`, `retention target: <how long to remember>`, and
`next due: <date>` computed per pedagogy.md (~10–20% of the retention
target). Update `last reviewed` and recompute `next due` after every
successful retrieval; a failed or assisted attempt shortens the gap rather
than advancing it.

While waiting on a checkpoint, keep a short section headed exactly
`## Pending decision`, not in a topic, with the question asked and what
reply is awaited. Include the stage: awaiting attempt, awaiting mastery
confirmation, or awaiting advance choice. Remove it once resolved: record
the outcome in the topic, and any reasoning evidence with it. Don't move
the pending text into a topic; update entries the outcome supersedes.
Confirmation covers only what was presented. Don't append unmentioned
claims, rejected alternatives, or invented rationale. Mark assisted answers
assisted; never attribute the tutor's explanation to the learner.

## roadmap.md

```markdown
# Learning Roadmap

## Subject and Goal
[What they're learning and the goal it serves.]

## Topics
[Ordered topics, each: name — status — one-line scope. Statuses: proposed /
confirmed / in progress / mastered. Order reflects the plan the learner
reasoned about, not just a syllabus.]

## Project scaffold
[Optional guided project anchoring practice, for novices or applied
subjects: the artifact they'll build or produce, decomposed into steps.
Mark proposed vs confirmed. None when the subject doesn't suit one.]

## Unknowns
[Unverified prerequisites, unclear scope, scheduling constraints, open
questions about the subject itself.]
```
