# Report

Scannable summary of status, progress, or findings for a defined audience.
Readers skim: the point must land in the first section.

## Interview questions

Ask all that are not already answered by context:

1. What kind of report — status/progress, investigation findings, periodic review?
2. Audience — team, leadership, external? Decides depth and jargon.
3. Period or scope covered?
4. Headline result — the one thing readers must know?
5. Key numbers/metrics to include?
6. What was done, what is blocked, what is next?
7. Risks or asks — anything the reader must decide or unblock?
8. Length constraint — one-pager vs full doc?

## Template

```markdown
# <Report title>
<Period or scope> · <date> · <author>

## TL;DR
<2-3 sentences. The headline result and anything the reader must act on.
If they read nothing else, this is enough.>

## Key metrics
<Only if the report type calls for numbers.>

| Metric | Value | Change |
|--------|-------|--------|
| <name> | <value> | <vs prior period/target> |

## Progress / Findings
<What was done or learned. Lead with outcomes, not activity —
"shipped X, cutting latency 30%" not "worked on X".>

## Issues and risks
<Blockers, risks, and anything needing the reader's attention. Each item
states impact and what would unblock it.>

## Next steps
<What happens next, with owners/dates where known.>

## Appendix
<Supporting detail, links, raw data. Keeps the body scannable.>
```

## Quality bar

- TL;DR survives alone — a reader who stops after it still gets the point.
- Outcomes over activity — each progress line states a result, not effort.
- Every risk says what unblocks it. Bare "we are blocked on X" wastes the
  reader's attention.
- Cut sections that have nothing to say — an empty "Issues" section is
  noise; delete it rather than padding it.
- Match jargon to audience — a leadership report explains acronyms, a team
  report does not.
- If a picture earns its place (process flow, architecture, dependency),
  it is a Mermaid block — never ASCII art. Most status reports need none.
