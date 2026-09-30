# Review loop reference

Load when running a review session and SKILL.md's summary isn't enough —
grading edge cases, lapse handling, pacing.

## Session flow

1. `SRS due <deck>` returns cards in quiz order: `relearn` (lapsed today),
   `review` (scheduled, oldest due first), `new` (never seen, capped by
   `--new`, default 10/day).
2. Present exactly one card. For `qa`, ask the question. For `cloze`, show
   the sentence with each `{{cN::text}}` replaced by `[...]` — never show the
   occluded text.
3. Wait for the answer. Judge it against the card's answer field (for cloze,
   against the occluded terms).
4. `SRS grade <deck> <id> <grade>`, then show the correct answer in one line
   ("A: Mitochondria — you had it" / "Actually: three duplicate ACKs") and
   continue.
5. At the end, re-quiz any card that lapsed (grade <3 → due same day) exactly
   once, then close with `SRS stats`.

## Grading rubric (0–5)

| Grade | Meaning | Example |
|---|---|---|
| 5 | Instant, complete, confident | Right answer, no hesitation |
| 4 | Correct with real effort | Right but slow/hedged |
| 3 | Correct but shaky — partial credit that captured the core | Got "duplicate ACKs" but missed "three" |
| 2 | Wrong, but recognized the right answer when shown | "Oh right, I knew that" |
| 1 | Wrong; faint familiarity only | Knew the topic, not the fact |
| 0 | Total blackout | No idea, or answered a different question |

Grade the *retrieval*, not the intention. "Almost had it" is a 2, not a 3.
When the user says "give me half credit," that's a 3 at most. Inflated grades
schedule cards past real retention — the deck rots quietly.

## Lapses

`grade <3` resets `reps` to 0 and due to today (status `relearn` in `due`
output). In-session: finish the planned queue, then re-ask lapsed cards once.
A second failure just stays due — don't loop a card more than twice in one
session; diminishing returns and frustration. Note stubborn cards in the
closing summary ("c7 failed twice — consider splitting it or rewriting it as
a cloze").

## Pacing and session shape

- Default session ≈15–20 cards or ~10 minutes; ask if the user wants more
  after the first batch rather than dumping everything.
- New cards enter at most `--new` per day (default 10) — exceeding it floods
  tomorrow's queue.
- If the user answers everything easily, don't inflate grades — 5s are fine;
  the ease factor adapts over reviews, not within one session.

## Multi-deck and housekeeping

- `SRS stats <deck>` per deck tells the user where attention is needed
  (many `relearning` or big `due_today` backlog).
- If the user corrects a card mid-review ("that answer is wrong/outdated"),
  stop, fix `cards.jsonl` for that card directly (edit the JSONL line), re-run
  `export`, then continue. Scheduling state is unaffected by content edits.
