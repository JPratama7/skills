# Card design reference

Load when drafting cards and the rules in SKILL.md aren't enough — ambiguous
material, lists, procedures, or when a draft needs a quality pass.

## Coverage: what deserves a card

Card-worthy facts are the ones a learner must *produce* later, not just
recognize. Scan for:

- Definitions the field actually uses (not dictionary glosses)
- Mechanisms: what causes what, in what order
- Contrasts: A vs B, when each applies, why one fails
- Numbers that matter: thresholds, limits, defaults, versions
- Failure modes: what breaks, what the symptom looks like
- Decision rules: "if X then Y"

Skip: transitional prose, anecdotes, trivia the user won't need, anything
they'd look up rather than recall (huge tables, exhaustive parameter lists —
card the *pattern*, not the table).

Target roughly one card per durable fact. A 2-page article usually yields
5–15 cards; a textbook chapter, 30–80. If you're drafting far more, you're
carding prose, not knowledge.

## Card types

**qa** (default): question front, answer back. For single facts, causes,
definitions.

**cloze**: sentence with `{{c1::occluded}}` (and `{{c2::...}}` for a second
deletion on the *same* card only when the two facts are inseparable). For:

- Lists and enumerations — one card per item, each occluding a different item
- Ordered steps — occlude one step (or the ordering cue)
- Precise terminology in context ("The {{c1::RAFT}} protocol elects a
  {{c2::leader}} before accepting writes")

For a cloze family over a list, make the *surrounding sentence identical* and
vary only which item is `{{c1}}` — or prefer separate `{{c1}}`/`{{c2}}`… on
one card when the list is short and stable (3–5 items you always need
together).

**Reversed / two-way**: only when both directions are real retrieval tasks —
language vocabulary, acronym ↔ expansion, symbol ↔ meaning. Write as two
separate `qa` cards. Never auto-reverse; most facts are one-way.

## Good vs bad

| Bad | Why it fails | Good |
|---|---|---|
| Q: What is TCP? | Cues nothing; dozens of honest answers | Q: In TCP, what mechanism prevents a sender from overwhelming a receiver? |
| Q: Name the 4 DNA bases | Compound answer; partial recall unscoreable | Cloze family: `DNA bases: adenine, {{c1::guanine}}, cytosine, thymine` etc. |
| Q: Is HTTP/2 multiplexed? | 50% guess; teaches nothing on failure | Q: What does HTTP/2 allow over one connection that HTTP/1.1 doesn't? |
| A: "Mitochondria, which are membrane-bound organelles found in most eukaryotic cells that generate most of the chemical energy..." | Recitation, not retrieval | A: "Mitochondria" (context belongs in the question) |
| Q: What did the article say about caching? | Depends on the source; no standalone answer | Q: Why does a cache write-through policy complicate reads? |

## Drafting procedure

1. Extract candidate facts (one line each: "X causes Y", "default timeout is
   30s") before writing questions — keeps coverage complete.
2. Write each card so the *question* carries the context and the *answer* is
   minimal. Move qualifiers from answer into question.
3. Self-check each card: (a) exactly one right answer? (b) answerable without
   the source? (c) under ~25 words? (d) not a re-worded sibling of another
   card? Fix or drop failures.
4. Tag by topic and set `src` to the source file/section — provenance matters
   when cards conflict later.

## Common failure modes in generated decks

- **Echo cards**: question embeds the answer ("Which organelle, the
  mitochondria, produces ATP?"). Always check the question doesn't leak the
  answer string.
- **Definition stuffing**: answer packs cause + properties + examples. Split.
- **Phantom context**: "What is the third step?" — meaningless without the
  source. Name the procedure in the question.
- **Trivia drift**: carding a number that appears in the source but isn't a
  fact worth keeping ("the study had 47 participants").
- **Cloze overkill**: occluding 4+ fields in one sentence — nothing left to
  cue retrieval. Two deletions per card max, and only if linked.
