# Critique Checklist

Full rubric for draft reviews (Session flow, step 4). Work top-down — never
skip to line-level while structural problems remain. Report at most 3
patterns per review; quote one instance of each and let the user hunt the rest.

## Priority 1 — Structure

- [ ] One-sentence takeaway exists and is stated in the first 2 paragraphs
- [ ] Title states the actual claim or topic (no clickbait, no vague nouns)
- [ ] Every section advances the takeaway; none repeat the intro
- [ ] Sections are ordered by what the reader needs next, not by what the
      author learned first
- [ ] The post ends with a "so what" or next step, not a summary of itself

## Priority 2 — Substance

- [ ] Every factual claim is verifiable or marked `[verify this]`
- [ ] Benchmarks include setup details (hardware, versions, dataset size)
- [ ] Trade-offs are named, not just benefits — what does the recommended
      approach *cost*?
- [ ] Failure modes covered: what breaks, when, and how you'd notice
- [ ] At least one concrete artifact per major section (code, config,
      command output, diagram)
- [ ] Code blocks are complete and runnable — no `...` hiding the hard part
- [ ] "Why" explained for each artifact, not just "what"

## Priority 3 — Clarity

- [ ] Paragraphs max 5 sentences; one idea each
- [ ] Each section opens with its point, then supports it
- [ ] Lists used for enumerations; prose for narrative and reasoning
- [ ] Jargon either defined on first use or appropriate for the stated audience
- [ ] No sentence requires re-reading to parse (flag the user to read
      difficult sentences aloud)

## Priority 4 — Line-level (only after 1–3 pass)

- [ ] Active voice dominates; passive only where the actor is irrelevant
- [ ] Filler phrases cut: "It is important to note", "In today's world",
      "As we all know", "Basically", "Just"
- [ ] Sentence length varies — no runs of 5+ same-length sentences
- [ ] Vague nouns replaced: "things", "stuff", "a lot of overhead" → specifics
- [ ] Hedging is earned: "might", "could", "somewhat" only with justification

## Common anti-patterns with diagnostics

| Symptom | Likely cause | Prescription |
|---|---|---|
| Intro starts with history/context | Writing in learning order | Move the conclusion to the top |
| Wall of text, no artifacts | Explaining without showing | Add the command/config/output being described |
| "X is fast" with no number | Unverified claim or missing benchmark | Rubber-duck the gap (block-playbook) |
| Conclusion restates the intro | Nothing left to say → post may be thin | Ask what the reader should *do* now |
| Every paragraph starts "Also," / "Next," | List disguised as prose | Convert to an actual list |
