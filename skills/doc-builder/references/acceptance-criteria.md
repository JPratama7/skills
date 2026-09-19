# Acceptance Criteria Guide

Deep guide for the Acceptance Criteria section. Load this when the user is
struggling to write testable criteria, when drafted criteria are vague, or
when a ticket type (bug, compliance, infra) has criteria that resist the
"plain checklist" form.

## Core rule

Every criterion must be checkable by a person who didn't write the ticket,
using only the ticket and the running system. If they'd have to ask the author
"did you mean…?", the criterion isn't done yet.

## Testability ladder

Run each drafted criterion through this check before keeping it:

| Phrase | Verdict | Fix |
|---|---|---|
| "Works correctly" | Fail — no observable behavior | Name the observable: "returns 200 with a JSON body containing…" |
| "Good performance" | Fail — no threshold | Pin a number and a condition: "p95 < 200ms at 100 RPS" |
| "Should be fast" | Fail — "should" + unmeasurable | Same as above; drop "should" |
| "Handles errors gracefully" | Fail — "gracefully" is subjective | Name the error and the user-visible response: "429 with Retry-After header" |
| "Returns results within 200ms p95" | Pass | — |
| "Empty query returns 400 with error code `QUERY_TOO_SHORT`" | Pass | — |

## Per-type guidance

### Task
Criteria describe the delivered behavior, not the implementation. One
criterion per scope item is a reasonable default; more is fine if a scope item
has multiple observable outcomes.

### Bug
The first criterion must pin the failure mode that defined the bug — the exact
"expected vs actual" gap from Reproduction, restated as a pass condition. Then
add regression guards: edge cases adjacent to the bug (empty input, max-size
input, concurrent access). A bug fix with no edge-case criteria is incomplete.

### Story
Criteria prove the user story's benefit is realized, not just that the feature
exists. "User can batch-approve 50 claims" tests the feature; "approving 50
routine claims takes under 30s end-to-end" tests the *benefit* (time saved).
Include both.

### Infra / migrations
Criteria for non-feature work often need a different shape:
- **Migrations:** "rollback succeeds and leaves the schema at the pre-migration
  state within 5 minutes" — not just "migration runs forward".
- **Deploys:** "deploy to staging completes with zero downtime, verified by
  health-check probe during cutover".
- **Cleanups:** "X is removed with no references remaining" — grep-verified,
  not asserted.

## Anti-patterns

- **Implementation-as-criteria:** "Uses a Redis cache" is implementation, not
  a criterion. The criterion is the observable outcome the cache produces
  ("p95 < 200ms at 100 RPS"). Implementation belongs in the PR.
- **Criteria that duplicate scope:** if a scope item and a criterion say the
  same thing in different words, the criterion adds nothing. Criteria state
  the *verifiable outcome*; scope states the *work*.
- **"No errors" as a criterion:** untestable — absence of observed errors
  isn't absence of errors. Name the specific error class that must not occur,
  or drop it.
- **Compound criteria:** "Search is fast and returns ranked results and
  handles special characters" — three criteria in a trench coat. Split into
  three so each can be checked and pass/fail independently.
