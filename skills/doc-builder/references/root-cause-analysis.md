# Root cause analysis

Blameless, factual account of a failure: what happened, why, and what prevents recurrence. Readers are engineers who were not there and reviewers checking that prevention is real.

Default voice is first person. "I deployed", "I noticed", "I rolled back". The author owns the timeline. State your own actions as facts without fault language, and name systems, not people, for causes. If the user asks for another voice, use that instead.

## Workflow

The script owns structure, the writer owns prose. Never hand-write the markdown. In the commands below, `<skill-dir>` is the directory holding this skill's `SKILL.md`.

1. **Interview the user.** Ask the questions below in one batch. Skip what the conversation already answers and state what you inferred instead. Anything still unknown becomes a `TODO:` marker in the draft, never an invented fact.
2. **Write the draft** as a Python file that builds an `RCA`. Start from `python3 <skill-dir>/scripts/rca.py scaffold -o draft.py` for the empty form, or `python3 <skill-dir>/scripts/rca.py example -o draft.py` for a filled one to copy.
3. **Render**: `python3 <skill-dir>/scripts/rca.py render draft.py -o rca-<slug>.md`. The script emits the sections the draft actually supports, so an empty section never reaches the document. Wrong field types fail here, before any markdown is written.
4. **Check**: `python3 <skill-dir>/scripts/rca.py check rca-<slug>.md`. Exit code 2 means findings. Fix every finding and rerun until it is clean. A document whose `Status` metadata reads `Draft` may carry `TODO:` markers; a `Final` document may not. Use `--draft` to force draft handling when the status line is missing.
5. **Run the prose gate**: `python3 <skill-dir>/scripts/slop_check.py rca-<slug>.md`. Fix every hit.
6. **Save** the markdown file, named after the incident (`rca-payment-outage-2026-09.md`).

## Failure types

The same draft covers all three. What changes is which optional sections carry information.

| Type | Symptom | Extra sections that usually matter | Not applicable |
|------|---------|------------------------------------|----------------|
| Incident | Users hit a live failure | Timeline, Detection, Contributing factors | none |
| Bug | A defect reached users or staging | Detection, Lessons learned | Timeline (use the deploy that carried it) |
| Process | A handoff, approval, or step broke down | Contributing factors, Lessons learned | Timeline, Detection |

A type is not a template. Use one draft shape and drop the fields the failure has nothing to say about. The script does this automatically: an empty field produces no section.

## Interview questions

Ask all that are not already answered by context:

1. What happened? User-visible symptom, when it started, how it was detected.
2. What was the blast radius? Affected users or systems, duration, data or revenue loss.
3. Timeline, for incidents. Trigger, detection, mitigation, resolution.
4. Root cause. The mechanism, not "a bad deploy". If unknown, what is suspected and what would confirm it?
5. Contributing factors. What made it possible or worse: missing test, missing alert, unsafe default, config drift.
6. How was it resolved? The immediate mitigation, and the fix that removed the cause.
7. Action items. Prevent, Detect, or Mitigate, with owners and due dates.
8. Severity or incident level, if the org uses levels.
9. Which failure type is this: incident, bug, or process?

## The draft

The draft is a Python file. It imports the dataclasses from `rca` and builds one `RCA`. Field types are enforced at render time, so a wrong type fails with a clear message instead of rendering a broken document.

```python
from rca import ActionItem, Factor, Metadata, Notice, RCA, Resolution, RootCause, TimelineEntry

doc = RCA(
    # --- required ---
    title="<short incident title>",
    intro="<one or two plain sentences: what happened and why this RCA exists>",
    notice=Notice(
        audience="<who needs to read this>",
        what="<incident and scope in one sentence>",
        action="<review, decide, note, or nothing>",
        skip_if="<legitimate exit condition, or None>",
    ),
    summary="<2-3 sentences: what broke, who was affected, current state>",
    impact="<blast radius, quantified>",
    root_cause=RootCause(
        statement="<the mechanism, in one or two sentences>",
        method="five-whys",
        chain=["<link 1>", "<link 2>", "<link 3>"],
        factors=[Factor(name="<factor>", contribution="<how it contributed>")],
    ),
    resolution=Resolution(
        mitigation="<what stopped the bleeding>",
        fix="<what removed the cause>",
    ),
    action_items=[
        ActionItem(action="<item>", type="Prevent", owner="<owner>", due="YYYY-MM-DD"),
    ],
    # --- optional ---
    metadata=Metadata(
        date="YYYY-MM-DD",
        severity="SEV-2",
        duration="45 minutes (14:02 to 14:47 UTC)",
        status="Draft",
        authors=["<name>"],
    ),
    timeline=[
        TimelineEntry(time="14:02", event="<trigger>"),
    ],
    contributing_factors=["<condition that allowed or amplified it>"],
    detection="<how it surfaced, how fast, what the signal missed>",
    lessons_learned="<what went well, what was lucky, what would have helped>",
)
```

The dataclass signature marks what is required: a field with no default must be passed, and it must carry content. A field with a default is optional; leave it empty and its section does not appear in the document.

Field notes:

- Required fields are the ones with no default in the dataclass: `title`, `intro`, `notice`, `summary`, `impact`, `root_cause`, `resolution`, `action_items`. Every other field is optional; leave it empty and its section does not appear in the document.
- `metadata` rows are omitted individually when unknown. Do not write "Unknown" to fill a slot.
- `impact` and `lessons_learned` accept a string or a list of strings.
- `resolution` takes a `mitigation` and a `fix`. Always separate the two when both are known: mitigation stopped the bleeding, fix removed the cause.
- `action_items` entries take `action`, `type`, `owner`, `due`. `type` is one of `Prevent`, `Detect`, `Mitigate`. `Prevent` maps to the root cause, `Detect` and `Mitigate` map to contributing factors.
- `root_cause.method` selects how the chain is rendered. See below.
- The draft must build the document into a variable named `doc`.

## Required fields

A required field has no default in the dataclass, so the draft must pass it, and it must carry content. Omitting one is a `TypeError` at construction; passing an empty one is reported before rendering.

| Field | Requirement | Reported as |
|-------|-------------|--------------|
| `title` | Non-empty | "title is required" |
| `intro` | Non-empty prose | "intro is required" |
| `notice` | All four of `audience`, `what`, `action`, `skip_if` non-empty | "notice.audience is required" (and the same for each) |
| `summary` | Non-empty | "summary is required" |
| `impact` | Non-empty | "impact is required" |
| `root_cause.statement` | Non-empty, at least 25 characters, and a mechanism rather than a trigger | "root_cause.statement is required" / "too short to state a mechanism" / "names a trigger, not a mechanism" |
| `resolution` | `mitigation` or `fix` present | "resolution needs a mitigation or a fix" |
| `action_items` | Each entry needs `action`, a `type` of Prevent/Detect/Mitigate, an `owner`, and a `due` | "action_items[1].type is required" / "has type 'Fix'; use Prevent, Detect, or Mitigate" / "has no owner" / "has no due date" |

Optional: `metadata` (all rows), `timeline`, `contributing_factors`, `detection`, `lessons_learned`, `root_cause.chain`, `root_cause.factors`.

An empty `action_items` list renders the section as "No action items." and passes. Say so deliberately, not by omission.

Two rules apply to the whole document rather than one field:

- A `TODO:` marker is only allowed when `metadata.status` is `Draft`. Set the status to `Final` when the RCA is complete.
- The root cause statement must stay blameless. It fails if it says human error, operator error, someone, went wrong, failed to work, be more careful, more vigilant, or avoid this in future.

## Analysis methods

Pick one. The method changes how `chain` and `factors` are used, not which sections appear.

**`five-whys`** (default). `chain` is a list of links in 5-whys order: the symptom first, then each link explaining the one before it, ending at the root cause. Rendered as a numbered list in that order, plus a Mermaid flowchart that runs the other way, from cause to effect. Use when one dominant causal chain explains the failure.

**`fault-tree`**. `chain` stays the linear spine; `factors` adds the branches that contributed weight to it. Rendered as a contributions table. Use when several independent conditions combined, and one link alone does not explain the failure.

**`none`**. `chain` is omitted and the statement stands alone. Use only when the failure is genuinely a single-step fact with no chain to trace.

## What the script checks

`rca.py check` fails with exit code 2 on any of these:

- Missing title, missing Attention Conservation Notice, a missing or empty notice line, or a missing plain intro before the notice.
- A missing required section: Summary, Impact, Root cause, Resolution, Action items.
- An empty section, or one holding only a stub such as "N/A" or "TBD".
- A `TODO:` marker in a document whose `Status` metadata is not `Draft`. Set the status to `Draft` while the RCA is still in progress.
- A root cause statement under 25 characters, or one that says human error, operator error, someone, went wrong, failed to work, be more careful, more vigilant, or avoid this in future.
- A root cause statement that names a trigger with no chain behind it, such as "the deploy broke it".
- A Mermaid block with no flowchart declaration, an unbalanced quote, an edge to an undefined node, or fewer than two nodes.
- A Mermaid diagram that starts at the symptom, so the flowchart points backwards at the root cause.
- A timeline that runs backwards, or a row whose timestamp cannot be read. Overnight incidents need explicit dates, `YYYY-MM-DD HH:MM`.
- An action item with a type outside Prevent, Detect, and Mitigate, or with a missing owner or due date.

`rca.py render` fails before writing any markdown when the draft has a wrong field type, an unknown `method`, a syntax error, or no `doc` variable.

## Quality bar

- Root cause is a mechanism, not an event. Test: could you fix it with one action item? If the fix is "be more careful", dig deeper.
- The causal chain is a Mermaid `flowchart`, not ASCII arrows. Mermaid renders in every doc viewer, ASCII art does not.
- Timeline is sourced from logs, alerts, and deploy history, not reconstructed from memory alone.
- Every action item has a type and an owner. Name a person or team, not "the team".
- Blameless throughout. The failure is in the system, not the operator.
- The intro and notice carry the reader's decision. Everything else is evidence for it.

Contrast, for the `statement` field:

- Weak: "The deploy broke the checkout service."
- Strong: "The checkout service stopped responding because the released migration dropped the index the payment lookup depended on, so every payment query scanned the full table."

Both are one sentence. Only the second survives the validator and tells a reader what to fix.

## Filling this in by hand

A human can write the same draft and run the same two commands. The draft is the form; the markdown is the output. Run `python3 scripts/rca.py example -o draft.py` for a filled example to edit.
