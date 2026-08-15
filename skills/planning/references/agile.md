# Agile / Sprint Plans

For team work: sprint planning, iteration scoping, backlog prioritization. The goal is a plan the team can commit to: a clear goal, capacity-matched scope, and explicit P0-vs-stretch separation so the sprint survives reality.

## 1. What you need before planning

Ask for (or pull from the tracker, if available):

- **Sprint length and dates** — e.g., 2 weeks, Mon–Fri
- **Team and availability** — who's on the team, and their actual available days (account for PTO, conferences, part-time, and known meeting load). Capacity math that ignores availability is fiction.
- **Backlog** — the candidate items, prioritized if possible. Pull from the tracker, or accept a pasted list.
- **Carryover** — anything unfinished from the last sprint that still matters, and why it slipped (the why decides whether it fits this sprint).
- **Dependencies and risks** — items blocked on other teams, external vendors, or decisions.

## 2. Build the plan

1. **Write the sprint goal first** — one sentence describing what success looks like at the end of the sprint. Everything in scope should serve it; anything that doesn't is a candidate for the backlog.
2. **Compute capacity** — sum available person-days (or person-hours). Compare against the backlog estimates; the sprint should fit the capacity, not the wishlist.
3. **Scope: P0 vs stretch.** P0 items are committed — the team signs up to deliver them. Stretch items are the buffer: only started if P0 finishes early. Never commit more than ~80–90% of capacity; the rest absorbs the unexpected.
4. **Order and assign** — sequence P0 items by dependency, note who's on what, and flag anything blocked.

## 3. Output format

```markdown
# Sprint Plan: <name/dates>

## Sprint Goal
<one sentence: what success looks like>

## Team & Capacity
| Person | Available days | Notes (PTO, meetings, part-time) |
|--------|---------------|----------------------------------|

Total capacity: <N> person-days

## Committed (P0)
- [ ] <item> — <owner> (~<estimate>) — <dependency/notes>
- [ ] <item> — <owner> (~<estimate>)

## Stretch (P1)
- [ ] <item> — (~<estimate>)

## Carryover from last sprint
- <item> — <why it slipped>

## Risks / blockers
- <risk, and who's watching it>
```

## 4. Estimation guidance

- Use whatever the team already uses (hours, story points, S/M/L) — consistency with existing practice beats a new system.
- If estimates are missing, give relative sizes (S/M/L) rather than inventing precise hours.
- Flag uncertainty honestly: an item the team has never done before gets a bigger estimate and a spike step if needed.

## Anti-patterns specific to sprint plans

- Capacity ignoring availability — planning 10 person-days for someone on PTO all week is planning fiction.
- All-P0 sprints — if everything is committed, nothing is committed; the sprint has no buffer and will fail as a unit.
- No sprint goal — without a goal, scope decisions during the sprint are arbitrary.
- Unchecked carryover — carryover is real work competing with new work; it belongs in the capacity math, not a footnote.
