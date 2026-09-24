# Decision record

Durable record of a significant choice and the reasoning behind it. ADRs
are the best-known form, but the format fits any consequential decision —
technical, product, process, organizational. Readers are future teammates
who need the *why* after everyone forgets the meeting. The *what* is
already visible in the code, the plan, or the org chart; this doc
preserves what isn't.

## Interview questions

Ask all that are not already answered by context:

1. Decision — what is being decided? Phrase it as a question the record answers.
2. Context — what makes a decision necessary now? Constraints, prior decisions, deadlines?
3. Drivers — which criteria actually decide this (cost, speed, risk, compliance, reversibility)?
4. Options — which alternatives were seriously considered? Pros and cons of each?
5. Outcome — which option won, or is this still a proposal? What tipped it?
6. Deciders — who made (or must make) the call?
7. Reversibility — how hard is it to undo? What signal should reopen the decision?
8. Consequences — what does the choice enable, cost, or rule out? What work does it create?
9. Prior records — does this supersede or amend an existing decision record?

## Template

````markdown
# <NNNN:> <decision as a short active sentence>

| Field | Value |
|-------|-------|
| Status | Proposed / Accepted / Rejected / Deprecated / Superseded by <NNNN> |
| Date | YYYY-MM-DD |
| Deciders | <names or roles> |
| Reversibility | Easy / Costly / Irreversible |

## Context
<The forces at play: why a decision is needed now, constraints, prior
decisions in scope. Name the drivers — the criteria that actually decide
this (cost, speed, risk, compliance). Neutral — advocacy belongs under
Decision. Write for a reader with no memory of the discussion.>

## Options considered

| Option | Pros | Cons |
|--------|------|------|
| A. <option> | <pros> | <cons> |
| B. <option> | <pros> | <cons> |
| C. Do nothing | <pros> | <cons> |


## Options Considered

### <Iterated using A, B, C, and continues> <Option>
#### Why 
<Explain why this option was chosen>
#### Pros
<Pros of this option, enforce in bullet point only>
#### Cons
<Cons of this option, enforce in bullet point only>

<If the decision changes a structure or flow, diagram the chosen shape —
or before/after — in Mermaid:>

```mermaid
flowchart LR
    A[<component>] -->|<relation>| B[<component>]
```

## Decision
<The chosen option as an active sentence — "We will do X" — then the
reasoning: which drivers mattered most, which cons were accepted
knowingly.>

## Consequences
<What this makes easier, harder, or impossible. Costs, follow-up work.
Negative consequences belong in the record — a doc listing only benefits
is a pitch, not a record. End with the revisit trigger: the condition or
signal that should reopen this decision.>

## Links
<Related records, docs, tickets, PRs. Omit the section if none.>
````

Naming: if the repo or team already keeps decision records
(`docs/decisions/`, `docs/adr/`, a decision log), follow its numbering and
location. Otherwise propose `docs/decisions/NNNN-<kebab-title>.md`
starting at 0001.

## Quality bar

- The decision is one active sentence a reader could disagree with —
  "We will ship monthly pricing only", not "pricing stuff". If it cannot
  be argued against, it isn't a decision.
- Rejected options carry real reasons — the "why not" is the most valuable
  part of the record years later.
- Consequences name the negatives — every accepted con from the options
  table shows up here.
- Context stands alone — a reader who missed the meeting can reconstruct
  the problem without digging through chat history.
- One decision per record — bundling several makes superseding just one
  awkward later.
- Status is honest — Proposed stays Proposed until deciders accept, and
  superseding links both ways: the old record gains "Superseded by NNNN".
- Reversibility is stated plainly — an irreversible decision deserves more
  scrutiny before acceptance, and the field forces that conversation.
- Diagrams are Mermaid when they earn their place; pure process or policy
  decisions need none — omit rather than forcing one.
