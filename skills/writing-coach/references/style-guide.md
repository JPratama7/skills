# Style Guide

House voice for coached posts. Load during line-level feedback and when the
user asks "does this sound right?" Do NOT enforce during drafting — style
polish is the last pass.

## Voice

- Direct, first-person where natural ("I benchmarked", not "benchmarks were
  run"). The author is a practitioner, not a reporter.
- Confident about verified claims; explicit about uncertainty elsewhere
  ("this held on our workload; yours may differ").
- Senior-engineer register: assumes fluency with the domain's basics,
  never explains what a pointer/GC/container is, always explains the
  author's specific design decision.
- Dry humor allowed, max once per post. No memes-as-sentences, no "Buckle up".

## Technical content rules

- Code blocks: language tagged, complete, copy-paste runnable. Comments only
  where the code isn't self-evident.
- Numbers: always with units and context. "42ms p99" not "fast".
- Commands: show the actual invocation, then explain the flags that matter.
- Diagrams: describe what to draw if the user hasn't made one yet
  (boxes, arrows, what each arrow is labeled).

## Formatting conventions

- Headers: `##` / `###`, plain text, no numbering, no emoji in headers.
- Paragraphs: max 5 sentences.
- Lists: bullets for unordered facts, numbers only for true sequences.
  One item per line, no nested bullets — fold sub-points inline with commas.
- Emphasis: bold for the load-bearing phrase per section, italics for
  incidental stress. Never both in one sentence.
- Links: descriptive anchor text, never "click here". 2–4 "Further reading"
  links at the end instead of a conclusion.

## Banned constructions

- "In today's fast-paced / ever-evolving world..."
- "Without further ado", "Let's dive in", "Stay tuned"
- "It goes without saying" (then don't say it)
- Rhetorical questions in the intro ("Have you ever wondered...?")
- "Obviously" / "Simply" / "Just" — if it were obvious, the post wouldn't exist
- Exclamation marks outside direct quotes
