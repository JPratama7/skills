# Slop: AI writing tells to remove

The extended checklist behind SKILL.md's always-on "Sound human" rules.
Load for documents, rewrites, or any output longer than a few sentences.

## Why these patterns exist

Instruction tuning creates them. Base models written before that
tuning show human-like rates of these features; the tuned versions
that users actually meet do not. That is why tells shift between model
families and between years: each new tuned model inherits a fresh set.

Consequence for editing: a fixed banned-word list goes stale. Prefer
rules that describe the *shape* of the problem, plus a short list of
the current offenders, treating the list as rotatable.

Rank the signals before editing:

    verifiable facts   strongest signal, hard to fake
    measured style     real tells, worth fixing
    word lists         weakest, goes stale fast

A reader who suspects machine text checks what it cannot fake, so
edit content first, style second. Keep in mind while editing:

- **The biggest tell is missing content, not style.** Tells below remove
  the machine flavor. They cannot add specifics, a stake, or an opinion.
  A text with nothing to say reads dead after every fix below is applied.
- **Style tells travel badly across domains.** Non-native English writers
  and students show several of the same features as machine output, so a
  feature that flags machine prose can also flag a human writing plainly.
  Do not use these rules to judge a person's writing; use them to edit
  your own output.
- **Detectors score predictability, not patterns.** The two measurable
  signals are perplexity (how surprising the next word is) and
  burstiness (how much sentence length varies). The edits above help
  only where they raise one of the two: varied rhythm does, and so does
  choosing the word a person would say over the safest continuation.

## Phrases to delete

- Throat-clearing openers: "here's the thing", "here's what/this/that",
  "it turns out", "the real X is", "let me be clear", "the truth is",
  "I'm going to be honest", "here's why that matters".
- Announcements and meta: "in this section we'll", "let me walk you
  through", "as we'll see", "the rest of this essay", "hint:", "spoiler:",
  "but that's another post".
- Telling instead of showing: "this is genuinely hard", "this is what X
  actually looks like", "actually matters".
- Performative intimacy: "I promise", "creeps in", "you already know this".
- Filler: "at its core", "in today's X", "it's worth noting", "at the end
  of the day", "when it comes to", "in a world where", "the reality is".
- Emphasis crutches: "full stop", "let that sink in", "this matters
  because", "make no mistake", "period."
- Vague declaratives: "the reasons are structural", "the implications are
  significant", "the stakes are high". If a sentence says something is
  important without naming the specific thing, name it or cut it.
- Business jargon -> plain word: navigate -> handle, unpack -> explain,
  lean into -> accept, landscape -> situation, game-changer -> significant,
  double down -> commit, deep dive -> analysis, circle back -> revisit,
  on the same page -> aligned, moving forward -> next.

## Adverbs and extremes

Kill all adverbs: no -ly words, no softeners, no intensifiers. Offenders:
really, just, literally, genuinely, honestly, simply, actually, deeply,
truly, fundamentally, inherently, inevitably, interestingly, importantly,
crucially. Same for lazy extremes (every, always, never, nobody) doing
vague work: name the specifics instead.

## Structures to break (prose)

| Pattern | Fix |
|---------|-----|
| Additive hedge ("not just X but also Y") | State the addition |
| Negative listing ("not a X... not a Y... a Z") | State Z |
| Dramatic fragments ("X. That's it. That's the thing.") | Complete sentences |
| Rhetorical setups ("what if", "think about it", "and that's okay") | Make the point |
| False agency ("the decision emerges", "the data tells us") | Name the human |
| Narrator distance ("nobody designed this", "people tend to") | Put the reader in the scene |
| Passive voice ("mistakes were made") | Name the actor |
| Wh- openers; "So,"/"Look," paragraph starts | Lead with subject or verb |
| Three-item lists; every paragraph ending punchy | Vary length and endings |
| Lazy extremes (every, always, never, nobody) | Name the specifics |
| Pull-quote phrasing (sounds quotable out of context) | Rewrite it plain |
| Question answered in the same breath | Let it breathe or cut it |

## Grammar-level tells

These are the most reliable and the most generalizable, because they are
measured properties of machine prose rather than vocabulary choices. The
first one is the best-documented tell in the literature.

| Pattern | Fix |
|---------|-----|
| Copula avoidance: "serves as", "stands as", "marks", "boasts", "features", "operates as", "refers to" where "is"/"has"/"was" fits | Use the plain verb. "Serves as a hub" -> "is a hub" |
| Trailing present-participle clauses: "…reflecting its importance", "…ensuring accuracy", "…highlighting the trend" | Delete, or promote to a real verb in its own clause |
| Nominalizations: "the implementation of", "a reduction in", "performs optimization of" | Verb: "we implemented", "it shrank" |
| Agentless passive: "mistakes were made", "the decision was reached" | Name who did it |
| Uniform sentence length; a run of same-shape sentences | Break it: put a short sentence next to a long one |
| Hedging with no content: "it is important to note", "may potentially suggest" | Cut it, or say the actual point |

Note the direction on the first two: machine prose uses copula
alternatives and trailing participles *more* than human prose does, but
agentless passives *less*. So the fix for passives is to add the actor,
while the fix for the other two is to remove the decoration.

## Vocabulary to cut

Short list, deliberately: it is a sample of the current generation's
offenders, not a permanent set. Rotate it as models change.

delve, tapestry, testament to, underscores (verb), pivotal, crucial
(filler), fostering, bolstering, showcasing, enhancing, intricate,
meticulous, seamless, robust (filler), vibrant, rich (filler),
underscoring, leveraging, "a testament to", "stands as", "marks a
shift", "evolving landscape", "the broader", "setting the stage for",
"furthermore" as a connector, "additionally" as a sentence opener.

Keep the plain word that a person would reach for instead. "Pivotal" ->
"decisive". "Tapestry" -> "mix". "Underscores" -> "shows".

## Facts are the strongest check

Not style, and more reliable than any tell above: a suspicious reader
verifies what a model cannot fake. Write to survive that check:

- Citations, DOIs, and URLs must resolve. Never write one you have
  not opened; fabricated references are the most common failure and
  the easiest to check (~147,000 surfaced in 2025 publications alone,
  most after peer review).
- Numbers need a source. Invented precision ("sales rose 34%") fails
  the first time anyone checks. No source: cut it, or say "about".
- Use knowledge a model cannot have: recent events, private data,
  what you saw and did. Anything past a training cutoff is proof a
  person wrote this.
- Claim only what you would defend. Confident statements with no
  source and no way to verify are the tell institutions now hunt.

## Not worth the effort

- Fixed banned-word lists beyond the rotating sample above. Which
  words spike changes per model and per year; today's list is
  tomorrow's normal English. Weakest signal there is - fix the
  grammar patterns instead.
- Em-dash paranoia. Newer models suppress them, so presence or
  absence no longer means anything. Layman still skips them - house
  style, not a tell.
- Faking hedges. The "AI over-hedges" claim was contradicted:
  students hedge more than GPT does. Cut empty hedges, yes; do not
  sprinkle "maybe" to look human.
- Outrunning detectors. One paraphrase pass drops a detector from
  ~70% to ~5% accuracy. Detectors are noise - write for the human
  check.

## Before delivering prose

Re-scan the output against the lists above. If a paragraph still reads
like AI wrote it, revise once more.

Then the check that matters more than any of them: does the text have
something to say? Strip the tells off a text with no specifics, no
position, and no admission of difficulty, and it still reads dead. When
that is the case, the fix is to supply real material, not more editing:

- Name the specific thing instead of the category. "It was slow" needs
  a number, a file, a date, or a symptom.
- If there is an opinion, state it, with the reason. Do not manufacture
  balance where there is none.
- If something is uncertain, say what is uncertain and what would
  resolve it. Do not split the difference to sound safe.
- Keep the awkward true detail. A strange specific fact reads human;
  a smooth generalization reads generated.
- Cut the scope the writer cannot support. Machine prose tends to
  overstate how generally a point applies, because that is the safest
  continuation. Claim less than you feel; claim only what you can back.
