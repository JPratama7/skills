# Writing style

Apply these rules to the prose of every generated document. They sharpen wording. They never change section order, required fields, or substance.

Adapted from the Vercel writing guidelines (vercel-labs/writing-guidelines). Docs-site, product-specific, and review-process rules were left out.

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
- Keep sentences under 20 words where you can.
- Use `we` only for a deliberate team action ("we decided"). Never use it to mean "you".
- Do not write rhetorical questions.
- Cut `very`, `just`, `really`, and `simply`. Replace `easy`, `simple`, and `quick` with a concrete description of the work.

## Specificity

- Replace weasel words (`significantly`, `many`, `often`, `typically`, `generally`) with a number or a specific claim. If the number is unknown, write a `TODO:` marker.
- Give the figure and its source for vague quantifiers (`near-zero`, `sub-second`, `most requests`). Never write them bare.
- Name the literal action instead of a metaphor verb (`moves through`, `lands`, `carries`, `hits`).
- Cut a name or implementation detail only when a more general phrasing would not change what the reader understands or does.

## Accuracy

- Attribute each figure to the source and scope the input states. Do not attach a count to a time window, population, or source the input does not name. If the input gives a total with no window, write the total and mark the window as `TODO:`.
- Recompute derived figures (durations, differences, totals, percentages) from the source values before you write them. Give the interval endpoints: "45 minutes (14:02 to 14:47 UTC)", not a bare "45 minutes".
- Do not name a source (a dashboard, log, deploy history, or person) that the input does not mention.

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
- Do not open a paragraph by recapping the previous one (`With this set up…`, `Now that we've covered…`). Pivot to the new point (`The catch is…`).
- Do not open a paragraph with `This`, `It`, or `Because` when the referent sits in the previous paragraph. Name the subject again.
- Avoid datasheet phrasing (`provides`, `is configurable`, `is explicitly labeled`). Say what the thing does.
- Give machines machine actions: "the browser fetches the URL", not "hand the browser a URL". "The token is stored", not "the token holds".
- Make the framing specific to this document. Do not reuse templated openers such as "The question most teams face is whether…".
- Re-read each sentence at speech pace. If you had to re-read it, name the subject, the action, and the consequence in a new sentence.

## Terms, acronyms, and headings

- Spell out each acronym on first use: "Content Security Policy (CSP) blocks inline scripts".
- Define each technical term on first use, unless the Attention Conservation Notice names an audience that already knows it.
- Write sentence case for headings you create: "Configure environment variables", not "Configure Environment Variables".
- Keep template-mandated section names verbatim (`Acceptance Criteria`, `Out of Scope`), even where they are title case.
- Write descriptive subheadings. Avoid single generic words (`Overview`, `Notes`, `Caveats`). A reader should guess the section content from its heading.
- Name the outcome or question in a title, not the internal feature name.

## Lists

- Convert three or more parallel items in a sentence into a list. Introduce every list with a colon.
- Use bullets for unordered items and numbers for sequences.
- Use the bold-term format for definition-style items: `- **Term**: description`.
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

- Use bold only for a UI element name or a critical fact. Using bold for tone means the sentence needs rewriting.
- Use inline code for paths, file extensions, identifiers, flags, field names, and short snippets.
- If a token would look wrong in a proportional font, format it as code.

## Punctuation and typography

- Never use an em dash or a spaced hyphen as punctuation. Use a colon, comma, period, or parentheses. Hyphens inside compound words, ranges, and IDs (`2026-09`, `NFR-1`) are fine.
- Use curly quotes in prose. Keep straight quotes inside code.
- Use the ellipsis character `…`, not three dots.
- End loading and saving states with `…`: `Loading…`.
- Use `&` only in space-constrained labels. Write "and" everywhere else.

## Links

- Name the destination in anchor text. Never use a bare URL, `here`, or `link` as anchor text.

## Markdown source

- Do not hard-wrap paragraphs. Each paragraph is one line in the source.
- Put one blank line before each heading and around each code block.
- Do not use `---` horizontal rules between sections.

## Pre-delivery scan

Before delivery, scan the generated prose for these and fix each hit:

- Em dashes or spaced hyphens as punctuation; `...`; straight quotes in prose
- Banned words: `easy`, `simple`, `quick`, `very`, `just`, `really`, `simply`
- Weasel words and vague quantifiers without a figure
- Figures tied to a window, population, or source the input does not state; derived figures not recomputed from their source values; sources the input never mentions
- `we` standing in for `you`; rhetorical questions
- Summary-style openers; passive voice that hides the actor
- Bare URLs, or `here` and `link` as anchor text
- Fenced code blocks without a language tag; hard-wrapped paragraphs
- Generic placeholders: `<TOKEN>`, `xxx`, `your-token`, `ABC123`

If a fix needs a fact you do not have, write a `TODO:` marker. Do not invent the fact.
