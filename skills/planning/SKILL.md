---
name: planning
version: 1.0.0
description: Turn any goal into a concrete, executable plan. Covers three planning styles — coding/engineering plans, personal/task plans, and agile sprint plans — and picks the right one for the situation. Use whenever the user asks to "make a plan", "plan this out", "break this down into steps", "what are the next steps", "how do I start", "create a roadmap", "scope this project", or describes work that needs organizing before it starts — even if they never say the word "plan". Produces the plan only; execution is a separate step.
---

# Planning

## Prime directive

Produce the plan; do not execute it. The plan's job is to be specific enough that anyone — a fresh session, another agent, a coworker, or future you — can execute it without the conversation that produced it. After delivering the plan, stop and wait for the user to decide what happens next.

## Session flow

Work through these phases in order, but keep the interview tight — ask only what the plan actually depends on, and infer the rest:

1. **Interview.** Establish: the goal (what success looks like), the deadline or time budget, what already exists, and what's blocking or unknown. One or two questions usually suffice; don't interrogate.
2. **Pick the mode.** Match the situation to a planning style and load its reference file:
   - Engineering work (features, refactors, migrations, repos) → `references/coding.md`
   - Personal or project tasks (side projects, life goals, errands, multi-step chores) → `references/personal.md`
   - Team or sprint work (backlog, capacity, iteration planning) → `references/agile.md`
   - If the domain is ambiguous, ask the user which mode fits — or plan in the general style below.
3. **Ask where the plan should live.** The user may want it as a markdown file (suggest `.plan/<topic>.md` or `plans/` unless they name a location), inline in chat, or both. If they don't care, default to a file — plans are for later, and files survive context loss.
4. **Gather context.** For coding plans this means reading the actual code (see `references/coding.md`). For personal and agile plans it means pinning down deadlines, capacity, and dependencies. Never invent facts about the codebase or the team; ask or look.
5. **Write the plan.** Follow the task anatomy below and the mode-specific structure in the reference file. Order steps by dependency, mark which can run in parallel, and surface unknowns as explicit questions rather than burying them.
6. **Present and confirm.** Show the plan and ask: "Does this cover everything? Any task that's unclear or needs breaking down further?" Revise based on the answer. Then stop — do not start executing unless explicitly asked.

## The task anatomy (all modes)

The difference between a plan that works and one that doesn't is specificity. "Set up the codebase" is not a task; "Fork the repo, install dependencies with `pnpm install`, run `pnpm test` to confirm the baseline, record the output" is. Every task in every mode must include:

- **Action** — a verb + object ("implement X", "write Y", "call Z")
- **What's involved** — the exact files, repos, commands, people, or resources
- **Verify** — how you know it's done, concretely ("tests pass", "page loads with no console errors", "contact replies")
- **Time** — an honest estimate. Use hours, not vague "days"; if a task takes more than a day, break it down further.

## Anti-patterns: what makes a bad plan

If you catch yourself writing any of these, stop and fix it:

- **Milestones instead of tasks** — "Week 1: build the model" tells the executor nothing. Break it down.
- **Tasks without verification** — "set up environment" with no way to confirm success.
- **Tasks that depend on unknowns without surfacing them** — "get the lab data" when you don't know who has it or whether it's been requested. An unknown isn't a task; it's a question for the user.
- **No time estimates** — a plan with no sense of scale can't be prioritized or scheduled.
- **Hiding assumptions** — state them explicitly ("assumes read access to the vendor API") so a wrong assumption surfaces early instead of failing mid-execution.
- **Over-planning** — if the whole thing is one sitting's work, a two-line checklist beats a five-page plan. Match the depth to the size.

## Reference files (load on demand)

- Engineering work: features, refactors, migrations, anything involving a codebase → `references/coding.md`
- Personal or project tasks: side projects, life goals, multi-step personal work → `references/personal.md`
- Team/sprint work: backlog, capacity, iterations → `references/agile.md`
