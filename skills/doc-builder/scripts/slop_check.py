#!/usr/bin/env python3
"""doc-builder pre-delivery checker: scan a generated doc for AI writing tells.

Usage:
    slop_check.py FILE [FILE ...]     scan files
    slop_check.py < draft.md          scan raw text on stdin
    echo '{"tool_input":{"file_path":"f.md"}}' | slop_check.py   hook-style JSON

Prints findings with line numbers; exits 2 if any, 0 when clean.

Three detection layers, merged and deduped:
  1. doc-builder house rules (typography, headings, template-aware formatting)
  2. unslop banned_phrase_scan: collocation-gated phrase and jargon patterns
     with domain false-positive protections, hard/soft severities
  3. unslop structure_scan: document-level rhythm tells (burstiness, coda,
     connector stacking, opener repetition, signposts, staccato)

Adapted from Abdulkader-Safi/AI-Writing-Rules scripts/slop-check.py
(Copyright (c) 2026 Abdulkader Safi, MIT License) and theclaymethod/unslop
(Copyright (c) 2025-2026 Clayton Kim, MIT License).

Doc-builder deltas vs AI-Writing-Rules upstream: file-arg/stdin interface,
allowlist for template-mandated Title-Case headings and the ticket
**Summary:** field, bold-label rule fires on paragraph use or 4+ stacked
label bullets (true definition lists stay legal, both `**X:**` and `**X**:`
forms caught), subjectless "not just X, it's Y" branch.
"""

import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

try:
    from banned_phrase_scan import scan_for_violations as _unslop_phrases
    from structure_scan import scan as _unslop_structure
    from _lang import is_probably_english as _is_english
    _UNSLOP = True
except Exception:
    _UNSLOP = False

OPT_OUT = "slop-check: off"
MAX_PER_RULE = 4
STACKED_LABEL_BULLETS = 4

# Template-mandated headings and field labels that stay verbatim even though
# they trip generic patterns. Compare label text case-insensitively.
ALLOWED_HEADINGS = {
    "acceptance criteria",
    "options considered",
    "technical details",
    "pr description",
    "user story",
    "attention conservation notice",
}
ALLOWED_LABELS = {"summary", "for", "what", "action", "skip if"}

# (label, compiled regex, hint)
RULES = [
    ("em dash", re.compile(r"[—―‒]"), "use a full stop, comma, colon, or brackets"),
    (
        "curly quote or ellipsis",
        re.compile(r"[‘’“”…]"),
        "use straight quotes and three dots",
    ),
    (
        "negative parallelism",
        re.compile(
            r"\b(?:it|this|that|we|they|you)\s*(?:'s|’s| is| are|n't| isn't|n’t)?\s*(?:is|are|was|were)?n?'?t?\s+not\s+(?:just\s+)?[^.!?\n]{1,60}?[,;]\s*(?:it|this|that|we|they|you)\s*(?:'s|’s| is| are)\b"
        r"|\b(?:isn'?t|aren'?t|wasn'?t|weren'?t|don'?t|doesn'?t)\s+(?:just\s+)?[^.!?\n]{1,50}?[,;]\s*(?:it|this|that)\s*(?:'s|’s| is)\b"
            r"|\bnot\s+just\s+[^.!?\n]{1,50}?,\s*but\b"
            r"|\bnot\s+just\s+[^.!?\n]{1,50}?,\s*(?:it|this|that|the)\s*(?:'s|’s|is|are)\b"
            r"|\bnot\s+only\s+[^.!?\n]{1,60}?\s+but\s+also\b",
            re.I,
        ),
        "delete the negation, keep the positive half",
    ),
    (
        "AI vocabulary",
        re.compile(
            r"\b(?:delve[sd]?|delving|tapestry|vibrant|multifaceted|nuanced|intricate|intricacies"
            r"|realm|testament|foster(?:s|ed|ing)?|leverag(?:e|es|ed|ing)|robust|seamless(?:ly)?"
            r"|underscor(?:e|es|ed|ing)|pivotal|crucial|holistic|transformative|elevat(?:e|es|ed|ing)"
            r"|embark(?:s|ed|ing)?|unlock(?:s|ed|ing)?|harness(?:es|ed|ing)?|showcas(?:e|es|ed|ing)"
            r"|resonat(?:e|es|ed|ing)|garner(?:s|ed|ing)?|boasts?|meticulous(?:ly)?|bolster(?:s|ed|ing)?"
            r"|streamlin(?:e|es|ed|ing)|empower(?:s|ed|ing)?|myriad|plethora|paradigm|quintessential"
            r"|interplay|indelible|groundbreaking|cutting-edge|state-of-the-art|world-class"
            r"|best-in-class|enterprise-grade|game-chang(?:er|ing)|revolutioniz(?:e|es|ed|ing))\b",
            re.I,
        ),
        "replace with the plainest word that carries the meaning",
    ),
    (
        "inflated verb",
        re.compile(
            r"\b(?:utiliz(?:e|es|ed|ing)|facilitat(?:e|es|ed|ing)|ascertain(?:s|ed)?"
            r"|endeavou?r(?:s|ed|ing)?|commenc(?:e|es|ed|ing)|terminat(?:e|es|ed|ing)"
            r"|in order to|prior to|subsequent to|with regard(?:s)? to|regarding"
            r"|a number of|the vast majority of|in the event that)\b",
            re.I,
        ),
        "use / help / find out / try / start / end / to / before / about / some",
    ),
    (
        "dodged copula",
        re.compile(
            r"\b(?:serves?|serving|stands?|standing|functions?|operates?)\s+as\b"
            r"|\brepresents\s+a\b|\bmarks\s+(?:a|the)\s+(?:significant|key|important|pivotal)\b",
            re.I,
        ),
        "say is",
    ),
    (
        "puffed significance",
        re.compile(
            r"\b(?:is\s+a\s+testament|plays?\s+a\s+(?:crucial|pivotal|vital|key|central)\s+role"
            r"|underscor\w+\s+the\s+importance|reflect\w*\s+a\s+broader"
            r"|(?:evolving|broader|changing)\s+landscape|setting\s+the\s+stage"
            r"|significant\s+milestone|key\s+turning\s+point|left\s+an\s+indelible)\b",
            re.I,
        ),
        "state what happened, drop why it matters to the universe",
    ),
    (
        "vague attribution",
        re.compile(
            r"\b(?:experts?\s+(?:say|agree|argue|believe|note)|studies\s+have\s+shown"
            r"|research\s+(?:suggests|shows|indicates)|industry\s+reports?"
            r"|(?:many|some)\s+(?:believe|argue|say)|it\s+is\s+widely\s+(?:regarded|known|believed)"
            r"|observers\s+have|several\s+sources)\b",
            re.I,
        ),
        "name the source or drop the claim",
    ),
    (
        "empty opener",
        re.compile(
            r"(?:^|\n)\s*(?:in\s+today'?s?\s+(?:fast-paced|digital|modern)|in\s+the\s+digital\s+age"
            r"|in\s+an?\s+era\s+of|picture\s+this|imagine\s+a\s+world|we\s+live\s+in\s+a\s+time"
            r"|now\s+more\s+than\s+ever|it'?s\s+no\s+secret|let'?s\s+face\s+it"
            r"|as\s+technology\s+continues)",
            re.I,
        ),
        "delete the sentence, start with the fact",
    ),
    (
        "outline ending",
        re.compile(
            r"\b(?:in\s+conclusion|to\s+conclude|as\s+we\s+look\s+ahead|moving\s+forward"
            r"|only\s+time\s+will\s+tell|challenges\s+and\s+(?:future|opportunities)"
            r"|future\s+(?:outlook|prospects)|it'?s\s+important\s+to\s+note)\b",
            re.I,
        ),
        "end at the last real sentence",
    ),
    (
        "hedge stack",
        re.compile(
            r"\b(?:it\s+could\s+be\s+argued|one\s+could\s+argue|may\s+potentially"
            r"|can\s+sometimes\s+be|to\s+some\s+extent|generally\s+speaking"
            r"|in\s+certain\s+contexts|there\s+is\s+no\s+one-size-fits-all)\b",
            re.I,
        ),
        "make the claim or write TODO:",
    ),
    (
        "pseudo-wisdom",
        re.compile(
            r"\b(?:the\s+key\s+is\s+to\s+find|at\s+the\s+end\s+of\s+the\s+day"
            r"|it\s+(?:all\s+)?(?:depends|comes\s+down\s+to)\s+(?:on\s+)?your\s+(?:specific\s+)?needs"
            r"|true\s+\w+\s+comes\s+from\s+within|the\s+right\s+balance)\b",
            re.I,
        ),
        "delete it or make it specific",
    ),
    (
        "assistant scaffolding",
        re.compile(
            r"(?:certainly!|i\s+hope\s+this\s+helps|as\s+an\s+ai(?:\s+language\s+model)?"
            r"|let\s+me\s+know\s+if\s+you'?d\s+like|feel\s+free\s+to\s+(?:ask|reach)"
            r"|great\s+question|as\s+of\s+my\s+knowledge\s+cutoff"
            r"|in\s+this\s+(?:article|guide|post|document|report),?\s+we(?:'ll|\s+will)\s+explore"
            r"|\[(?:insert|your|company\s+name|placeholder|citation\s+needed)\b)",
            re.I,
        ),
        "strip it",
    ),
    (
        "model artifact",
        re.compile(
            r"(?:oaicite|contentReference|turn\d+search\d+|attributableIndex|\[cite:\s*\d"
            r"|grok_card|grok_render_citation|ppl-ai-file-upload|:::writing|utm_source=)"
        ),
        "leaked markup, delete it",
    ),
    (
        "emphasis crutch",
        re.compile(
            r"\b(?:let that sink in|read that again|make no mistake"
            r"|this cannot be overstated|the uncomfortable truth is)\b",
            re.I,
        ),
        "the content carries the emphasis; delete the stage direction",
    ),
    (
        "false agency",
        re.compile(r"\bspeaks?\s+for\s+(?:itself|themselves)\b", re.I),
        "state the numbers and what they show",
    ),
    (
        "trailing -ing commentary",
        re.compile(
            r",\s+(?:highlighting|underscoring|emphasizing|emphasising|ensuring|reflecting"
            r"|symbolizing|symbolising|showcasing|fostering|cultivating|paving\s+the\s+way"
            r"|allowing\s+for|contributing\s+to)\b",
            re.I,
        ),
        "cut everything after the comma",
    ),
]

TITLE_CASE_HEADING = re.compile(r"^#{1,6}\s+(?:[A-Z][a-z]+\s+){1,}(?:[A-Z][a-z]+)\s*$")
HEADING_TEXT = re.compile(r"^#{1,6}\s+(.*?)\s*$")
# Matches both `**Term**: x` and `**Term:** x`; a colon must be present so a
# bold-led bullet without one (`- **2026-09** rollout`) does not flag.
PARA_LABEL = re.compile(r"^\s*\*\*([^*\n:]{2,40}?)(?::\*\*\s+|\*\*\s*:)\s*\S")
BULLET_LABEL = re.compile(r"^\s*[-*+]\s+\*\*([^*\n:]{2,40}?)(?::\*\*\s+|\*\*\s*:)\s*\S")

TRICOLON = re.compile(
    r"\b([a-z]{3,14}), ([a-z]{3,14}),? and ([a-z]{3,14})\b(?!\s*[,:])", re.I
)
TRANSITIONS = re.compile(
    r"(?:^|(?<=[.!?])\s)\s*(?:Furthermore|Moreover|Additionally|In addition|Consequently|Nevertheless"
    r"|Nonetheless|Ultimately|Notably|Importantly|That said|Indeed|Thus|Hence)\b",
    re.I,
)

# Friendlier labels for unslop structure_scan metric names.
STRUCT_LABELS = {
    "sentence_burstiness": "uniform sentence length",
    "conclusion_coda": "wrap-up coda",
    "bold_colon_listicle": "bold-label listicle",
    "one_line_staccato": "staccato fragments",
    "connective_paragraph_openers": "connector-stacked paragraphs",
    "every_template_openers": "Every-template paragraph openers",
    "signpost_density": "structural signposting",
    "opener_repetition": "repeated sentence openers",
    "participial_closer_share": "-ing closer density",
}


def strip_noise(text):
    """Blank out fenced code and inline code so we only lint prose."""
    text = re.sub(r"(?ms)^```.*?^```", lambda m: "\n" * m.group(0).count("\n"), text)
    return re.sub(r"`[^`\n]+`", " ", text)


def _words_of(text):
    return set(re.findall(r"[a-z0-9']+", text.lower()))


def _dedupe_house_hits(house_hits, unslop_violations):
    """Drop a house-rule hit when an unslop violation covers the same span on
    the same line. unslop findings carry severity and a tighter span (their
    collocation gating protects literal uses), so theirs wins on overlap."""
    by_line = {}
    for v in unslop_violations:
        by_line.setdefault(v["line_number"], []).append(v["phrase"].lower())
    kept = []
    for label, hint, hits in house_hits:
        kept_hits = []
        for n, excerpt in hits:
            ex = excerpt.lower()
            ex_words = _words_of(excerpt)
            covered = False
            for phrase in by_line.get(n, []):
                ph_words = _words_of(phrase)
                if ex in phrase or phrase in ex or len(ex_words & ph_words) >= 2:
                    covered = True
                    break
            if not covered:
                kept_hits.append((n, excerpt))
        if kept_hits:
            kept.append((label, hint, kept_hits))
    return kept


def _house_scan(raw):
    prose = strip_noise(raw)
    lines = prose.split("\n")
    findings = []

    for label, rx, hint in RULES:
        hits = []
        for n, line in enumerate(lines, 1):
            for m in rx.finditer(line):
                hits.append((n, m.group(0).strip()[:60]))
                break
        if hits:
            findings.append((label, hint, hits))

    hits = []
    for n, line in enumerate(lines, 1):
        if TITLE_CASE_HEADING.match(line):
            text = HEADING_TEXT.match(line).group(1)
            if text.lower() not in ALLOWED_HEADINGS:
                hits.append((n, line.strip()[:60]))
    if hits:
        findings.append(
            ("Title Case heading", "sentence case: capital on the first word only", hits)
        )

    hits = []
    stack = []
    for n, line in enumerate(lines, 1):
        m = BULLET_LABEL.match(line)
        if m and m.group(1).strip().lower() not in ALLOWED_LABELS:
            stack.append((n, line.strip()[:60]))
            continue
        if len(stack) >= STACKED_LABEL_BULLETS:
            hits.extend(stack)
        stack = []
        m = PARA_LABEL.match(line)
        if m and m.group(1).strip().lower() not in ALLOWED_LABELS:
            hits.append((n, line.strip()[:60]))
    if len(stack) >= STACKED_LABEL_BULLETS:
        hits.extend(stack)
    if hits:
        findings.append(
            (
                "bold-label formatting",
                "write it as prose or plain bullets; **Term**: lists are for true definitions",
                hits,
            )
        )

    tri = [
        (n, m.group(0))
        for n, line in enumerate(lines, 1)
        for m in [TRICOLON.search(line)]
        if m
    ]
    words = len(prose.split())
    if len(tri) >= 2 or (tri and words < 250):
        findings.append(
            ("rule of three", "break the triplet: use one, two, or four", tri)
        )

    conn = TRANSITIONS.findall(prose)
    if len(conn) >= 3:
        findings.append(
            (
                "transition stacking",
                f"{len(conn)} sentences open with a formal connector, delete them",
                [],
            )
        )

    return findings


def scan(raw):
    """Return (findings, unslop_violations, structure_flags).

    findings: house rules as (label, hint, [(line, excerpt)])
    unslop_violations: phrase-level hits (already deduped against findings)
    structure_flags: document-level metric flags
    """
    if OPT_OUT in raw:
        return [], [], []

    house = _house_scan(raw)

    violations = []
    struct_flags = []
    if _UNSLOP and _is_english(raw):
        violations = _unslop_phrases(raw)
        struct = _unslop_structure(raw, genre="docs")
        # one_line_staccato hunts de-slopped choppy prose; doc-builder output is
        # deliberately short-paragraphed (3-sentence cap, ACN block, bullet
        # fields), so the metric false-positives on tickets and specs. Drop it.
        struct_flags = [
            (STRUCT_LABELS.get(f["metric"], f["metric"]), f["suggestion"], f["detail"])
            for f in struct.get("flags", [])
            if f["metric"] != "one_line_staccato"
        ]

    house = _dedupe_house_hits(house, violations)
    return house, violations, struct_flags


def report(name, house, violations, struct_flags):
    total = len(house) + len(violations) + len(struct_flags)
    out = [
        f"Writing rules: {total} issue(s) in {name}. Fix before moving on.\n"
    ]
    for label, hint, hits in house:
        shown = hits[:MAX_PER_RULE]
        more = f" (+{len(hits) - len(shown)} more)" if len(hits) > len(shown) else ""
        locs = "; ".join(f"L{n}: {t}" for n, t in shown) if shown else ""
        out.append(f"  {label}{more}: {hint}")
        if locs:
            out.append(f"    {locs}")

    by_cat = {}
    for v in violations:
        by_cat.setdefault((v["category"], v["severity"], v["suggestion"]), []).append(v)
    for (cat, severity, suggestion), vs in by_cat.items():
        label = cat.replace("_", " ") + (" (judgment call)" if severity == "soft" else "")
        hint = suggestion or "rewrite or cut"
        out.append(f"  {label}: {hint}")
        shown = vs[:MAX_PER_RULE]
        locs = "; ".join(f"L{v['line_number']}: {v['phrase'][:60]}" for v in shown)
        out.append(f"    {locs}")
        if len(vs) > len(shown):
            out.append(f"    (+{len(vs) - len(shown)} more)")

    for label, suggestion, detail in struct_flags:
        out.append(f"  {label}: {suggestion}")

    out.append("\nDetail: references/writing-style.md in the doc-builder skill.")
    sys.stderr.write("\n".join(out) + "\n")


def main():
    jobs = []  # (name, raw_text)

    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            try:
                with open(path, encoding="utf-8") as fh:
                    jobs.append((os.path.basename(path), fh.read()))
            except OSError as e:
                sys.stderr.write(f"slop_check: cannot read {path}: {e}\n")
                return 1
    else:
        data = sys.stdin.read()
        try:
            payload = json.loads(data)
        except Exception:
            payload = None
        if isinstance(payload, dict) and "tool_input" in payload:
            path = payload["tool_input"].get("file_path") or ""
            try:
                with open(path, encoding="utf-8") as fh:
                    jobs.append((os.path.basename(path), fh.read()))
            except OSError:
                pass
        elif data.strip():
            jobs.append(("<stdin>", data))

    failed = False
    for name, raw in jobs:
        house, violations, struct_flags = scan(raw)
        if house or violations or struct_flags:
            failed = True
            report(name, house, violations, struct_flags)

    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
