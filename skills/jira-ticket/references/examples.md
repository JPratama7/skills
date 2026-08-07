# Worked Examples

Calibration examples for each template type. Load this when the user wants to
see what a good ticket looks like, or when a drafted ticket feels off and you
need a concrete contrast to diagnose why. Each type has a strong and a weak
example — the gap between them is the lesson.

## Task

### Strong
```
Summary: [BE] Add ICD10 search API for claims intake

## Context
Claims adjusters manually look up ICD10 codes on a separate site, adding ~40s
per claim. Part of the claims-speed epic (PAY-220).

## Scope
- New GET /api/icd10/search?q= endpoint, prefix match on code and description
- Return top 20 results, ranked by exact-code > prefix-code > description match
- Rate-limited to 60 req/min per user

## Refs
*Repo:* clinic-api
*Epic:* PAY-220

## Acceptance Criteria
- Search returns results within 200ms p95 for queries of 3+ characters
- Empty query or <3 characters returns 400 with a clear error message
- Results include code, short description, and category
```

### Weak (and why)
```
Summary: [BE] ICD10 stuff

## Context
We need ICD10 search.

## Scope
- Add search
- Make it fast
- Maybe caching? Confirm during discovery.

## Acceptance Criteria
- Works correctly
- Good performance
```
- **Summary** describes nothing actionable; no outcome.
- **Context** has no "why this exists" or link to the larger effort.
- **Scope** hedges ("confirm during discovery") instead of committing; "make
  it fast" has no target. The conditional caching item should be stated as a
  condition ("Redis cache if p95 exceeds 200ms at 100 RPS"), not a hedge.
- **Acceptance Criteria** are untestable — "works correctly" and "good
  performance" cannot be verified with a single check.

## Bug

### Strong
```
Summary: [BUG] Export CSV drops rows when description contains a comma

## Reproduction
*Steps:*
# Open the claims list, filter to status=paid
# Click "Export CSV"
# Open the file — 312 rows expected (matches filter count), 298 present

*Expected:* Exported row count matches the filtered list count.
*Actual:* 14 rows missing; every missing row has a comma in the description
field.

## Environment
*Env:* staging
*Version:* clinic-api@a1b2c3d
*Repo:* clinic-api

## Refs
*PRs:* #482

## Acceptance Criteria
- Exported row count equals filtered list count for any description content
- Descriptions containing commas are quoted per RFC 4180
- Existing exports without commas are byte-identical to pre-fix output
```

### Weak (and why)
- Summary says "Export is broken" — no specificity, unsearchable in a backlog
  of 200 bugs.
- Reproduction lists "click export" but not the filter or the expected vs
  actual counts — the reporter knows the gap is the signal.
- Environment omitted. Without the version, the fixer can't reproduce.
- Acceptance criteria: "Export works" — doesn't pin the failure mode, so the
  fix can regress silently.

## Story

### Strong
```
Summary: [STORY] Clinicians can batch-approve routine claims

## User Story
As a claims lead,
I want to select and approve up to 50 routine claims in one action,
so that I spend my review time on complex claims instead of clicking
through 200 identical $12 co-pays.

## Context
Routine claims under $50 with no flags account for 60% of review volume but
2% of dispute risk. Batch approval is the highest-leverage cut in the
claims-speed epic.

## Scope
- Multi-select on the claims list (shift-click range, ctrl-click individual)
- "Approve selected" action, capped at 50 per batch
- Confirmation modal listing count and total value before commit
- Audit log entry per claim (not per batch) for compliance

## Out of Scope
- Bulk rejection (separate story, PAY-241)
- Saved filter presets (PAY-238)

## Refs
*Epic:* PAY-220
*PRs:* #490

## Acceptance Criteria
- Selecting 50 claims and approving completes in one round-trip
- Selecting 51 claims disables the approve button with a visible reason
- Each approved claim gets its own audit entry with reviewer id and timestamp
- Confirmation modal shows exact count and sum before the action commits
```

### Weak (and why)
- User story's "so that" restates the capability ("so that I can batch
  approve") instead of naming the benefit.
- Scope mixes in "maybe bulk reject too" — that belongs in Out of Scope or a
  separate story, not as a hedge inside scope.
- Acceptance criteria miss the edge case (the 51st claim) and the compliance
  requirement (per-claim audit). Both are the kind of thing that causes
  rework.

## PR Description

### Strong
```
## Ticket
PAY-245 (clinic-api)

## What changed
- Added GET /api/icd10/search with prefix matching on code and description
- Results ranked: exact code > prefix code > description match, top 20
- Per-user rate limit at 60 req/min via the existing token-bucket middleware

## Technical Details
Ranking is a single SQL query with ORDER BY CASE — no second round-trip, no
in-memory sort. The CASE weights exact-code (3), prefix-code (2), description
(1); ties break alphabetically. Considered a separate search index (Meilisearch)
but rejected: 18k codes, sub-200ms p95 already met, and an index would add an
operational surface we don't need yet. Rate limiting reuses the existing
token-bucket middleware (src/middleware/ratelimit.ts) so behavior matches the
rest of the API.

## Test plan
- 3-char query returns ranked results within 200ms p95 (bench locally)
- Empty / <3-char query returns 400, not an empty 200
- Description with comma/special chars doesn't break ranking or JSON output
- 61st request in a minute returns 429, not 500
```

### Weak (and why)
- Technical Details lists "added ranking" with no rationale — reader can't
  evaluate the design or maintain it.
- Test plan only covers the happy path; the 429 and the special-character
  cases are exactly what regresses first.
- Ticket line omits the repo, so a reviewer scanning cross-repo PRs can't
  tell which service this is.
