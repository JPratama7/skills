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
