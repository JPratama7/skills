#!/usr/bin/env python3
"""doc-builder RCA generator and validator.

    rca.py scaffold -o draft.py    blank draft to fill in
    rca.py example -o draft.py     filled example draft to copy
    rca.py render draft.py -o out.md   draft -> markdown RCA
    rca.py check out.md            structural and judgment checks

The draft is a Python file that builds an RCA dataclass. The script owns
section presence and structure; the writer owns the prose in each field.

check enforces what prose review misses: required sections, empty stubs,
Mermaid validity, action-item typing and ownership, timeline chronology, and
root-cause statements that name a trigger or a person instead of a mechanism.
"""
import argparse
import dataclasses
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Union

# A draft may import these by name. Registering this module under "rca" keeps
# the imported classes identical to the ones defined here, so type checks hold.
sys.modules.setdefault("rca", sys.modules[__name__])

# ---------- the document model ----------

Text = Union[str, list[str]]


@dataclass
class Metadata:
    date: str = ""
    severity: str = ""
    duration: str = ""
    status: str = ""
    authors: list[str] = field(default_factory=list)


@dataclass
class Notice:
    """All four lines are required; an empty one is reported."""

    audience: str
    what: str
    action: str
    skip_if: str


@dataclass
class TimelineEntry:
    time: str = ""
    event: str = ""


@dataclass
class Factor:
    name: str = ""
    contribution: str = ""


@dataclass
class RootCause:
    """`statement` is required. `method` and the chain are optional."""

    statement: str
    method: str = "five-whys"
    chain: list[str] = field(default_factory=list)
    factors: list[Factor] = field(default_factory=list)


@dataclass
class Resolution:
    """At least one of `mitigation` or `fix` is required."""

    mitigation: str = ""
    fix: str = ""


@dataclass
class ActionItem:
    """All four fields are required; an empty one is reported."""

    action: str
    type: str
    owner: str
    due: str


@dataclass
class RCA:
    """One RCA document.

    Fields with no default are REQUIRED: the draft must pass them, and they
    must carry content. A required field left blank is reported by
    `validate_required` before anything renders.

    Fields with a default are OPTIONAL. Leave one empty and its section does
    not appear in the document.
    """

    # --- required ---
    title: str
    intro: str
    notice: Notice
    summary: str
    impact: Text
    root_cause: RootCause
    resolution: Resolution
    action_items: list[ActionItem]
    # --- optional ---
    metadata: Metadata = field(default_factory=Metadata)
    timeline: list[TimelineEntry] = field(default_factory=list)
    contributing_factors: list[str] = field(default_factory=list)
    detection: str = ""
    lessons_learned: Text = ""


DRAFT_NAMES = {
    "RCA": RCA,
    "Metadata": Metadata,
    "Notice": Notice,
    "TimelineEntry": TimelineEntry,
    "Factor": Factor,
    "RootCause": RootCause,
    "Resolution": Resolution,
    "ActionItem": ActionItem,
}

# ---------- section registry ----------

REQUIRED_SECTIONS = [
    "Summary",
    "Impact",
    "Root cause",
    "Resolution",
    "Action items",
]

OPTIONAL_SECTIONS = [
    "Timeline",
    "Contributing factors",
    "Detection",
    "Lessons learned",
]

EMPTY_STUBS = {"n/a", "na", "none", "tbd", "tba", "-", "--", "not applicable"}

WEAK_CAUSE_PATTERNS = [
    (r"\bhuman error\b", "names human error instead of a system mechanism"),
    (r"\boperator error\b", "names operator error instead of a system mechanism"),
    (r"\bsomeone\b", "names a person instead of a system mechanism"),
    (r"\bwent wrong\b", "says the thing went wrong instead of what made it happen"),
    (r"\bfailed to work\b", "says the thing failed instead of what made it fail"),
    (r"\bbe more careful\b", "asks for care instead of a fix"),
    (r"\bmore careful\b", "asks for care instead of a fix"),
    (r"\bvigilant\b", "asks for vigilance instead of a fix"),
    (r"\bavoid (this|it) in (the )?future\b", "asks for avoidance instead of a fix"),
    (r"\bprocess (was not )?followed\b", "names a process gap without the mechanism"),
]

TRIGGER_AS_CAUSE_PATTERNS = [
    r"^(the |a |our )?(deploy(ment)?|release|rollout|update|change|config(uration)?)",
    r"\b(because|due to|caused by|caused the) (the |our |a )?(deploy(ment)?|release|rollout|update|change|config(uration)?)",
]

VALID_ACTION_TYPES = {"prevent", "detect", "mitigate"}

VALID_METHODS = {"five-whys", "fault-tree", "none"}


def die(msg, code=1):
    print(f"rca.py: {msg}", file=sys.stderr)
    sys.exit(code)


# ---------- draft loading ----------

def load_draft(path):
    """Load a draft Python file and return the RCA it builds."""
    if not os.path.isfile(path):
        die(f"draft file not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        source = fh.read()
    namespace = dict(DRAFT_NAMES)
    try:
        exec(compile(source, path, "exec"), namespace)
    except Exception as exc:
        die(f"could not load {path}: {type(exc).__name__}: {exc}")
    doc = namespace.get("doc")
    if doc is None:
        for value in namespace.values():
            if isinstance(value, RCA):
                doc = value
                break
    if doc is None:
        die(f"{path} does not build an RCA. Name it: doc = RCA(...)")
    if not isinstance(doc, RCA):
        die(f"{path} builds a {type(doc).__name__}, not an RCA")
    return doc


def check_types(doc):
    """Catch field values of the wrong shape before rendering."""
    problems = []
    if not isinstance(doc.title, str):
        problems.append("title must be a string")
    if not isinstance(doc.summary, str):
        problems.append("summary must be a string")
    if not isinstance(doc.impact, (str, list)):
        problems.append("impact must be a string or a list of strings")
    if not isinstance(doc.timeline, list) or any(
        not isinstance(entry, TimelineEntry) for entry in doc.timeline
    ):
        problems.append("timeline must be a list of TimelineEntry")
    if not isinstance(doc.action_items, list) or any(
        not isinstance(item, ActionItem) for item in doc.action_items
    ):
        problems.append("action_items must be a list of ActionItem")
    if not isinstance(doc.contributing_factors, list) or any(
        not isinstance(item, str) for item in doc.contributing_factors
    ):
        problems.append("contributing_factors must be a list of strings")
    if not isinstance(doc.root_cause, RootCause):
        problems.append("root_cause must be a RootCause")
    elif doc.root_cause.method not in VALID_METHODS:
        problems.append(
            f"root_cause.method is {doc.root_cause.method!r}; "
            "use five-whys, fault-tree, or none"
        )
    elif doc.root_cause.factors and any(
        not isinstance(factor, Factor) for factor in doc.root_cause.factors
    ):
        problems.append("root_cause.factors must be a list of Factor")
    if not isinstance(doc.resolution, Resolution):
        problems.append("resolution must be a Resolution")
    if not isinstance(doc.notice, Notice):
        problems.append("notice must be a Notice")
    if not isinstance(doc.metadata, Metadata):
        problems.append("metadata must be a Metadata")
    if problems:
        for problem in problems:
            print(f"rca.py: {problem}", file=sys.stderr)
        sys.exit(2)


def validate_required(doc):
    """Report required fields that were passed but left empty.

    The dataclass signature marks which fields are required, so a missing
    one is a TypeError at construction. This catches the subtler case: a
    required field that was passed as an empty string or an empty list.
    """
    problems = []

    def blank(value):
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, list):
            return not value
        return False

    if blank(doc.title):
        problems.append("title is required")
    if blank(doc.intro):
        problems.append("intro is required")
    if blank(doc.summary):
        problems.append("summary is required")
    if blank(doc.impact):
        problems.append("impact is required")
    if blank(doc.root_cause.statement):
        problems.append("root_cause.statement is required")
    if blank(doc.resolution.mitigation) and blank(doc.resolution.fix):
        problems.append("resolution needs a mitigation or a fix")
    for key in ("audience", "what", "action", "skip_if"):
        if blank(getattr(doc.notice, key)):
            problems.append(f"notice.{key} is required")
    for index, item in enumerate(doc.action_items, 1):
        for key in ("action", "type", "owner", "due"):
            if blank(getattr(item, key)):
                problems.append(f"action_items[{index}].{key} is required")
    if problems:
        for problem in problems:
            print(f"rca.py: {problem}", file=sys.stderr)
        sys.exit(2)


# ---------- rendering ----------

def as_lines(value):
    """Flatten a string or list of strings into a list of strings."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def mermaid_label(value):
    """Strip characters that break a Mermaid node label."""
    cleaned = re.sub(r'["\[\](){}]', "", str(value))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "step"


def mermaid_from_chain(chain):
    """Render a causal chain as a left-to-right flowchart, cause to effect.

    The chain is authored in 5-whys order: the symptom first, then each link
    explaining the one before it, ending at the root cause. That order is
    what makes the numbered list a readable why-chain.

    A flowchart reads the other way, from cause to effect, so the chain is
    reversed here. Without this the diagram starts at the symptom and
    points backwards at the root cause.
    """
    steps = [str(step).strip() for step in chain if str(step).strip()]
    if len(steps) < 2:
        return ""
    steps.reverse()
    lines_out = ["flowchart LR"]
    ids = []
    for index, step in enumerate(steps):
        node = chr(ord("A") + index) if index < 26 else f"N{index}"
        ids.append(node)
        lines_out.append(f'    {node}["{mermaid_label(step)}"]')
    for index in range(len(ids) - 1):
        lines_out.append(f"    {ids[index]} --> {ids[index + 1]}")
    return "\n".join(lines_out)


def render_metadata(metadata):
    rows = []
    for spec in dataclasses.fields(metadata):
        value = getattr(metadata, spec.name)
        if spec.name == "authors":
            value = ", ".join(str(author).strip() for author in value if str(author).strip())
        else:
            value = str(value).strip()
        if value:
            rows.append(f"| {spec.name.capitalize()} | {value} |")
    if not rows:
        return ""
    body = "\n".join(rows)
    return f"| Field | Value |\n|-------|-------|\n{body}"


def render_notice(notice):
    lines_out = ["Attention Conservation Notice"]
    for attribute, label in (
        ("audience", "For"),
        ("what", "What"),
        ("action", "Action"),
        ("skip_if", "Skip if"),
    ):
        lines_out.append(f"{label}: {getattr(notice, attribute).strip()}")
    return "\n".join(lines_out)


def render_root_cause(root_cause):
    out = []
    if root_cause.statement.strip():
        out.append(root_cause.statement.strip())
    chain = [str(step).strip() for step in root_cause.chain if str(step).strip()]

    if root_cause.method == "five-whys" and chain:
        out.append("")
        out.append("Why chain:")
        out.append("")
        for index, step in enumerate(chain, 1):
            out.append(f"{index}. {step}")
    elif root_cause.method == "fault-tree" and root_cause.factors:
        out.append("")
        out.append("Contributions:")
        out.append("")
        out.append("| Factor | Contribution |")
        out.append("|--------|--------------|")
        for factor in root_cause.factors:
            out.append(f"| {factor.name} | {factor.contribution} |")

    diagram = mermaid_from_chain(chain)
    if diagram:
        out.append("")
        out.append("```mermaid")
        out.append(diagram)
        out.append("```")
    return "\n".join(out)


def render_resolution(resolution):
    parts = [resolution.mitigation.strip(), resolution.fix.strip()]
    return "\n\n".join(part for part in parts if part)


def render_timeline(timeline):
    if not timeline:
        return ""
    rows = ["| Time | Event |", "|------|-------|"]
    for entry in timeline:
        rows.append(f"| {entry.time.strip()} | {entry.event.strip()} |")
    return "\n".join(rows)


def render_actions(actions):
    if not actions:
        return "No action items."
    rows = ["| # | Action | Type | Owner | Due |", "|---|--------|------|-------|-----"]
    for index, item in enumerate(actions, 1):
        rows.append(
            f"| {index} | {item.action.strip()} | {item.type.strip()} "
            f"| {item.owner.strip()} | {item.due.strip()} |"
        )
    return "\n".join(rows)


def render(doc):
    """Render an RCA dataclass into a markdown document."""
    out = [f"# RCA: {doc.title.strip()}", ""]

    metadata_block = render_metadata(doc.metadata)
    if metadata_block:
        out.append(metadata_block)
        out.append("")

    if doc.intro.strip():
        out.append(doc.intro.strip())
        out.append("")

    out.append(render_notice(doc.notice))
    out.append("")

    blocks = [
        ("Summary", doc.summary),
        ("Impact", "\n".join(f"- {line}" for line in as_lines(doc.impact))),
        ("Timeline", render_timeline(doc.timeline)),
        ("Root cause", render_root_cause(doc.root_cause)),
        (
            "Contributing factors",
            "\n".join(f"- {line}" for line in as_lines(doc.contributing_factors)),
        ),
        ("Detection", doc.detection),
        ("Resolution", render_resolution(doc.resolution)),
        ("Action items", render_actions(doc.action_items)),
        ("Lessons learned", "\n".join(f"- {line}" for line in as_lines(doc.lessons_learned))),
    ]

    for heading, body in blocks:
        if not body.strip():
            continue
        out.append(f"## {heading}")
        out.append("")
        out.append(body)
        out.append("")

    return "\n".join(out).rstrip() + "\n"


# ---------- checking ----------

def parse_sections(markdown):
    """Split markdown into the preamble and (heading, body) pairs.

    The top-level title is its own heading and never a section, so the
    preamble keeps the intro and the notice.
    """
    preamble = []
    sections = []
    current_heading = None
    current_body = []
    seen_title = False
    for line in markdown.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            level = len(match.group(1))
            heading = match.group(2).strip()
            if level == 1 and not seen_title:
                seen_title = True
                continue
            if current_heading is None:
                preamble.extend(current_body)
            else:
                sections.append((current_heading, "\n".join(current_body)))
            current_heading = heading
            current_body = []
        else:
            current_body.append(line)
    if current_heading is None:
        preamble.extend(current_body)
    else:
        sections.append((current_heading, "\n".join(current_body)))
    return "\n".join(preamble), sections


def extract_notice(preamble):
    match = re.search(
        r"Attention Conservation Notice\s*\n(.*?)(?:\n\s*\n|\Z)",
        preamble,
        re.S,
    )
    if not match:
        return None
    found = {}
    for line in match.group(1).splitlines():
        for key in ("For", "What", "Action", "Skip if"):
            if line.strip().startswith(f"{key}:"):
                found[key] = line.strip()[len(key) + 1:].strip()
    return found


def table_rows(body, min_cells):
    """Yield table data rows, skipping the header and separator rows."""
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < min_cells:
            continue
        if all(set(cell) <= set("-: ") for cell in cells if cell):
            continue
        if cells[0].lower() in ("time", "#", "field", "factor", "contributions", "step"):
            continue
        yield cells


def check_mermaid(markdown):
    """Validate Mermaid blocks: declaration, balanced labels, known nodes."""
    findings = []
    for block in re.findall(r"```mermaid\n(.*?)```", markdown, re.S):
        lines_out = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines_out:
            findings.append("Mermaid block is empty")
            continue
        if not re.match(r"^(flowchart|graph)\s", lines_out[0]):
            findings.append(f"Mermaid block does not start with a flowchart declaration: {lines_out[0]!r}")
        defined = set()
        for line in lines_out:
            # A node can be declared on its own line or inline on an edge,
            # as in `A[label] --> B[label]`.
            for node in re.findall(r"([A-Za-z0-9_]+)\s*\[", line):
                defined.add(node)
            if line.count('"') % 2:
                findings.append(f"Mermaid node has an unbalanced quote: {line!r}")
        for line in lines_out:
            for edge in re.findall(r"([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)", line):
                for node in edge:
                    if node not in defined:
                        findings.append(f"Mermaid edge references undefined node {node!r}")
        if len(defined) < 2:
            findings.append("Mermaid chain has fewer than two nodes")
    return findings


def parse_times(timeline_body):
    """Return (kind, value) pairs for timeline rows, or None if unparsable."""
    rows = []
    for cells in table_rows(timeline_body, 2):
        stamp = cells[0]
        date_match = re.match(r"^(\d{4}-\d{2}-\d{2})[ T](\d{1,2}:\d{2})$", stamp)
        clock_match = re.match(r"^(\d{1,2}):(\d{2})$", stamp)
        if date_match:
            rows.append(("date", f"{date_match.group(1)}T{date_match.group(2)}"))
        elif clock_match:
            rows.append(("clock", f"{int(clock_match.group(1)):02d}:{clock_match.group(2)}"))
        else:
            rows.append(("other", stamp))
    return rows


def check_timeline(body):
    findings = []
    rows = parse_times(body)
    if not rows:
        findings.append("Timeline section has no rows")
        return findings
    kinds = {kind for kind, _ in rows}
    if kinds == {"clock"}:
        for index in range(len(rows) - 1):
            if rows[index + 1][1] < rows[index][1]:
                findings.append(
                    "Timeline goes backwards at "
                    f"{rows[index][1]} -> {rows[index + 1][1]}; add dates for an overnight incident"
                )
    elif "date" in kinds:
        dated = [(kind, value) for kind, value in rows if kind == "date"]
        for index in range(len(dated) - 1):
            if dated[index + 1][1] < dated[index][1]:
                findings.append(
                    "Timeline goes backwards at "
                    f"{dated[index][1]} -> {dated[index + 1][1]}"
                )
    if "other" in kinds:
        stamps = [value for kind, value in rows if kind == "other"]
        findings.append(f"Timeline has unreadable timestamps: {', '.join(stamps)}")
    return findings


def check_action_items(body):
    findings = []
    rows = list(table_rows(body, 5))
    if not rows:
        stripped = body.strip().lower()
        if stripped.startswith("no action item") or stripped in ("none", "none."):
            return findings
        findings.append("Action items section has no table rows")
        return findings
    for number, cells in enumerate(rows, 1):
        label, kind, owner, due = cells[1], cells[2], cells[3], cells[4]
        if not label:
            findings.append(f"Action item {number} has no action text")
        if kind.lower() not in VALID_ACTION_TYPES:
            findings.append(
                f"Action item {number} has type {kind!r}; use Prevent, Detect, or Mitigate"
            )
        if not owner:
            findings.append(f"Action item {number} has no owner")
        if not due:
            findings.append(f"Action item {number} has no due date")
    return findings


def check_root_cause(body):
    findings = []
    statement = ""
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("```", "|", "#")):
            continue
        if stripped[0].isdigit() and ". " in stripped[:4]:
            continue
        statement = stripped
        break
    if not statement:
        findings.append("Root cause section has no statement")
        return findings
    if len(statement) < 25:
        findings.append("Root cause statement is too short to state a mechanism")
    for pattern, reason in WEAK_CAUSE_PATTERNS:
        if re.search(pattern, statement, re.I):
            findings.append(f"Root cause statement {reason}")
    has_chain = "```mermaid" in body
    if not has_chain:
        for pattern in TRIGGER_AS_CAUSE_PATTERNS:
            if re.search(pattern, statement, re.I):
                findings.append(
                    "Root cause names a trigger, not a mechanism; trace the chain to the "
                    "deepest actionable level"
                )
    findings.extend(check_chain_direction(body))
    return findings


def mermaid_labels(body):
    """Extract node labels from a Mermaid flowchart in order."""
    labels = []
    for block in re.findall(r"```mermaid\n(.*?)```", body, re.S):
        for line in block.splitlines():
            quoted = re.match(r'^\s*([A-Za-z0-9_]+)\s*\["(.*)"\]\s*$', line)
            if quoted:
                labels.append(quoted.group(2))
                continue
            bare = re.match(r"^\s*([A-Za-z0-9_]+)\s*\[(.*)\]\s*$", line)
            if bare:
                labels.append(bare.group(2))
    return labels


def numbered_chain(body):
    """Extract the entries of a numbered why-chain list, in order."""
    entries = []
    for line in body.splitlines():
        match = re.match(r"^\s*\d+\.\s+(.*\S)\s*$", line)
        if match:
            entries.append(match.group(1))
    return entries


def normalize_label(text):
    """Reduce a label to comparable words for direction checking."""
    return re.sub(r"[^a-z0-9 ]+", "", str(text).lower()).split()


def check_chain_direction(body):
    """The diagram must run the opposite way to the numbered why-chain.

    The why-chain reads symptom to root cause; the flowchart reads cause to
    effect. So the diagram's first node is the chain's last entry, and its
    last node is the chain's first entry. A diagram that starts at the
    symptom points backwards.
    """
    findings = []
    diagram = mermaid_labels(body)
    chain = numbered_chain(body)
    if len(diagram) < 2 or len(chain) != len(diagram):
        return findings
    starts_at_root = normalize_label(diagram[0]) == normalize_label(chain[-1])
    ends_at_symptom = normalize_label(diagram[-1]) == normalize_label(chain[0])
    if starts_at_root and ends_at_symptom:
        return findings
    if normalize_label(diagram[0]) == normalize_label(chain[0]):
        findings.append(
            "Mermaid diagram starts at the symptom and points backwards; the "
            "flowchart must run from cause to effect"
        )
    return findings


def declared_status(preamble):
    """Read the Status value from the metadata table, if the document has one."""
    for cells in table_rows(preamble, 2):
        if cells[0].lower() == "status":
            return cells[1].strip().lower()
    return ""


def check_markdown(markdown, draft=False):
    """Run every structural and judgment check. Returns a list of findings."""
    findings = []
    preamble, sections = parse_sections(markdown)

    # A document that declares itself a draft may carry TODO markers. The
    # explicit --draft flag forces this regardless of the declared status.
    if declared_status(preamble).startswith("draft"):
        draft = True

    if not re.search(r"^#\s+\S", markdown, re.M):
        findings.append("Document has no top-level title")

    notice_match = re.search(r"Attention Conservation Notice", preamble)
    if not notice_match:
        findings.append("Missing Attention Conservation Notice")
    else:
        before = preamble[: notice_match.start()].strip()
        notice = extract_notice(preamble[notice_match.start():])
        if notice is None:
            findings.append("Attention Conservation Notice is malformed")
        else:
            for key in ("For", "What", "Action", "Skip if"):
                if key not in notice:
                    findings.append(f"Attention Conservation Notice is missing the {key} line")
                elif not notice[key]:
                    findings.append(f"Attention Conservation Notice has an empty {key} line")
        # The intro is prose. A metadata table above the notice does not
        # count as an intro, so strip table rows before testing.
        before = preamble[: notice_match.start()].strip()
        prose_before = "\n".join(
            line for line in before.splitlines() if not line.strip().startswith("|")
        ).strip()
        if not prose_before:
            findings.append("Document has no plain intro before the Attention Conservation Notice")
    if not preamble.strip():
        findings.append("Document has no preamble")

    present = {heading for heading, _ in sections}
    for heading in REQUIRED_SECTIONS:
        if heading not in present:
            findings.append(f"Missing required section: {heading}")

    bodies = {heading: body for heading, body in sections}
    for heading, body in bodies.items():
        content = body.strip()
        if not content:
            findings.append(f"Section '{heading}' is empty; remove it or fill it")
            continue
        if content.lower() in EMPTY_STUBS:
            findings.append(f"Section '{heading}' contains only a stub ({content!r})")
            continue
        if not draft and re.search(r"TODO:", content):
            findings.append(f"Section '{heading}' still contains a TODO marker")

    if "Timeline" in bodies:
        findings.extend(check_timeline(bodies["Timeline"]))
    if "Action items" in bodies:
        findings.extend(check_action_items(bodies["Action items"]))
    if "Root cause" in bodies:
        findings.extend(check_root_cause(bodies["Root cause"]))
    findings.extend(check_mermaid(markdown))
    return findings


# ---------- drafts ----------

SCAFFOLD = '''"""RCA draft.

Fill in every REQUIRED field, then run:
    python3 scripts/rca.py render {name} -o rca-<slug>.md
    python3 scripts/rca.py check rca-<slug>.md

REQUIRED fields have no default and must carry content. OPTIONAL fields may
be left empty; an empty one drops its section from the document.
"""

from rca import ActionItem, Metadata, Notice, RCA, Resolution, RootCause, TimelineEntry

doc = RCA(
    # --- required ---
    title="",
    intro="",
    notice=Notice(
        audience="",
        what="",
        action="",
        skip_if="",
    ),
    summary="",
    impact="",
    root_cause=RootCause(
        statement="",
        method="five-whys",
        chain=[],
        factors=[],
    ),
    resolution=Resolution(
        mitigation="",
        fix="",
    ),
    action_items=[],
    # --- optional ---
    metadata=Metadata(
        date="",
        severity="",
        duration="",
        status="Draft",
        authors=[],
    ),
    timeline=[],
    contributing_factors=[],
    detection="",
    lessons_learned="",
)
'''

EXAMPLE_DRAFT = '''"""Filled example RCA draft. Copy it and replace the values."""

from rca import ActionItem, Metadata, Notice, RCA, Resolution, RootCause, TimelineEntry

doc = RCA(
    # --- required ---
    title="Checkout returns 503 for card payments",
    intro=(
        "Card payment requests failed with 503 for 45 minutes on 2026-09-14. "
        "This RCA covers the failure and the changes that prevent it from recurring."
    ),
    notice=Notice(
        audience="Payments and checkout engineers",
        what="The 503 outage on the card payment path and its causes",
        action="Review the action items and confirm owners by 2026-09-18",
        skip_if="None",
    ),
    summary=(
        "I released a schema migration that added an unindexed column to the payments "
        "table. Queries on the payment lookup path fell back to full table scans, the "
        "connection pool saturated, and card payment requests timed out. I rolled the "
        "migration back at 14:47 UTC and the error rate returned to baseline."
    ),
    impact=(
        "312 card payment requests failed between 14:02 and 14:47 UTC, about 4% of "
        "checkout attempts in that window. No payment was double charged and no card "
        "data was lost. No revenue figure is confirmed yet."
    ),
    root_cause=RootCause(
        statement=(
            "The payments lookup query gained a full table scan because the migration "
            "added a filter column with no index, and the resulting query latency "
            "exhausted the connection pool, so requests timed out instead of returning "
            "a response."
        ),
        method="five-whys",
        chain=[
            "Card payment requests returned 503",
            "Requests timed out after 3 s waiting for a free connection",
            "The connection pool saturated under retry load",
            "Query latency rose from 12 ms to 4 s",
            "Lookup queries fell back to full table scans",
            "The migration added an unindexed filter column to the payments table",
        ],
    ),
    resolution=Resolution(
        mitigation="I rolled back the migration at 14:44 UTC and confirmed recovery at 14:47 UTC.",
        fix=(
            "I re-applied the migration with a concurrent index build and a backfill, so "
            "the lookup path kept its index."
        ),
    ),
    action_items=[
        ActionItem(
            action="Run EXPLAIN against production-shaped data in the migration pipeline",
            type="Prevent",
            owner="Payments platform team",
            due="2026-10-02",
        ),
        ActionItem(
            action="Alert when p99 query latency on the payments path exceeds 500 ms",
            type="Detect",
            owner="Observability team",
            due="2026-10-10",
        ),
        ActionItem(
            action="Add an index coverage check to the migration review checklist",
            type="Prevent",
            owner="Payments platform team",
            due="2026-09-28",
        ),
        ActionItem(
            action="Document a rollback procedure for payments schema migrations",
            type="Mitigate",
            owner="Payments on-call",
            due="2026-09-25",
        ),
    ],
    # --- optional ---
    metadata=Metadata(
        date="2026-09-14",
        severity="SEV-2",
        duration="45 minutes (14:02 to 14:47 UTC)",
        status="Draft",
        authors=["I. Okafor"],
    ),
    timeline=[
        TimelineEntry(time="14:02", event="Migration 2026-09-14-a applied to the payments table"),
        TimelineEntry(time="14:09", event="Alert fired on payment path 5xx rate above 2%"),
        TimelineEntry(time="14:14", event="I paged the payments on-call and started reading the migration diff"),
        TimelineEntry(time="14:31", event="I confirmed the missing index and the full table scans in query logs"),
        TimelineEntry(time="14:44", event="I rolled back migration 2026-09-14-a"),
        TimelineEntry(time="14:47", event="Error rate returned to 0.1%, recovery verified"),
    ],
    contributing_factors=[
        "The migration pipeline does not run EXPLAIN against production-shaped data",
        "No alert fires on query latency, only on 5xx rate",
        "The payments table had no index coverage check in the migration review checklist",
    ],
    detection=(
        "The alerting stack caught it 7 minutes after the migration, on the 5xx rate. "
        "Nothing alerted on query latency, so the first signal described the symptom "
        "rather than the cause."
    ),
    lessons_learned=(
        "The migration pipeline gave false confidence: it passed because it checked that "
        "the new column existed, not that queries still used indexes. The 5xx alert also "
        "described the symptom, which cost about 22 minutes of diagnosis."
    ),
)
'''


# ---------- cli ----------

def main():
    parser = argparse.ArgumentParser(prog="rca.py", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    scaffold_parser = sub.add_parser("scaffold", help="write a blank draft to fill in")
    scaffold_parser.add_argument("-o", "--output", help="output file (default: stdout)")

    example_parser = sub.add_parser("example", help="write a filled example draft")
    example_parser.add_argument("-o", "--output", help="output file (default: stdout)")

    render_parser = sub.add_parser("render", help="render a draft into markdown")
    render_parser.add_argument("draft", help="draft Python file to render")
    render_parser.add_argument("-o", "--output", help="output file (default: stdout)")

    check_parser = sub.add_parser("check", help="validate a rendered RCA")
    check_parser.add_argument("doc", help="markdown file to check")
    check_parser.add_argument(
        "--draft",
        action="store_true",
        help="allow TODO markers for a work in progress",
    )
    check_parser.add_argument(
        "--json",
        action="store_true",
        help="emit findings as JSON",
    )

    args = parser.parse_args()

    if args.command == "scaffold":
        text = SCAFFOLD.format(name=os.path.basename(args.output or "draft.py"))
        return write_out(text, args.output)

    if args.command == "example":
        return write_out(EXAMPLE_DRAFT, args.output)

    if args.command == "render":
        doc = load_draft(args.draft)
        check_types(doc)
        validate_required(doc)
        markdown = render(doc)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(markdown)
            print(f"rca.py: wrote {args.output}", file=sys.stderr)
        else:
            sys.stdout.write(markdown)
        return 0

    if not os.path.isfile(args.doc):
        die(f"document not found: {args.doc}")
    with open(args.doc, "r", encoding="utf-8") as fh:
        markdown = fh.read()

    findings = check_markdown(markdown, draft=args.draft)
    if args.json:
        import json

        json.dump({"findings": findings, "clean": not findings}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0 if not findings else 2
    if not findings:
        print("rca.py: clean")
        return 0
    for finding in findings:
        print(finding, file=sys.stderr)
    print(f"rca.py: {len(findings)} finding(s)", file=sys.stderr)
    return 2


def write_out(text, output):
    if output:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"rca.py: wrote {output}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
