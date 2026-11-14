# Knowledge reliability

Rules for learning content written to files — concept notes, exercises,
material-grounded content, reading lists. State files (profile, progress,
roadmap) record what happened and are exempt; fabricated content is the
failure mode this file exists to prevent.

## No source, no claim

Never fabricate: URLs, DOIs, citations, publication dates, version
numbers, author names, expert quotes, statistics, benchmark results, or
material page/slide numbers. To reference a specific resource:

- **With web access:** search and verify before citing.
- **Without:** name the resource by type ("the official Python asyncio
  docs") without a URL, and mark `[unverified — verify before use]`.

Anything you state as fact without a source gets marked `[unverified]`
or cut. Prefer primary sources (official docs, papers, textbooks) over
secondary (expert blogs, talks) over tertiary (AI output, forum answers).

## Freshness

Tag generated content by how fast it goes stale, and say so near the
content — the learner shouldn't have to open a log to learn the material
may be dated:

| Tag | Meaning | Re-check |
|---|---|---|
| 🟢 Stable | Foundational, rarely changes | ~yearly |
| 🟡 Evolving | Shifts every 1–3 years | ~6 months |
| 🔴 Volatile | Changes monthly or faster | ~monthly |

🔴 Volatile content carries an inline warning: "may be outdated — verify
before use." Versioned APIs, pricing, benchmark claims, exam policies,
and regulations are volatile by default.

## No web access

When you can't verify against the live web, tag generated content
`⚠ Unverified draft` and tell the learner which specific claims to check
and where (e.g. "check the current React docs for this API"). Do not
invent links, versions, or dates to compensate for missing access.

## High-stakes domains

Medical, legal, financial, safety-critical, and professional-certification
material gets a one-line disclaimer at the top of generated files —
educational use only, not professional advice — and every claim not
backed by a primary source is flagged.

## Per-file footer

Each generated learning-content file ends with:

```markdown
---
**Sources:** <what the content grounds to, or "model knowledge">
**Freshness:** 🟢 | 🟡 | 🔴
**Claims to verify:** <list, or "none">
**Last verified:** <date or "unverified">
```
