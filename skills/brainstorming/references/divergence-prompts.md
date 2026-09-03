# Divergence Prompts

Load when Phase 2 is stalling — you're generating options that feel like variations of the same idea, or the spread isn't wide enough.

## Diagnose the stall

First, figure out *why* the options are converging:

- **Anchored to one solution shape?** All options assume the same architecture / approach / tool. → Run first-principles: list the irreducible constraints, then ask "what's the simplest thing that satisfies only these?"
- **Anchored to one constraint?** All options respect a constraint the user stated, but that constraint might be softer than they think. → Run constraint removal: "what if [constraint] didn't exist?" then walk back.
- **Only varying implementation detail?** Options differ in *how* but not *what*. → Run jobs-to-be-done: reframe around the outcome the user is hiring the solution for, then generate options that achieve that outcome differently.
- **Only safe options?** Everything generated is reasonable and boring. → Run inversion: "how would I guarantee this fails?" then flip each failure into a design. Or steelman the option the user dismissed fastest.

## Re-framing moves

If the frameworks above aren't breaking the stall, try changing the *frame* of the problem:

- **Change the timescale:** "what's the 1-week version? the 1-year version?" — the gap between them reveals what's essential vs. what's ambition.
- **Change the actor:** "what if the user wasn't a person but a cron job / another system / a non-technical stakeholder?" — surfaces assumptions about who does what.
- **Change the scope of the problem:** "what if this were 10x bigger? 10x smaller?" — reveals whether the current shape scales or is accidental.
- **Invert the goal:** "what would make this problem *worse* / more interesting / someone else's problem?" — sometimes the right move is to reframe the problem, not solve the stated one.

## When to stop diverging

Stop when you have 4–6 options that a reader would describe as genuinely different approaches, not "variations on X." If after the moves above you still can't get there, say so — it may mean the problem is narrow enough that 2–3 real options is the honest answer, and that's fine.
