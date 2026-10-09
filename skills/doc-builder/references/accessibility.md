# Accessible documents

Make documents easy to scan, re-enter, and act on, especially for readers with ADHD or dyslexia. The same structure helps busy readers without reducing the document's substance.

## Opening

Open every document with a one- or two-sentence plain statement of what it is and why it exists. Follow it immediately with a section labeled exactly `Attention Conservation Notice`, with these four lines in this order:

```markdown
Attention Conservation Notice
For: <who needs to read this>
What: <subject and scope in one sentence>
Action: <what the reader should do: review, decide, note, or nothing>
Skip if: <legitimate condition for stopping here>
```

Keep the intro and notice concise enough to fit on one page. Ground every line in the request, conversation, source document, or established team context. Ask about material gaps in the single interview round; do not invent an audience, owner, action, or skip condition. If no action is needed, say `Nothing; this is for awareness`. If no legitimate skip condition is known, say `None` rather than manufacturing one. Omit optional metadata fields (such as report date or author) when unknown; reserve `TODO:` for material unresolved content that belongs in the document, not routine metadata.

Preserve the document type's required leading identifier. In tickets, put the Summary first, then the intro and notice, then the ticket sections. In PR descriptions, put the ticket reference first, then the intro and notice, then the PR sections. In other documents, put the intro and notice immediately after the title or metadata required by that type. If an external form imposes a stricter structure, keep its required fields intact and place the notice at the nearest compatible point.

## Structure and prose

- Front-load the most important information and any required reader action. For standup-style updates, put action items before background.
- Use descriptive headings that tell readers what follows; avoid clever or generic headings.
- Keep paragraphs to three sentences maximum. Split longer paragraphs or move parallel details into a list.
- Use lists for three or more parallel items, not by default for connected ideas. Keep nesting to one level.
- Define technical terms at first use unless the notice identifies an audience that already knows them.
- Use whitespace and short sections to make it easy to find one's place again. Use bold sparingly.
- Be direct and active, especially when naming action owners. Do not use vague collective ownership where a person or role is known.

## Preserve meaning and rigor

Accessibility is not a reason to remove decision-bearing information. Keep facts, evidence, causal detail, requirements, risks, trade-offs, and technical precision. Shorten repetition and filler, not substance. Retain the type-specific section order and quality bar.

For existing-document rewrites, read the full source first. Derive the intro and notice from its actual contents and audience, extract existing action items near the top, then reorganize and clarify without changing meaning or dropping facts. Flag ambiguous ownership and ask who owns it when context cannot resolve it; do not assign ownership by guess.
