# Agent-facing text — operational rules

Apply these rules only when the reader is an agent or tool: prompts, tool
descriptions, error messages, inter-agent instructions, system prompts.
Human explanations keep the plain style.

An agent reader cannot ask a follow-up question, so each rule removes one way
a sentence can be misread. These rules come from ASD-STE100 (Simplified
Technical English); background in `writing-rules.md`.

- One instruction per sentence. Put each step in its own sentence or list item.
- Active voice with a named actor for instructions and procedures.
- Simple tenses only: present, past, future. No "have/has/had + verb".
- One word, one meaning. Use one verb for one action. Do not rotate synonyms.
- Prefer plain verbs (use, check, send, stop, start, report). Avoid "handle",
  "process", "ensure", "leverage".
- No "-ing" verb forms. Write "the tool reads the file", not "is reading".
- No phrasal verbs (set up, carry out, reach out). Use the single verb.
- Use the verb, not a noun made from it ("analyze", not "perform an analysis").
- No semicolons. Write separate sentences.
- Instructions: about 20 words or fewer per sentence. Descriptions: about 25.
- Put conditions and safety rules first, before the action.
- Keep every hedge ("may", "could", "might") in the same sentence as the claim
  it qualifies. Write "the tool may resolve it", never "the tool resolves it".
  A hedge is content: dropping it changes the claim. Do not convert a modal
  hedge into a label or noun ("possible cause", "likely cause", "potential
  issue") — the modal stays inside the sentence that carries the claim.
- No marketing adjectives (seamless, robust, powerful).

After writing an agent-facing file, run
`python3 references/ste100/ste-lint.py FILE` and fix hard violations. It never
flags hedges. Passive-voice findings are advisory.
