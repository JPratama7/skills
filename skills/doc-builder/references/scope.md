# Scope Guide

Deep guide for the Scope and Out of Scope sections. Load this when the user is
uncertain how to phrase a scope item, when scope contains hedges or TBDs, or
when a feature has fuzzy boundaries that need an explicit out-of-scope list.

## What scope is

Scope items are **commitments to deliver**, written as definitive statements.
A reader — engineer, PM, or reviewer — should finish the scope section knowing
exactly what will exist when the ticket is done. Scope is not a brainstorm, a
research agenda, or a place to register uncertainty.

## Handling uncertainty

The rule in `ticket.md`: no "TBD", no "confirm during discovery". Uncertainty gets
resolved *before* writing scope, by asking the user. When you can't ask, use
these forms instead of hedging:

### Conditional item (when something *might* be needed)
State the condition and the action as a single committed item:
```
- Redis cache layer if p95 exceeds 200ms at 100 RPS in load test
```
The condition makes it actionable and testable; "maybe caching, confirm
during discovery" makes it noise. The reader knows the trigger and the
response without a follow-up conversation.

### Alternative item (when one of two approaches will win)
Pick the default and name the fallback, both as commitments:
```
- Streaming response via SSE; fall back to polling if SSE is blocked by
  the corporate proxy in the staging env
```
Don't write "SSE or polling, decide later" — that defers the decision into
the work itself, which is where decisions go to die.

### Genuinely unknown work (research spike)
If the work is to *find out* whether something is possible, that's the scope
item — the deliverable is the answer, not the feature:
```
- Spike: determine whether Postgres full-text search meets the 200ms p95
  requirement on the 18k-row ICD10 dataset; document findings in a comment
```
This is a committed deliverable (a documented finding), not a hedge.

## Out of Scope

Out of Scope is not a dumping ground for "things we thought about". It exists
to **pre-empt scope creep and mis-set expectations**. An item belongs here
when:
- A reasonable reader would assume it's included, but it isn't.
- It's a known adjacent feature that will tempt the implementer to expand.
- It was explicitly discussed and deferred.

Don't list things nobody would assume are included ("Out of Scope: rewriting
the auth system") — that's filler. List the *tempting* exclusions.

## Anti-patterns

- **"And polish"** — unbounded. Name the specific polish items or drop it.
- **"Fix related bugs"** — which bugs? File them separately or name them.
- **Scope that's really acceptance criteria** — "search returns results in
  under 200ms" is a criterion, not scope. Scope is the work; criteria are the
  verifiable outcomes.
- **Scope that's really context** — "the claims team has been asking for
  this" is context, not scope. Scope is what you're building.
- **Single mega-item** — "Implement batch approval" with no breakdown. Split
  into the discrete deliverables (multi-select, action, confirmation modal,
  audit log) so progress is trackable and review is scoped.
