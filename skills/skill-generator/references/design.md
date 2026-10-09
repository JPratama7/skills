# New-skill design workflow

Use this only for a new skill or a revision that adds a substantial capability. For ordinary improvements, capture the requested outcome and run the eval loop.

1. **Ground the problem.** Identify the pain point and ask for 2–3 concrete examples of inputs, deliverables, or manual work. If none exist, ask one focused question for a representative anonymized or synthetic example. Do not design or draft before there is an example to analyze.
2. **Check relevant coverage.** Inspect names and descriptions of likely skills/tools in the current repository or harness. For each plausible asset, decide tentatively whether to reuse, extend, invoke, or keep separate. Do not inspect unrelated implementations or imply an asset was inspected when only its description is known.
3. **Confirm the gap.** Summarize pain, coverage, and missing capability; ask whether that gap is correct. Stop for confirmation before proposing architecture.
4. **Analyze examples.** Extract repeated steps, decisions, and failure points. Make mechanical work deterministic with scripts or validators where practical; reserve skill instructions for judgment and ambiguity.
5. **Compare approaches.** Offer 2–3 options, recommend one, and state deterministic coverage, model judgment, trade-offs, and reused/separate assets. After selection, define table stakes, differentiators, and anti-features.
6. **Sketch minimal architecture.** State each asset's responsibility, invocation, inputs, outputs, and behavior for unavailable, malformed, or inconclusive inputs. Separate confirmed interfaces from assumptions; defer nonessential work.
7. **Hand off to drafting.** Recap the agreed problem, examples, scope, and architecture briefly in chat or scratch. Create a handoff file only if it helps resume or coordinate work.

Ask only for missing information. Prefer one focused question at a time; validate major decisions before drafting. For every task, identify trigger context, desired output, objective vs subjective evaluation, and target harness (default to the current harness).