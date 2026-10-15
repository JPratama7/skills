# Writing style

Apply these rules to the prose of every generated document. They sharpen wording and keep text from reading as machine-generated. They never change section order, required fields, or substance.

Adapted from the Vercel writing guidelines (vercel-labs/writing-guidelines), the AI-Writing-Rules patterns (Abdulkader-Safi/AI-Writing-Rules, MIT), and the unslop tell catalog (theclaymethod/unslop, MIT). `scripts/slop_check.py` covers the mechanical subset with line numbers; this file is the source of truth for judgment calls.

## Precedence

When rules conflict, the first matching source wins:

1. An explicit user request: a stated voice ("we"), house style, or a required external form.
2. The document type's conventions in its reference file: first-person narrative, blameless framing, ticket and PR voice, template section names.
3. `accessibility.md`: opening, paragraph length, list rules.
4. This file.

This file never removes evidence, source figures, causal detail, requirements, risks, or trade-offs. It cuts only words that add no meaning.

## Voice

- Use active voice. Test each sentence by appending "by monkeys". If it still parses, rewrite it.
- Address the reader as `you` in instructions. Use first person in narrative documents, as each type's reference specifies. Never write "the user" or "one can".
- Write steps in the imperative: "Click **Add Project**", not "You will need to click **Add Project**".
- Use the present tense unless the document describes future behavior.
- Keep sentences under 20 words where you can, and vary the length. A four-word sentence next to a long one reads as human; ten uniform 15-word sentences read as generated even when each obeys the cap.
- Use `we` only for a deliberate team action ("we decided"). Never use it to mean "you".
- Do not write rhetorical questions.
- Repeat the real word instead of cycling synonyms ("the app... the platform... the solution"). Pick one name per thing.
- No audience flattery or self-Q&A setups: `Whether you're a beginner or a veteran`, `Why does this matter?`, `What does this mean for you?`, `Here are 5 reasons`. State the point directly.
- No assistant scaffolding in the document itself: no "Certainly!", "I hope this helps", "In this guide we'll explore", no `[insert X]` placeholders (use `TODO:`), no citation artifacts (`[cite: 4]`, `utm_source=`).

## Specificity

- Replace weasel words (`significantly`, `many`, `often`, `typically`, `generally`) with a number or a specific claim. If the number is unknown, write a `TODO:` marker.
- Give the figure and its source for vague quantifiers (`near-zero`, `sub-second`, `most requests`). Never write them bare.
- Name the literal action instead of a metaphor verb (`moves through`, `lands`, `carries`, `hits`).
- Cut a name or implementation detail only when a more general phrasing would not change what the reader understands or does.
- Test each sentence by deleting it. If the paragraph loses nothing, the sentence was filler: cut it for real. Every sentence carries a fact, number, date, cause, or concrete example.
- Make the claim or mark it `TODO:`. Stacked hedges (`it could be argued`, `may potentially`, `to some extent`, `generally speaking`) commit to nothing; one honest unknown beats four qualifiers.
- State what happened; do not explain why it matters to the universe (`plays a pivotal role`, `marks a significant milestone`, `a testament to`). Ceremony is not fact, and neither is an emphasis stage direction (`let that sink in`, `read that again`, `make no mistake`, `the stakes are real`).

## Word choice

- Use the plainest word that carries the meaning: `use` not `utilize`, `help` not `facilitate`, `about` not `regarding`, `before` not `prior to`, `to` not `in order to`, `start` not `commence`, `end` not `terminate`, `find out` not `ascertain`, `some` not `a number of`, `is` not `serves as`, `has` not `boasts`.
- Cut `very`, `just`, `really`, and `simply`. Replace `easy`, `simple`, and `quick` with a concrete description of the work.
- Avoid the AI-vocabulary set: delve, tapestry, vibrant, multifaceted, nuanced, intricate, realm, testament, foster, leverage, robust, seamless, underscore, pivotal, crucial, comprehensive, holistic, transformative, elevate, embark, unlock, harness, showcase, resonate, garner, meticulous, bolster, streamline, empower, myriad, plethora, paradigm, interplay, groundbreaking, cutting-edge, world-class, enterprise-grade. Use `landscape` and `navigate` only literally.

## Accuracy

- Attribute each figure to the source and scope the input states. Do not attach a count to a time window, population, or source the input does not name. If the input gives a total with no window, write the total and mark the window as `TODO:`.
- Recompute derived figures (durations, differences, totals, percentages) from the source values before you write them. Give the interval endpoints: "45 minutes (14:02 to 14:47 UTC)", not a bare "45 minutes".
- Do not name a source (a dashboard, log, deploy history, or person) that the input does not mention.
- Name the source or drop the claim. `Experts say`, `studies have shown`, `many believe`, and `research suggests` lend authority without a source and are banned outright.
- Data does not speak, tell stories, or make cases. `The data speaks for itself` and `the numbers tell a story` dodge the author's job: state the figure and what it shows.

## Tone by document type

- **RCA**: factual and blameless. Name the failure, then the fix. Do not stack apologies.
- **Report**: neutral and scannable. Lead with outcomes, not activity.
- **Requirements**: neutral and exhaustive. Write testable statements.
- **Decision record**: neutral. State the reasons plainly.
- **Ticket**: terse and imperative.
- **PR description**: terse and direct. The reader is mid-review.

## Sentences and paragraphs

- Keep paragraphs to three sentences maximum (`accessibility.md`). Split any paragraph that covers two ideas.
- Open each section with a summary sentence.
- Merge a dependent idea split into choppy fragments into one sentence. Short sentences for emphasis are fine.
- Do not open a paragraph by recapping the previous one (`With this set up...`, `Now that we've covered...`). Pivot to the new point (`The catch is...`).
- Do not open a paragraph with `This`, `It`, or `Because` when the referent sits in the previous paragraph. Name the subject again.
- Do not open consecutive sentences or paragraphs with connectors (`Furthermore`, `Moreover`, `Additionally`, `That said`, `Indeed`). Three or more in a document is the tell; use one only where the logic genuinely turns.
- Avoid datasheet phrasing (`provides`, `is configurable`, `is explicitly labeled`). Say what the thing does.
- Give machines machine actions: "the browser fetches the URL", not "hand the browser a URL". "The token is stored", not "the token holds".
- Make the framing specific to this document. Do not reuse templated openers such as "The question most teams face is whether...".
- Re-read each sentence at speech pace. If you had to re-read it, name the subject, the action, and the consequence in a new sentence.
- No `not just X, it's Y` constructions. Delete the negation and keep the positive half; if it cannot stand alone, the sentence had no content.
- Cut `, highlighting`, `, underscoring`, `, ensuring` tails. They restate what the clause already said.
- Open with the fact, not a warm-up (`In today's fast-paced...`, `It's no secret that...`) and not throat-clearing (`Here's the thing`, `The real issue is`, `Let me be clear`). The mandated intro states what the document is; it never defines the title back to the reader (`X is a Y that...`).
- Do not signpost the document's own structure (`as mentioned above`, `in this section`, `let's turn to`, `having established that`). The next point carries the transition.
- Two or more paragraphs opening on the same template (`Every service was migrated... Every endpoint was verified...`) read as machine rhythm even when each sentence is fine. Vary the openings.
- Do not split a claim into dramatic fragments for rhythm (`Not because X. Because Y.`, `Speed. Quality. Cost. Pick two.`). Join it into one varied sentence; de-slopping into staccato beats is its own tell.
- End at the last real sentence. No wrap-up paragraph that restates the opening (`In conclusion`, `as we look ahead`), and no coda that rephrases the first paragraph in new words; end on a specific fact. Mandated closing sections (`Next steps`, `Open questions`, `Lessons learned`) stay.

## Terms, acronyms, and headings

- Spell out each acronym on first use: "Content Security Policy (CSP) blocks inline scripts".
- Define each technical term on first use, unless the Attention Conservation Notice names an audience that already knows it.
- Write sentence case for headings you create: "Configure environment variables", not "Configure Environment Variables".
- Keep template-mandated section names verbatim (`Acceptance Criteria`, `Out of Scope`), even where they are title case.
- Write descriptive subheadings. Avoid single generic words (`Overview`, `Notes`, `Caveats`). A reader should guess the section content from its heading.
- Name the outcome or question in a title, not the internal feature name.
- Never skip a heading level, and never open the document with a heading that repeats its own title.

## Lists

- Convert three or more parallel items in a sentence into a list. Introduce every list with a colon.
- Use bullets for unordered items and numbers for sequences.
- Keep the real count. Do not pad or trim a list to exactly three items for shape, and break the `a, b, and c` triplet habit in prose: where the count is a choice, pick one, two, or four.
- Use the bold-term format for true definition lists only: `- **Term**: description`. A section where every bullet opens with a bolded label reads as generated; write prose or plain bullets instead.
- Use a table only for genuinely tabular data, never to format a short list or a single comparison.
- Do not end fragments with a period. End full sentences with one.

## Code and placeholders

- Add a language tag to every fenced code block. Use `mermaid` for diagrams.
- Keep code lines at 80 columns or fewer. Keep snippets to 25 lines or fewer, and split longer blocks with prose.
- Explain what each code block does in prose. Do not drop code without explanation.
- Do not point to a full example file at the end of the document. Inline the part that matters.
- Write text placeholders in `snake_case` and make them descriptive: `your_access_token_here`. Write number placeholders as counting sequences: `1234567890123`.
- Never use `<TOKEN>`, `xxx`, `your-token`, or `ABC123`.
- When an example names a model, library version, or API version, check the current string. Do not copy it from memory.
- Write units with a space: `64 KB`, `200 ms`. Seconds are the exception: `30s`.

## Emphasis and inline formatting

- Use bold only for a UI element name or a critical fact, at most one bolded item per screen. Using bold for tone means the sentence needs rewriting.
- Use inline code for paths, file extensions, identifiers, flags, field names, and short snippets.
- If a token would look wrong in a proportional font, format it as code.

## Punctuation and typography

- Never use an em dash or a spaced hyphen as punctuation; it is a ban, not a density target. Use a colon, comma, period, or parentheses. Hyphens inside compound words, ranges, and IDs (`2026-09`, `NFR-1`) are fine.
- Use straight quotes and apostrophes everywhere, prose included. Curly quotes read as typeset output, an AI tell in markdown sources. Write an ellipsis as three dots `...`, never the single `…` character.
- Use `&` only in space-constrained labels. Write "and" everywhere else.

## Links

- Name the destination in anchor text. Never use a bare URL, `here`, or `link` as anchor text.

## Markdown source

- Do not hard-wrap paragraphs. Each paragraph is one line in the source.
- Put one blank line before each heading and around each code block.
- Do not use `---` horizontal rules between sections.

## Pre-delivery scan

Run `python3 scripts/slop_check.py` on the saved file first. For paste-ready output that is not saved (tickets, PR descriptions), pipe the draft: `cat draft.md | python3 scripts/slop_check.py` reads stdin. Fix every hit; template-mandated headings (`Acceptance Criteria`, `Technical Details`, `User Story`, `Options Considered`, `PR Description`) and the ticket `**Summary:**` field are allowlisted already, and hits marked `(judgment call)` are context-dependent — resolve them rather than reflexively rewriting. The script merges three detectors: doc-builder house rules (typography, headings, template-aware formatting), the unslop phrase scanner (collocation-gated jargon, throat-clearing, reader addressing, scaffolds, with domain false-positive protection), and the unslop structure scanner (sentence rhythm, wrap-up codas, connector and opener repetition, signposting).

Then check the judgment items it cannot see:

- Weasel words and vague quantifiers without a figure
- Figures tied to a window, population, or source the input does not state; derived figures not recomputed from their source values; sources the input never mentions
- `we` standing in for `you`; rhetorical questions
- Summary-style openers; passive voice that hides the actor
- `not just X` constructions and `, highlighting`-style tails the regex missed
- Bare URLs, or `here` and `link` as anchor text
- Fenced code blocks without a language tag; hard-wrapped paragraphs
- Generic placeholders: `<TOKEN>`, `xxx`, `your-token`, `ABC123`
- A decorative table, or a bolded-label wall used as a section's default shape
- A wrap-up paragraph that restates the opening; a genuine definition list wrongly flagged
- Template-mandated section names kept verbatim; required sections intact

If a fix needs a fact you do not have, write a `TODO:` marker. Do not invent the fact.

<!-- slop-check: off (this file quotes bad examples on purpose) -->
