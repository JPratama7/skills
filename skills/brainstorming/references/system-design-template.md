# System Design Template

Use when the user chooses "System design" as the output format in Phase 3. Adapt to the problem — not every section applies to every design.

## Structure

1. **Problem & requirements** — what the system does, who uses it, the load/scale/latency constraints that actually matter. Distinguish hard requirements from nice-to-haves.
2. **High-level architecture** — the major components and how they connect. A diagram (even ASCII) is worth a thousand words here. Name the components; don't just draw boxes.
3. **Data model & flow** — what data exists, where it lives, how it moves. Cover the write path and the read path separately if they differ.
4. **Key decisions & trade-offs** — for each non-obvious choice: what was chosen, what was the alternative, why this one. This is the most valuable section for a reader reviewing the design.
5. **Failure modes** — what breaks when a component fails, degrades, or gets overloaded. What's the blast radius. Don't list every possible failure — list the likely and the catastrophic.
6. **Open questions** — what's unresolved and needs a decision before implementation. Be specific; "needs more research" is not an open question, it's a deferral.

## Why this structure

Decisions and trade-offs come before failure modes because the trade-offs *cause* the failure modes. A reader who understands the choices can predict the failures; a reader who only sees the failures can't tell if they're accepted risks or oversights.
