# Evidence base

The research behind each `evidence:` tag in `SKILL.md`, distilled from the
`agent-prompting-arxiv.md` and `research-llm-overthinking.md` research notes.
Numbers are as reported by the papers' authors, not independent replications.
Use this file to justify a recommendation or answer a skeptical user — not to
stack citations into a finding the session doesn't support.

## External feedback

Self-correction without an external signal does not reliably improve reasoning
and often degrades it; the gains in reflection-style methods come from
consuming external feedback (env state, unit tests, tool results), not from
the critique text itself. This is why a mechanical violation becomes a
deterministic check rather than a written rule, and why "add a reviewer rule"
is the weaker fix whenever a check is buildable.

- Intrinsic self-correction does NOT reliably improve reasoning — Huang et
  al., "Large Language Models Cannot Self-Correct Reasoning Yet",
  arXiv:2310.01798
- Reflexion works *because it consumes external feedback* — Shinn et al.,
  arXiv:2303.11366
- CRITIC: verify output with external tools, then correct — Gou et al.,
  arXiv:2305.11738
- LATS: search + env feedback + self-reflection — Zhou et al.,
  arXiv:2310.04406
- At fixed compute, sampling more solutions + voting beats generative
  verification (~8x cheaper) — Singhi et al., arXiv:2504.01005

## Interface design

The agent-computer interface is a first-class variable, on par with prompt
wording: a small set of reliable actions, guardrails that reject malformed
edits, and concise specific feedback per step.

- SWE-agent ACI findings — Yang et al., arXiv:2405.15793
- Bare LLMs produce executable plans ~12% of the time; delegate planning and
  checking to solvers — Valmeekam et al., arXiv:2302.06706
- LLM+P: NL→formal planner→back beats LLM-alone (Blocksworld 90% vs 15-20%) —
  Liu et al., arXiv:2304.11477

## Position bias

Models use information at the beginning and end of the context window well
and significantly worse in the middle; answer-bearing material placed
mid-context can perform below a closed-book baseline. Critical rules belong
at the edges of steering files; reference material belongs in disclosed docs.

- Lost in the Middle — Liu et al., arXiv:2307.03172
- Attention sorting / recalibrating U-shaped attention (+10-15 pts RAG) —
  Peysakhovich & Lerer, arXiv:2310.01427; Hsieh et al., "Found in the
  Middle", arXiv:2406.16008

## Context load

Every always-loaded line spends context and attention every turn, and
irrelevant text actively degrades output — not merely wastes tokens. This
grounds the no-op hunt and the case for disclosed references.

- Irrelevant context dramatically degrades all tested prompting methods —
  Shi et al., arXiv:2302.00093
- Longer contexts degrade utilization even for long-context models — Liu et
  al., arXiv:2307.03172
- Interleaved thought-action-observation replays the whole context each
  step; decoupling planning from observations (ReWOO) cuts tokens ~5x —
  Xu et al., arXiv:2305.18323

## Spec failures

The largest empirical failure taxonomy for multi-agent systems puts spec
clarity, termination conditions, and output verification at the top. Applies
to subagent briefs, delegated tickets, and any agent-to-agent handoff;
structured artifacts between agents beat free-form chat.

- MAST: 14 failure modes — specification issues, inter-agent misalignment,
  missing/inadequate verification — Cemri et al., arXiv:2503.13657
- SOPs + role specialization + structured artifacts reduce cascading errors —
  Hong et al., MetaGPT, arXiv:2308.00352; Qian et al., ChatDev,
  arXiv:2307.07924

## Overthinking

Reasoning effort is a dial with a wrong setting on both ends: easy inputs
burn tokens on redundant solution rounds, while suppressing thought on hard
inputs produces underthinking. Concrete patterns beat vague "be brief", and
doubt-cue vocabulary ("wait", "verify", "reconsider") causally inflates
reasoning length. Provider effort parameters are the first-class knob for
reasoning quantity; prompting owns direction and output verbosity.

- Overthinking concentrates on easy problems — Chen et al.,
  arXiv:2412.21187; compute-optimal scaling is difficulty-dependent,
  arXiv:2408.03314
- s1 budget forcing: "Wait" extends thinking, delimiters cut it — a
  bidirectional dial — arXiv:2501.19393; injected "wait" tokens invoke
  long-CoT behavior, arXiv:2505.17697
- "Be concise" + step-by-step: ~−49% length, negligible MCQA loss, but −28%
  math on weak models — arXiv:2401.05618
- Chain of Draft: parity accuracy at 7.6–20% of CoT tokens —
  arXiv:2502.18600; TALE budgets, arXiv:2412.18547; too-tight budgets
  backfire
- Underthinking: premature thought-switching on hard problems correlates
  with wrong answers — arXiv:2501.18585
- Effort params are API-enforced ceilings (`reasoning_effort`, thinking
  budget/level); providers recommend raising effort rather than prompting
  around it — OpenAI/Anthropic/Gemini docs
- Inverse scaling: longer reasoning actively degrades accuracy on
  distractor-rich tasks — arXiv:2507.14417

## Unfaithful self-reports

An agent's written reasoning is not a causal log: biasing features change
answers while the generated rationale never mentions them. Verify the output
and the artifacts, never the self-explanation — including when reading
session logs during a session debrief.

- Turpin et al., "Language Models Don't Always Say What They Think",
  arXiv:2305.04388

## Externalized memory

Long-running agents need memory outside the prompt: a stored event stream
retrieved by relevance/recency/importance beats dumping all history into
context, which "distracts the model". Grounds teed logs, memory files, and
read-only service access as session-debrief findings.

- Generative Agents memory/retrieval/reflection ablations — Park et al.,
  arXiv:2304.03442
- Voyager's skill library: compounding capability via stored, retrievable
  artifacts — Wang et al., arXiv:2305.16291

## Personas

Persona prose does not reliably improve objective performance — the largest
controlled study (162 roles × 4 model families) found no gain, and assigned
personas can degrade reasoning. Where role prompts help, they act as an
implicit CoT trigger, not activated expertise. Keep roles short and
functional; cut biographies.

- Zheng et al., "When 'A Helpful Assistant' Is Not Really Helpful" (v3
  reversal after scaling) — arXiv:2311.10054
- Persona is a double-edged sword (hurt on 7/12 datasets) — Tseng et al.,
  arXiv:2408.08631
- Role-play gains act as implicit CoT trigger — Kong et al.,
  arXiv:2308.07702

## Prompts are empirical

Semantically equivalent phrasings swing accuracy by tens of points and do
not transfer across models; the best wording is found by search, not
design. A session debrief should propose wording changes as hypotheses with a
measurement plan, not as asserted improvements.

- Format sensitivity: up to 76-point swings; weak cross-model transfer —
  Sclar et al., arXiv:2310.11324
- Example order alone swings SOTA↔random; model-specific — Lu et al.,
  arXiv:2104.08786
- OPRO: best phrasing is found, not designed — Yang et al.,
  arXiv:2309.03409; APE, arXiv:2211.01910; ProTeGi, arXiv:2305.03495
