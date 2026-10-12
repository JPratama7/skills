---
name: research
version: 1.7.0
description: Research a question by reasoning as an evolving graph of sub-questions — ask the user how to execute, decompose the question, explore branches with parallel research agents, merge, score, and prune — then deliver a cited markdown report plus the thought graph that produced it. Use whenever the user wants a topic investigated, facts or docs/API details gathered, a comparison made, contradictions between sources resolved, or reading legwork delegated — even if they just say "look into X", "find out whether", "dig into", "research this", or "how does X actually work".
---

# Research

Answer research questions as a graph of thoughts: ask the user how to
execute, decompose into sub-questions, explore branches with research
agents, merge, score, prune — then ship a cited markdown report plus the
graph. Explicit coverage beats a linear search, where the first promising
thread eats the budget and unchecked paths go unrecorded.

Keep the working artifacts telegraphic — graph labels, branch findings,
claim lines, bullets. The report is prose, but lean prose: every sentence
carries a claim or a citation, no filler.

## Loop

1. **Root** — one sentence: what is true when answered. Sharpen a vague ask
   first.
2. **Ask execution** — before decomposing, ask the user how to run it. One
   ask covering all of it, not a drip-feed (use the harness's question tool
   if it has one):
   - *Mode* — `parallel` (default): one research subagent per branch,
     launched same turn / `sequential`: same contract, one at a time /
     `inline`: no subagents, you read
   - *Breadth* — how many branches to fan out (suggest 3-5)
   - *Depth* — `quick` (1-2 primary sources per branch) / `standard` /
     `deep` (follow secondary threads)
   - *Background* — what the user already knows and the context that
     should frame the report: why the question matters, prior work,
     constraints, things they refuse to rely on. Feeds the report's
     Background section and can seed branches — never invent motivation
     the user didn't supply.

   Fan-out spends the user's tokens and wall-clock time — they pick the
   trade-off, not you. No usable answer (skipped, non-interactive run, no
   question tool) → defaults: parallel, 3 branches, standard (2 if the
   question is narrow).
3. **Decompose** — independent *angles* (mechanism, status, edge cases,
   alternatives), not steps, sized to the chosen breadth. "And then" = a
   chain, not a branch — fold it. A focused question may honestly be 1-2
   nodes; don't inflate just because agents are available.
4. **Plan check** — show the branch list telegraphically (one line each)
   plus the chosen mode; the user confirms, prunes, or adjusts before
   anything launches. No way to ask → proceed. This is the cost
   checkpoint: each branch will cost a fresh agent context, so cut any
   branch you could resolve with a direct fetch.
5. **Explore** — per the chosen mode. Primary sources only: official docs,
   source code, specs, first-party APIs, papers. A blog citing the docs is
   a pointer to the docs, not a source. Per node record
   `claim — source URL — strong|weak` (`strong` = primary + corroborated;
   `weak` = single or secondary only).

   Spawning a child agent is the loop's most expensive move — roughly the
   cost of everything else combined. Fan out only branches that need
   independent multi-source exploration; a branch you could resolve with
   one or two direct fetches is an inline lookup, not a child. Once a
   branch reports, do not re-read its sources: compile from its findings
   and spot-check only the claims that decide the root answer.
6. **Grow** — findings mutate the graph:
   - new question → spawn a child node
   - conflict with another branch → `contradicts` edge; resolve by source
     authority or flag unresolved — never average two conflicting claims
   - two branches reach the same claim → merge into one node

   Cap the graph at ~12 nodes. Past that, expand only if a branch is needed
   to answer the root — more nodes cost tokens without buying coverage.
   Follow a branch until it answers, dead-ends, or stops mattering to the
   root; then mark it and move on.
7. **Score** — verdict per node: `answered` / `weak` / `pruned` + reason.
   Pruned nodes stay in the graph — silent pruning hides coverage holes.
8. **Synthesize** — write the report.

## Branch contract

Subagent or not, a branch reports back the same way — telegraphic, ≤10
finding lines (≤5 on quick depth), at most two sources per line. Use the
`subagent-manager` brief format if available:

```
Node: <sub-question>
Findings: claim — primary source URL — confidence
New questions: <child-node candidates, or none>
Contradictions: <conflicts, or none>
```

`New questions` feeds step 6 — evaluate each before aggregating. You keep
the graph and run grow/score/synthesize; branches never see each other's
work.

## Report

Save one markdown file where the repo keeps research notes (match
convention; else `docs/research/` or ask). The report is prose, not
bullet claims — the findings told as a story — but stays telegraphic:
~600 words, hard ceiling 800: if the draft runs over, cut the claims that
don't change the root answer, never the citations. Match the worked
example in the template:

- Starting the report → `references/report-template.md`

Sections:

1. **Summary** — 2-4 sentences answering the root question directly. The
   whole report in miniature; a reader stops here if they must.
2. **Mind map** — a mermaid `mindmap` of the question decomposition with
   inline verdicts; orientation at a glance. The thought graph in the
   appendix carries the edges.
3. **Background** — why the question matters, key terms, prior state.
   A few sentences; context the reader needs before the body, never a
   history dump. Ground it in what the user supplied at the ask — never
   invent motivation or prior state.
4. **Body** — one section per sub-question, flowing prose. Claims carry
   inline citation markers `[1]`, `[2]`; weak claims flagged inline
   `[3, weak]`. No restating the question, no transitions.
5. **Unresolved** — contradictions, weak claims, and pruned branches, one
   line each. A dropped branch nobody can see is a coverage hole.
6. **Appendix: thought graph** — mermaid; node labels = compressed
   sub-question + `[verdict]`; edges `spawns` / `merges` / `contradicts`;
   pruned nodes marked (`:::pruned` class or `[pruned]` in label).
7. **Sources** — numbered list mapping `[n]` to URL + confidence
   (`strong` = primary + corroborated; `weak` = single or secondary
   only). URLs appear here once, never inline.

## Reference files (load on demand)

- Writing the report → `references/report-template.md`

## Anti-patterns

- **Chain-as-graph** — sequencing dressed as branches.
- **Silent fan-out** — agents launched before the plan check; the user
  never saw what they're paying for.
- **Branch bloat** — spawning a child agent for a branch you could resolve
  with a direct fetch; a child costs roughly as much as the rest of the
  run.
- **Re-reading** — fetching pages a branch already read; compile from its
  findings and spot-check only what decides the root.
- **Ask-spam** — mode, breadth, and depth are one ask; three separate
  questions is a drip-feed.
- **Silent pruning** — a dropped branch nobody can see is a coverage hole.
- **Averaging contradictions** — "some say X, some say Y" without resolving
  authority.
- **Source laundering** — citing the blog that cited the docs.
- **Invented background** — motivation, prior state, or constraints the
  user never supplied, written as fact. If the user gave no background,
  write the section from the question alone or omit it.
- **Graph theater** — nodes nobody needed.
- **Report padding** — restating the question, narrative filler, sources
  listed twice.
