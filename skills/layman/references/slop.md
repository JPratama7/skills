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
- **A pattern match is a candidate, not a verdict.** Every tell has an
  innocent use. Protect literal and domain-valid senses (a builder's
  "foundation", a lawyer's "notwithstanding"), quoted examples,
  attributed claims, and register words that carry force ("never store
  secrets", "may cause drowsiness" - hedges that are content). Confirm
  the defect in context before cutting; a scanner match alone never
  authorizes an edit.
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
- Pseudo-wisdom: sentences that sound like insight and cannot be false.
  "The key is to find the right balance", "it depends on your needs",
  "context is everything", "there is no one-size-fits-all answer". Delete
  the sentence; if nothing is lost, it was filler.
- Vague attribution: "experts say", "studies have shown", "research
  suggests", "it is widely regarded", "many believe". The model has a
  diffuse impression, not a source. Name the source or drop the claim;
  an honest hedge in your own voice beats borrowed authority.
- Outline endings and canned closes: "in conclusion", "as we look ahead",
  "moving forward", "only time will tell", "challenges and future
  prospects", a final paragraph that restates the opening, a section
  summary recapping what the reader just read. End at the last real
  sentence. If a close is genuinely needed, make it a specific next
  action or a real open question.
- Assistant scaffolding: "certainly!", "I hope this helps", "great
  question", "as an AI", "as of my knowledge cutoff", "feel free to",
  "let me know if you'd like", leftover [placeholders], collaborative
  framing in a solo document ("in this article we will explore"). It
  lives on the first and last lines - read those before shipping.
- Status-report filler in commit messages, PR bodies, and updates:
  "preserved all citations", "ensured compliance", "updated
  documentation", "various fixes and enhancements", "maintained
  backwards compatibility" when nothing threatened it. Say what changed
  and why, in one line. If you cannot name the change, you do not
  understand it well enough to summarize it.
- Reader flattery and steering: "here's what's interesting", "worth
  your time", "worth reading", "whether you're a seasoned X or just
  starting out". The reader decides what is interesting.
- Reasoning-chain leaks: "let me think step by step", "breaking this
  down", "here's my thought process". Chat machinery in finished text.
- The "X is real" closer: "the struggle is real", "the stakes are
  real". Spares only the literal is-it-genuine sense.
- Generic positive closes: "the future looks bright", "exciting times
  ahead", "great things are coming". Vague optimism is still a coda.
- Formulaic challenges sections: "despite its strengths, X faces
  several challenges", a whole section named "Challenges and future
  prospects". Say the actual obstacle or skip it.
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
| Paragraphs opening with formal connectors ("Furthermore,", "Moreover,", "Additionally,") | Delete the connector; if the link breaks, fix the order, not the word |
| Synonym cycling ("the app... the platform... the tool") | Pick one name per thing, pronouns for the rest |
| Comma-and chains only; no colons, semicolons, or brackets | Vary the punctuation, not just the words |
| Title-as-thing opener ("X is a curated compilation of...", "Y serves as a guide designed to...") | Delete the definitional first sentence; start with the substance |
| Slogan cadence ("Emit 1,100 tokens. Ship 237KB.", "Four presets, one input.") | Write the sentence, not the tagline |
| Numbered-list inflation ("1. First... 2. Second..." where order is fake) | Use plain bullets or prose |
| False ranges and both-sides padding ("from X to Y" spanning nothing) | Name the actual cases |

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

Second row of the same shelf: multifaceted, nuanced, realm, landscape
(figurative), comprehensive, holistic, transformative, elevate, embark,
unlock, harness, resonate, garner, empower, streamline, myriad,
plethora, paradigm, quintessential, interplay, indelible,
groundbreaking, cutting-edge, state-of-the-art, world-class,
best-in-class, enterprise-grade, renowned, supercharge, revolutionize,
boasts (verb), "nestled in the heart of", "a commitment to", "natural
beauty", "unlock the potential of".

Keep the plain word that a person would reach for instead. "Pivotal" ->
"decisive". "Tapestry" -> "mix". "Underscores" -> "shows".

## Inflated verbs -> plain swaps

Longer Latinate verbs read as formal; formality is the register models
are tuned toward. If you would not say the word to a colleague at a
desk, cut it:

| Inflated | Plain |
|----------|-------|
| utilize, leverage | use, or say what you actually did |
| facilitate | help |
| implement | build, add, do |
| optimize | speed up, cut, tune |
| initiate, commence | start |
| terminate | end, stop |
| demonstrate | show |
| ascertain | find out, check |
| endeavour | try |
| regarding | about |
| prior to | before |
| in order to | to |
| subsequent to | after |
| in the event that | if |
| a number of | some, or the actual number |

Two vocabulary traps pull in opposite directions and both are real:
the ordinary register narrows to safe common words while the
decorative one reaches for showy synonyms. The fix is neither rarer
nor simpler - it is the exact word, chosen by meaning rather than
texture.

## Formatting and leftovers (mostly documents)

- Straight quotes only. No curly quotes, no … character; three dots or
  none. (Em dashes are already banned above - house style, not a tell.)
- Headings: sentence case, never Title Case. No skipped levels. Do not
  open with a heading that repeats the title. Avoid paired-noun
  headings ("Challenges and opportunities", "Tools and technologies") -
  name the heading after what is in the section. No empty parent
  headings.
- Bold: at most one thing per screen. No stacked "**Label:** text"
  bullets - write prose or plain bullets.
- Forced structure: no two-column tables where the second column
  restates the first, no one-row tables, no bullets that are secretly a
  paragraph, no numbered steps with no order. A table earns its place
  when the reader compares across rows or scans a column.
- Model artifacts: markup leaked from a chat window is proof, not a
  signal. Grep pasted output before shipping:
  `oaicite|contentReference|turn0search|[cite: |grok_card|ppl-ai-|utm_source=`
  plus malformed DOIs, named references never used, links that 404.
- Register mismatch: one formal, balanced, slightly promotional tone
  applied to every audience and format. A two-line answer stays two
  lines; use contractions where a person would; no greeting-plus-offer
  wrapper on every message. Also watch for the reverse: a sudden style
  shift mid-document, the seam where generated meets written.
- Emoji as section markers is the same instinct as the bold-label
  bullet in a different costume.

## The shape of the argument (silhouette)

A level above sentences: how the ideas are arranged. These tells survive
even when every sentence is clean. The checker's silhouette layer scores
them against a human reference corpus.

- Preview-then-fulfill: the intro lists what is coming, then the body
  delivers it in that order, headings restating the outline. Cut the
  preview; let sections carry their own titles.
- Rotating scaffold openers: body paragraphs each opening on a
  discourse cue ("First... Next... Finally...", "Another key point")
  instead of their own claim. Open on the claim.
- Summary sandwich: the last paragraph repeats the first paragraph's
  content. Delete the recap loop.
- Callback vocabulary: intro words that vanish mid-document and return
  in the conclusion. Arrangement boilerplate, not resonance.

Genre carve-outs keep this honest: bold-label lists are correct in
reference docs, staccato is correct in social copy, a roadmap abstract
is academic convention. Pass `--genre docs` or `--genre social` to the
checker when the format calls for it.

## Facts are the strongest check

Not style, and more reliable than any tell above: a suspicious reader
verifies what a model cannot fake. Write to survive that check:

- Citations, DOIs, and URLs must resolve. Never write one you have
  not opened; fabricated references are the most common failure and
  the easiest to check (~147,000 surfaced in 2025 publications alone,
  most after peer review).
- Name the source or drop the claim. "Experts say" borrows authority
  you cannot produce; hedging honestly in your own voice beats it.
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

## Rewriting someone else's text

A de-slop pass on a human draft has a second contract, separate from
style: prefer a no-op to an uncertain edit.

- Edit only sentences with a confirmed defect, with the smallest repair
  that fixes it. Copy every other sentence byte-for-byte, in its
  original order and paragraph. No findings: return the source exactly.
- Preserve facts, quantities, dates, names, quotations, citations,
  units, scope, uncertainty, attribution, and register. Magnitude-aware:
  `$47.3M` must not become `$47.3 billion`, `150 km` not `150 miles`.
- Add nothing: no claims, advice, personality, anecdote, certainty, or
  conclusion that was not there.
- Do not create staccato anti-slop prose - a rewrite that chops every
  sentence to five words just moves the tell.
- Force-bearing words are content: keep every "never", "must", "all",
  negation, and scope limiter in safety, security, legal, medical, and
  technical text. Dropping one is a correctness bug, not a style fix.

## Before delivering prose

When the output is a file, run the deterministic checker first:

    python3 references/slop-check.py path/to/file.md [--genre docs|social]

Stdlib Python, three vendored scanners plus local rules, findings with
line numbers on stderr (exit 2 = findings, exit 0 = clean). A file that
quotes bad examples on purpose can carry `<!-- slop-check: off -->`
anywhere in it.

Then re-scan against the lists above for what regex cannot see. If a
paragraph still reads like AI wrote it, revise once more.

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

<!-- slop-check: off (this file quotes bad examples on purpose) -->
<!-- Sources: adapted from Abdulkader-Safi/AI-Writing-Rules (MIT) and
     theclaymethod/unslop (MIT) - both build on Wikipedia's "Signs of AI
     writing" and SlopDetector. -->
