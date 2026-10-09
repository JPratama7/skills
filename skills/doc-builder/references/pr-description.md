# PR description

The **how** companion to a ticket: technical implementation lives next to
the code, where it stays accurate. Readers are reviewers deciding whether to
approve, and future maintainers reconstructing why the code is this way.
Fills the gap left by keeping implementation detail out of the ticket.

## Interview questions

Much of this comes from the diff itself — ask only what the code can't
answer:

1. Ticket — which ticket does this close? Which repo, if cross-repo?
2. What changed — the 2-5 bullets of substance?
3. Design decisions — what approach was chosen, what was rejected, why?
4. Trade-offs — what failure mode does the chosen design prevent? How do
   the pieces interact?
5. Test plan — how to verify, including edge and error cases?

## Template

```
## Ticket
<Jira link / issue ref>

<One- or two-sentence plain intro stating what the PR changes and why.>

Attention Conservation Notice
For: <reviewers>
What: <change and scope>
Action: <review, decide, note, or nothing>
Skip if: <legitimate exit condition, or None>

## What changed
<summary of changes, 2-5 bullets>

## Technical Details
<code paths, design decisions, trade-offs, commands, config changes>

## Test plan
- <how to verify>
- <how to verify>
```

If the user mentions a repo name, include it in the Ticket line (e.g.
`PAY-112 (clinic-api)`) or as a header note. Omit if not provided.

## Quality bar

- **Technical Details carries design rationale**, not just parameter
  values. Explain *why* the chosen approach makes sense — what failure mode
  it prevents, what alternatives were considered, how the pieces interact.
  A reader should understand the design, not just the config.
- **Test plan covers edge cases and error scenarios** when behavior is
  specified by the change or established contract. When details are unknown,
  ask what is intended or phrase the check as inspecting the implementation
  against its documented contract; do not turn plausible behavior into an
  asserted requirement.
- **No meta-commentary** — the description is the output, nothing else. No
  "Assumptions made" or "Notes" sections. If a material detail is unresolved,
  ask before drafting; do not leave avoidable TODOs in paste-ready output.
