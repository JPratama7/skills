# New-skill design workflow

New skill / substantial-capability revision only; else capture outcome, run eval loop.

1. **Ground.** Find pain; ask 2–3 examples of inputs, deliverables, manual work. None → one focused question for a representative anonymized/synthetic example. No design before an example exists.
2. **Check coverage.** List candidates by name/description; per asset, tentatively reuse / extend / invoke / keep separate. Don't inspect unrelated implementations; don't imply inspection when only description is known.
3. **Confirm gap.** Recap pain, coverage, missing capability; ask if right. Stop before architecture.
4. **Analyze.** Extract steps, decisions, failure points. Mechanical work → deterministic scripts/validators; skill text for judgment/ambiguity.
5. **Compare.** 2–3 options; recommend one with deterministic coverage, model judgment, trade-offs, reused vs separate assets. Then table stakes, differentiators, anti-features.
6. **Sketch architecture.** Minimal. Per asset: responsibility, invocation, inputs, outputs, behavior on unavailable/malformed/inconclusive input. Separate confirmed interfaces from assumptions; defer nonessential work.
7. **Hand off.** Recap problem, examples, scope, architecture in chat/scratch; handoff file only if it aids resume/coordination.

Grill in rounds; recommended answer per question; look up discoverable facts instead of asking; validate major decisions before drafting. Per task: trigger context, desired output, objective vs subjective evaluation, target harness (default: current). Interview is done when an implementer could draft with zero remaining questions.
