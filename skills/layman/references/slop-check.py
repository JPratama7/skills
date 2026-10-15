#!/usr/bin/env python3
"""Scan a text file for AI writing tells. Prints findings, exits 2 if any.

Two layers:
  1. The vendored unslop scanner stack (references/unslop/scripts/):
     phrase scanner (contextually gated, quotes/code masked), structure
     metrics (burstiness, triads, connective scaffolds, codas), and the
     silhouette scorer (idea-arrangement tells).
  2. Local regexes for gaps unslop intentionally leaves: smart
     punctuation, leaked model artifacts, Title Case headings, em
     dashes (house rule: zero), label-colon bullets under unslop's
     count of 3, and bare-word vocabulary/phrase recall.

Usage:
    python3 slop-check.py FILE [--genre docs|social|prose]
    echo '{"tool_input":{"file_path":"FILE"}}' | python3 slop-check.py

unslop stack: MIT, https://github.com/theclaymethod/unslop (claytonkim).
Local regexes adapted from github.com/Abdulkader-Safi/AI-Writing-Rules (MIT).
"""

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "unslop" / "scripts"))

import banned_phrase_scan  # noqa: E402
import structure_scan  # noqa: E402
import silhouette_scan  # noqa: E402
from _lang import is_probably_english  # noqa: E402

TEXT_EXT = {".md", ".mdx", ".markdown", ".txt", ".rst"}
OPT_OUT = "slop-check: off"
MAX_PER_RULE = 4

# Local rules for gaps the unslop scanners do not cover.
LOCAL_RULES = [
    ("em dash", re.compile(r"[—―‒]"), "house rule is zero; use a full stop, comma, colon, or brackets"),
    (
        "curly quote or ellipsis",
        re.compile(r"[‘’“”…]"),
        "use straight quotes and three dots",
    ),
    (
        "Title Case heading",
        re.compile(r"(?m)^#{1,6}\s+(?:[A-Z][a-z]+\s+){1,}(?:[A-Z][a-z]+)\s*$"),
        "sentence case: capital on the first word only",
    ),
    (
        "inline-header bullet",
        re.compile(r"(?m)^\s*(?:[-*+]\s+)?\*\*[^*\n:]{2,40}:?\*\*\s*:?\s*\S"),
        "write it as prose or drop the label",
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
        "trailing -ing commentary",
        re.compile(
            r",\s+(?:highlighting|underscoring|emphasizing|emphasising|ensuring|reflecting"
            r"|symbolizing|symbolising|showcasing|fostering|cultivating|paving\s+the\s+way"
            r"|allowing\s+for|contributing\s+to)\b",
            re.I,
        ),
        "cut everything after the comma",
    ),
    (
        "assistant scaffolding",
        re.compile(
            r"(?:certainly!|i\s+hope\s+this\s+helps|great\s+question"
            r"|let\s+me\s+know\s+if\s+you'?d\s+like|feel\s+free\s+to\s+(?:ask|reach)"
            r"|in\s+this\s+(?:article|guide|post),?\s+we(?:'ll|\s+will)\s+explore"
            r"|\[(?:insert|your|company\s+name|placeholder|citation\s+needed)\b)",
            re.I,
        ),
        "strip it",
    ),
    (
        "empty opener",
        re.compile(
            r"(?:^|\n)\s*(?:picture\s+this|imagine\s+a\s+world|we\s+live\s+in\s+a\s+time"
            r"|now\s+more\s+than\s+ever|it'?s\s+no\s+secret|let'?s\s+face\s+it"
            r"|as\s+technology\s+continues|in\s+an?\s+era\s+of)",
            re.I,
        ),
        "delete the sentence, start with the fact",
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
        "pseudo-wisdom",
        re.compile(
            r"\b(?:the\s+key\s+is\s+to\s+find|it\s+(?:all\s+)?(?:depends|comes\s+down\s+to)"
            r"\s+(?:on\s+)?your\s+(?:specific\s+)?needs|true\s+\w+\s+comes\s+from\s+within"
            r"|the\s+right\s+balance|context\s+is\s+everything)\b",
            re.I,
        ),
        "delete it or make it specific",
    ),
    (
        "AI vocabulary",
        re.compile(
            r"\b(?:delve[sd]?|delving|tapestry|vibrant|multifaceted|nuanced|intricate|intricacies"
            r"|realm|testament|myriad|plethora|paradigm|quintessential|interplay|indelible"
            r"|groundbreaking|cutting-edge|state-of-the-art|world-class|best-in-class"
            r"|enterprise-grade|game-chang(?:er|ing)|revolutioniz(?:e|es|ed|ing)|supercharg\w*"
            r"|renowned|resonat(?:e|es|ed|ing)?|garner(?:s|ed|ing)?|meticulous(?:ly)?"
            r"|bolster(?:s|ed|ing)?|streamlin(?:e|es|ed|ing)|empower(?:s|ed|ing)?"
            r"|embark(?:s|ed|ing)?|unlock(?:s|ed|ing)?|elevat(?:e|es|ed|ing)"
            r"|transformative|holistic|showcas(?:e|es|ed|ing))\b",
            re.I,
        ),
        "bare-word flag; replace with the plainest word that carries the meaning",
    ),
    (
        "outline ending",
        re.compile(
            r"\b(?:to\s+conclude|as\s+we\s+look\s+ahead|moving\s+forward"
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
        "make the claim or drop it",
    ),
    (
        "puffed significance",
        re.compile(
            r"\b(?:is\s+a\s+testament|plays?\s+a\s+(?:crucial|pivotal|vital|key|central)\s+role"
            r"|(?:evolving|broader|changing)\s+landscape|setting\s+the\s+stage"
            r"|significant\s+milestone|key\s+turning\s+point|left\s+an\s+indelible)\b",
            re.I,
        ),
        "state what happened, drop why it matters to the universe",
    ),
]


def strip_noise(text):
    """Blank out fenced code and inline code so we only lint prose."""
    text = re.sub(r"(?ms)^```.*?^```", lambda m: "\n" * m.group(0).count("\n"), text)
    return re.sub(r"`[^`\n]+`", " ", text)


def resolve_path(argv):
    if argv:
        return argv[0]
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return ""
    return (payload.get("tool_input") or {}).get("file_path") or ""


def main(argv):
    genre = "prose"
    args = list(argv)
    if "--genre" in args:
        i = args.index("--genre")
        if i + 1 < len(args):
            genre = args[i + 1]
        args = args[:i] + args[i + 2 :]

    path = resolve_path(args)
    if not path or os.path.splitext(path)[1].lower() not in TEXT_EXT:
        return 0
    try:
        raw = open(path, encoding="utf-8").read()
    except Exception:
        return 0
    if OPT_OUT in raw:
        return 0

    findings = []  # (source, label, hint, [(line, excerpt)])

    # --- unslop phrase layer ---
    try:
        for v in banned_phrase_scan.scan_for_violations(raw):
            findings.append(
                (
                    f"phrase/{v['category']}",
                    v["severity"],
                    v.get("suggestion") or "rewrite or cut",
                    [(v["line_number"], f'"{v["phrase"]}"')],
                )
            )
    except Exception as e:
        findings.append(("phrase layer", "info", f"scanner error: {e}", []))

    # --- unslop structure layer ---
    try:
        for f in structure_scan.scan(raw, genre)["flags"]:
            findings.append(
                (
                    f"structure/{f['metric']}",
                    f["severity"],
                    f"{f['suggestion']} [{f['metric']}={f['value']}, flag at {f['threshold']}]",
                    [],
                )
            )
    except Exception as e:
        findings.append(("structure layer", "info", f"scanner error: {e}", []))

    # --- unslop silhouette layer ---
    try:
        ref = silhouette_scan.load_reference(silhouette_scan.REFERENCE_PATH)
        for f in silhouette_scan.scan(raw, ref, genre)["flags"]:
            findings.append(
                (
                    f"silhouette/{f['metric']}",
                    f["severity"],
                    f"{f['suggestion']} [{f['metric']}={f['value']}, flag at {f['threshold']}]",
                    [],
                )
            )
    except Exception as e:
        findings.append(("silhouette layer", "info", f"scanner error: {e}", []))

    # --- local regex layer ---
    prose = strip_noise(raw)
    lines = prose.split("\n")
    for label, rx, hint in LOCAL_RULES:
        hits = []
        for n, line in enumerate(lines, 1):
            if rx.search(line):
                hits.append((n, rx.search(line).group(0).strip()[:60]))
        if hits:
            findings.append((label, "local", hint, hits))

    if not findings:
        return 0

    eng_note = "" if is_probably_english(prose) else " (input looks non-English; English-tuned checks may misfire)"
    out = [
        f"Writing rules: {len(findings)} issue(s) in {os.path.basename(path)}.{eng_note} Fix before moving on.\n"
    ]
    for label, sev, hint, hits in findings:
        shown = hits[:MAX_PER_RULE]
        more = f" (+{len(hits) - len(shown)} more)" if len(hits) > len(shown) else ""
        locs = "; ".join(f"L{n}: {t}" for n, t in shown) if shown else ""
        out.append(f"  {label} [{sev}]{more}: {hint}")
        if locs:
            out.append(f"    {locs}")
    out.append("\nDetail: references/slop.md in the layman skill.")
    sys.stderr.write("\n".join(out) + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
