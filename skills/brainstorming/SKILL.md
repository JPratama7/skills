---
name: brainstorming
version: 1.2.1
description: Brainstorm an idea, feature, product, or system from multiple angles before committing to a direction. Use whenever the user wants to explore options, think through a problem, "brainstorm", "ideate", "help me think about", "what are my options for", "explore approaches to", or is about to design something and hasn't settled the shape yet. Also trigger when the user has a vague goal and needs help turning it into something concrete — whether that ends up as an explanatory doc, a PRD, a system design, or a simple writeup. The output format is flexible and chosen with the user at the end.
---

# Brainstorming

Turn a vague idea into a well-understood problem with a chosen direction and a concrete artifact. The artifact's shape is not fixed up front — it could be an explanatory note, a PRD, a system design, or a one-page writeup. You decide the shape *with the user* after the brainstorming converges, not before.

## Why this skill exists

Most brainstorming fails one of two ways: jumping to the first plausible idea, or listing options forever without committing. The three-phase shape — probe, diverge, converge — forces a direction the user chose for stated reasons.

## Session flow

Work through these phases in order. Each phase has an explicit exit condition. Do not skip ahead.

### Phase 1 — Probe (Socratic)

Goal: surface the user's real goal, constraints, and unstated assumptions before any options are generated.

Ask 3–5 sharp questions, one or two at a time (not a wall). Prioritize:

- **The real goal:** "When this is done, what's different in the world?" Distinguish the stated task from the underlying outcome. A user who says "I want to build a notification system" often really wants "users come back without me emailing them."
- **Constraints:** time, budget, team size, must-keep integrations, things they refuse to do.
- **Audience / stakeholders:** who is this for, who decides, who is affected.
- **Success signal:** how will they know it worked in 3–6 months.
- **What they've already ruled out and why** — this reveals hidden assumptions faster than asking about assumptions directly.

Exit when you can state the problem back in one sentence and the user agrees that's actually the problem. If you can't, keep probing — don't move on with a fuzzy frame.

### Phase 2 — Diverge (frameworks)

Goal: generate a wide spread of genuinely different directions, not variations on one theme.

Apply at least two of these frameworks explicitly (name them so the user can follow the reasoning):

- **First-principles:** strip the problem to its irreducible constraints, then rebuild from there. Useful when the user is anchored to an existing solution shape.
- **Inversion:** ask "how would I guarantee this fails?" then flip each failure into a design constraint. Good for risk-heavy problems.
- **Jobs-to-be-done:** frame the user as "hiring" the solution to make progress on a job. Good when the user is feature-focused but the real value is an outcome.
- **SCAMPER:** Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse. Good when there's an existing thing to evolve.
- **Steelman the rejected option:** take something the user dismissed early and argue its case as strongly as possible. Surfaces whether the dismissal was reasoning or reflex.
- **Constraint removal:** "what would this look like if [hard constraint] didn't exist?" — then walk back to feasibility. Loosens fixation.

For each direction, give: a one-line name, 2–3 sentences on the core idea, the strongest argument *for* it, and the strongest argument *against* it. The "against" matters as much as the "for" — directions without honest weaknesses are underexplored.

Aim for 4–6 genuinely distinct directions, not 10 slight variations. Two directions that differ only in implementation detail count as one.

Exit when the user has reacted to the spread — pushed back, picked favorites, or asked to combine elements. Their reaction is the signal that enough ground is covered.

### Phase 3 — Converge

Goal: pick a direction (or a synthesis) and turn it into a concrete artifact.

1. Reflect the user's reactions back: which directions excited them, which they rejected, which elements they wanted to combine.
2. Propose 1–2 synthesis options if no single direction won. A synthesis is not a kitchen-sink — it's a specific combination with a reason.
3. Once a direction is chosen, **ask the user what artifact they want**. Present 3–5 format options with a one-line description of each, tailored to the topic. Common options:
   - **Explanatory doc** — explains the idea and the reasoning to a reader (teammate, future self, stakeholder).
   - **PRD** — product requirement doc: problem, users, solution, success criteria, scope, risks.
   - **System design** — architecture, components, data flow, trade-offs, open questions.
   - **One-pager / decision memo** — the decision, alternatives considered, why this one, what's next.
   - **Plain writeup** — unstructured notes capturing the conclusion and the why.
   - Let the user name a different format if none fit.
4. Produce the artifact in the chosen format, grounded in everything surfaced in phases 1–2. It should read as if the brainstorming already happened — the artifact is the *output*, not a re-narration of the process.
5. End with an explicit "what's next" — the smallest concrete step that moves this forward.

## Token discipline

The session shape costs tokens; keep it lean without cutting substance. Terse ≠ thin — cut redundancy and narration, never decision-bearing detail: risks, evidence, and mechanism-level specifics stay in.

- Say it once. Don't recap the user's answers back at length — one line of confirmation, then move.
- Keep probe questions to a line or two each. Directions stay compact: name, core idea, strongest for, strongest against — no preamble, no summary paragraph.
- Detour returns are summaries — the minimum that grounds the next step, not the companion skill's full output.
- Reference files load only when their trigger fits — never "just in case".

## Companion skills

The probe-diverge-converge core is yours — never route it. Some moments call for a specialist, though. When a trigger fits, invoke the named skill through your harness's skill mechanism, then come back — a routing is a detour, not a hand-off. If the skill isn't installed, note that and do a lean version inline rather than blocking.

### In-session detours

| Trigger | Skill | What it brings back |
|---|---|---|
| The user's *decision* hinges on facts they can't supply — they'd pick differently depending on what competitors, the market, or prior art actually look like | `research` | Cited findings that ground the divergence |
| The brainstorm is converging on an API, module, or interface shape | `design-an-interface` | Parallel radically-different designs to fold into the option spread |
| The problem is adversarial — a conflict, negotiation, or opponent to outmaneuver | `perspective-reversal` | The opponent's likely moves and your counters |
| A direction hinges on a question a throwaway build answers cheaper than debate ("would this flow feel right?") | `prototype` | A working sketch that resolves the question. Offer first — a mid-session build needs a yes |
| The leading direction is high-stakes and the user wants it attacked before committing | `discussion` | Counterarguments that stress-test the pick |

One detour at a time. When it returns, resume the phase you left.

Relevance isn't enough — nearly any brainstorm touches facts someone could look up. Route when the pick would change with the answer. When a fact is merely nice-to-have, fold it into the direction as a flagged assumption ("unverified: whether gyms allow this") and keep moving instead of pausing the session to offer a detour.

### After the artifact

Brainstorming ends at the artifact. These carry the user forward — offer them, don't auto-run:

| Trigger | Skill |
|---|---|
| They want a format outside the list — report, RCA, tracker ticket, PR description | `doc-builder` |
| The initiative is big enough to need a full PRD build-out | `prd-development` |
| "So what are the actual steps" | `planning` |
| Steps with deadlines and reminders | `actionize` |

## Hard rules

- **Never produce the artifact before phase 3.** Producing a doc mid-brainstorm anchors the user to whatever shape it took.
- **Every direction needs an honest weakness.** "Weakness: hard to implement" is not honest — *what* is hard about it, and *why*?
- **Don't generate more than 6 directions.** A long list is avoidance of choosing. If you can't find 4 genuinely distinct ones, say so — that's diagnostic, not a failure.
- **The user picks the direction, not you.** You can recommend with reasons, but the choice is theirs. If they ask you to decide, give a clear recommendation and the one reason it wins — then confirm.
- **Name the frameworks you're using.** Silent frameworks are just you thinking out loud; named frameworks let the user reuse the method later.
- **One sentence problem statement before diverging.** No exceptions. A fuzzy frame produces fuzzy options.
- **Ask, don't assume, the output format.** Even when the topic strongly implies a format, confirm — the user may want a one-pager when you'd default to a PRD.
- **Routing is a detour, not a hand-off.** After a companion skill returns, resume the phase you were in. The session shape stays yours — companions do specialist work, they don't run the brainstorm.
- **Route or admit, never fabricate.** If the *decision* hinges on facts you don't have and can't derive, either run the `research` detour or say plainly that the fact is missing. If the fact is only nice-to-have, flag it as an unverified assumption and move on. Invented market numbers and fake competitor names poison every direction built on them.

## Anti-patterns to catch in yourself

- Generating options that all share the same hidden assumption (e.g. all assume a certain tech stack). Name the shared assumption and break it explicitly.
- Treating the user's first stated goal as the real goal. It usually isn't.
- Long flat lists of options with no recommendation, no weaknesses, no synthesis. This is brainstorming theater.
- Producing a polished artifact that papers over an unresolved decision. If a decision is still open, say so in the artifact and flag it.
- Skipping the probe because the user "already explained it." The probe is where the real problem gets found.
- Doing a specialist's job badly instead of routing — guessing at the competitive landscape or hand-waving an adversary's moves are exactly what the companion table is for.

## Reference files (load on demand)

- User wants to brainstorm a product/feature and may need PRD structure → `references/prd-template.md`
- User wants to brainstorm a system/architecture and may need design doc structure → `references/system-design-template.md`
- Diverge phase stalling — not generating genuinely distinct directions → `references/divergence-prompts.md`
- User is stuck in one frame and won't consider alternatives → `references/reframe-techniques.md`
