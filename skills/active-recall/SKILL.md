---
name: active-recall
version: 1.0.0
description: Build spaced-repetition flashcard decks from source material and run in-chat review sessions backed by a real scheduler. Use whenever the user wants flashcards, Anki cards, cloze deletions, or Q&A cards made from notes, docs, articles, or transcripts; says "make cards", "turn this into flashcards", "quiz me", "test me on", "what's due", "spaced repetition", or "active recall"; or wants to memorize or study material. Cards persist to files with review state — not just chat output.
---

# Spaced Repetition

Two jobs: **build** decks from source material and **review** them in chat.
Everything lives in a deck directory — cards, scheduling state, and exports —
so progress survives across sessions.

## Deck layout

```
<deck-dir>/
├── cards.jsonl    canonical store: {"id","type","q","a","tags","src"}
├── state.json     SM-2 scheduling state + review log (managed by srs.py)
└── exports/       generated files: anki.tsv, deck.md, obsidian.md, mochi.md
```

Default location: `decks/<topic-slug>/` under the working directory unless the
user names a path. `SRS` below means `python3 <this-skill-dir>/scripts/srs.py`.

```
SRS init <deck> [--name "Deck name"]        # create a deck
SRS add  <deck> <cards.jsonl | ->           # validate + append, dedupes by question
SRS lint <deck | draft.jsonl>               # mechanical quality warnings
SRS due  <deck> [--limit N] [--new N]       # cards to quiz now (JSON)
SRS grade <deck> <card-id> <0-5>            # record a review result
SRS stats <deck>                            # totals, due counts, ease
SRS export <deck> --formats anki md obsidian mochi
```

Always update decks through `srs.py` — never hand-edit `state.json`. The
scheduler is deterministic; guessing intervals or due dates defeats it.

## Build mode

Trigger: user supplies material (files, pasted notes, articles, transcripts)
and wants cards.

1. **Read the source fully.** Note its structure; durable facts cluster around
   definitions, mechanisms, contrasts, numbers, and failure modes.
2. **Draft cards** as JSONL objects: `{"q", "a", "type", "tags", "src"}` —
   `type` is `qa` (default) or `cloze` (`{{c1::occluded text}}` inside `q`),
   `src` is the source file/section for provenance. Apply the card rules
   below; load `references/card-design.md` for depth and worked examples.
3. **Grade twice.** First `SRS lint <file>` — fix the mechanical failures
   it names. Then spawn a subagent with the draft plus the card rules
   below; it fails any card a stranger couldn't answer with exactly one
   right answer, or anything compound, recognition-cued, or needing the
   source to parse. Apply its verdicts; re-grade once if many cards
   changed. Authors grade their own drafts leniently, so neither pass is
   optional.
4. **Load them:** `SRS init` then `SRS add <deck> <file>`. Fix any reported
   errors; skipped dupes are fine (they mean coverage overlap). The script
   checks structure only — catching bad questions is what step 3 was for.
5. **Export** the format the user asked for (`--formats anki` for Anki,
   `obsidian`, `mochi`, or `md` for a readable file). If they didn't say,
   produce `md` + `anki` and mention the others exist.
6. **Report** card count, dupe count, and where the deck + exports live.

## Card rules (the quality core)

- **One card, one testable fact.** If the answer has two parts, split the
  card. Retrieval fails on compound answers.
- **Exactly one correct answer.** Add context ("In TCP, what...") until the
  question can't be honestly answered a different way.
- **Answers stay short** — aim ≤25 words. Longer means the card wants splitting.
- **Lists become cloze families**, never "name all 7..." — occlude one item
  per card, make sibling cards for the rest.
- **No yes/no or either/or questions** unless forcing a discrimination
  ("X or Y — which one does Z?").
- **The question must cue retrieval, not recognition.** "What is true about
  X?" cues nothing; "What does X do when Y?" does.
- **Cards must stand alone** — answerable by someone holding only the card.
- **Prefer why/how over what** when the material supports it, but keep the
  answer concrete.
- **Reverse cards only for genuinely two-way facts** (term ↔ definition,
  acronym ↔ expansion). Most facts are one-way.

The grading agent's rubric is this list: read each card as a stranger —
would it have exactly one right answer without the source? If not, it fails:
split it, rewrite it, or drop it.

## Review mode

Trigger: "quiz me", "test me on X", "what's due", or a deck path.

1. Run `SRS due <deck>` — it returns relearning cards first, then due
   reviews, then new cards.
2. Ask **one question at a time**; for cloze cards show the text with
   deletions blanked. Wait for the user's answer.
3. Grade honestly on the 0–5 scale (rubric in `references/review-loop.md`),
   run `SRS grade`, then show the correct answer in one line and move on.
4. Cards that lapsed (`grade <3`) resurface the same day — re-quiz them once
   at the end of the session.
5. Close with `SRS stats` and a one-line summary (reviewed, lapsed, next
   session's due count).

Honest grading is the whole system — inflating grades pushes cards past the
user's actual retention and silently breaks scheduling. When in doubt, grade
lower.

## Hard rules

- Cards go through `srs.py` and into `cards.jsonl` — never chat-only output
  the user can't reuse.
- Don't dump all questions at once in review mode; retrieval needs one at a
  time.
- Keep source facts accurate — a card that misstates the material teaches the
  wrong memory. If the source is ambiguous, flag it instead of guessing.
- Adding cards to an existing deck? `SRS add` dedupes automatically — still
  skim existing cards first to write around them, not into them.
- Drafts pass `SRS lint` and a spawned grading agent before `SRS add`; the
  author's own read doesn't count.
- The quality bar, restated: one testable fact per card, exactly one right
  answer, answerable without the source. Split, rewrite, or drop failures.

## Reference files (load on demand)

- Card quality depth, good/bad examples, coverage strategy, cloze patterns → `references/card-design.md`
- Export format details and per-app import notes → `references/formats.md`
- Full review session flow, grading rubric, lapse handling, pacing → `references/review-loop.md`
