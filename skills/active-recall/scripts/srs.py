#!/usr/bin/env python3
"""srs.py — minimal spaced-repetition deck manager (SM-2 lite). Stdlib only.

Deck layout (all inside <deck-dir>):
  cards.jsonl   canonical card store, one JSON object per line:
                {"id","type","q","a","tags","src"}
  state.json    scheduling state per card + review log
  exports/      generated export files (anki.tsv, deck.md, ...)

Commands: init, add, lint, due, grade, stats, export. Run `<cmd> -h` for
flags.
"""

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

CARDS_FILE = "cards.jsonl"
STATE_FILE = "state.json"
DEFAULT_EASE = 2.5
MIN_EASE = 1.3
GRADES = (0, 1, 2, 3, 4, 5)


# ---------- storage ----------

def deck_dir(p):
    d = Path(p)
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_cards(d):
    f = d / CARDS_FILE
    if not f.exists():
        return []
    cards = []
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            cards.append(json.loads(line))
        except json.JSONDecodeError as e:
            die(f"{CARDS_FILE} line {i}: invalid JSON: {e}")
    return cards


def save_cards(d, cards):
    (d / CARDS_FILE).write_text(
        "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cards),
        encoding="utf-8")


def load_state(d):
    f = d / STATE_FILE
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"deck": d.name, "cards": {}, "log": []}


def save_state(d, st):
    (d / STATE_FILE).write_text(json.dumps(st, ensure_ascii=False, indent=1),
                                encoding="utf-8")


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def norm_q(q):
    return re.sub(r"\s+", " ", q.strip().lower())


def new_card_state():
    return {"seen": False, "reps": 0, "lapses": 0, "ease": DEFAULT_EASE,
            "interval": 0, "due": None, "last_grade": None}


def parse_date(s):
    if not s:
        return date.today()
    return date.fromisoformat(s)


# ---------- commands ----------

def cmd_init(args):
    d = deck_dir(args.deck)
    if not (d / STATE_FILE).exists():
        save_state(d, {"deck": args.name or d.name, "cards": {}, "log": []})
    if not (d / CARDS_FILE).exists():
        save_cards(d, [])
    print(json.dumps({"deck": (d / STATE_FILE and load_state(d)["deck"]),
                      "dir": str(d)}))


def cmd_add(args):
    d = deck_dir(args.deck)
    cards = load_cards(d)
    state = load_state(d)
    have = {norm_q(c["q"]) for c in cards}
    n = max([int(c["id"][1:]) for c in cards
             if re.fullmatch(r"c\d+", c.get("id", ""))] or [0])
    added, skipped, errors = 0, 0, []
    src_lines = (sys.stdin.read().splitlines() if args.file == "-"
                 else Path(args.file).read_text(encoding="utf-8").splitlines())
    for i, line in enumerate(src_lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            c = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"line {i}: invalid JSON ({e})")
            continue
        if not c.get("q") or not isinstance(c["q"], str):
            errors.append(f"line {i}: missing 'q'")
            continue
        if norm_q(c["q"]) in have:
            skipped += 1
            continue
        ctype = c.get("type", "qa")
        if ctype not in ("qa", "cloze"):
            errors.append(f"line {i}: bad type {ctype!r} (use qa|cloze)")
            continue
        if ctype == "qa" and not c.get("a"):
            errors.append(f"line {i}: qa card missing 'a'")
            continue
        if ctype == "cloze" and not re.search(r"\{\{c\d+::", c["q"]):
            errors.append(f"line {i}: cloze card without {{{{cN::..}}}} marker")
            continue
        n += 1
        card = {"id": f"c{n}", "type": ctype, "q": c["q"].strip(),
                "a": c.get("a", "").strip(),
                "tags": list(c.get("tags", [])),
                "src": c.get("src", "")}
        cards.append(card)
        state["cards"][card["id"]] = new_card_state()
        have.add(norm_q(card["q"]))
        added += 1
    save_cards(d, cards)
    save_state(d, state)
    print(json.dumps({"added": added, "skipped_dupes": skipped,
                      "errors": errors, "total": len(cards)}))


YESNO_RE = re.compile(
    r"^(?:is|are|was|were|do|does|did|can|could|will|would|should|has|have|had)\b",
    re.I)
MULTI_Q_RE = re.compile(
    r"\b(?:name|list|give|state)\s+(?:all|every|each)\b"
    r"|\ball of the above\b|\bwhich of the following\b"
    r"|\bwhat is true about\b", re.I)


def lint_card(c):
    w = []
    q = (c.get("q") or "").strip()
    a = (c.get("a") or "").strip()
    if not q:
        return w
    if YESNO_RE.match(q):
        w.append("yes/no-style question stem; force a discrimination instead")
    if MULTI_Q_RE.search(q):
        w.append("multi-item or recognition-cued question; split or re-cue")
    if c.get("type", "qa") == "cloze":
        idx = set(re.findall(r"\{\{c(\d+)::", q))
        if len(idx) > 1:
            w.append("multiple cloze indices; occlude one item per card")
        elif not idx:
            w.append("cloze card without {{cN::..}} marker")
    elif len(a.split()) > 25:
        w.append(f"answer is {len(a.split())} words; keep ≤25 or split")
    if ";" in a or a.count(",") >= 2:
        w.append("answer looks multi-part")
    return w


def cmd_lint(args):
    p = Path(args.path)
    f = p / CARDS_FILE if p.is_dir() else p
    if not f.exists():
        die(f"no such file: {f}")
    warns, n = [], 0
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        n += 1
        where = f"line {i}"
        try:
            c = json.loads(line)
        except json.JSONDecodeError as e:
            warns.append({"card": where, "warning": f"invalid JSON ({e})"})
            continue
        for msg in lint_card(c):
            warns.append({"card": c.get("id") or where, "warning": msg,
                          "q": (c.get("q") or "")[:80]})
    print(json.dumps({"file": str(f), "cards": n, "warnings": warns},
                     indent=1))


def cmd_due(args):
    d = deck_dir(args.deck)
    today = parse_date(args.date)
    cards = {c["id"]: c for c in load_cards(d)}
    state = load_state(d)["cards"]
    relearn, review, fresh = [], [], []
    for cid, st in state.items():
        c = cards.get(cid)
        if not c:
            continue
        due = date.fromisoformat(st["due"]) if st["due"] else None
        if not st["seen"]:
            fresh.append(c)
        elif due and due <= today:
            (relearn if st["interval"] == 0 else review).append(
                (due, c))
    out = [dict(c, status="relearn") for _, c in
           sorted(relearn, key=lambda t: t[0])]
    out += [dict(c, status="review") for _, c in
            sorted(review, key=lambda t: t[0])]
    out += [dict(c, status="new") for c in fresh[: args.new]]
    print(json.dumps(out[: args.limit], ensure_ascii=False, indent=1))


def cmd_grade(args):
    d = deck_dir(args.deck)
    today = parse_date(args.date)
    st_all = load_state(d)
    st = st_all["cards"].get(args.id)
    if st is None:
        die(f"no card {args.id!r} in state")
    g = args.grade
    if g not in GRADES:
        die(f"grade must be one of {GRADES}")
    if g < 3:
        st["reps"] = 0
        st["lapses"] += 1
        st["interval"] = 0
        st["ease"] = max(MIN_EASE, round(st["ease"] - 0.2, 3))
        st["due"] = today.isoformat()
    else:
        st["reps"] += 1
        if st["reps"] == 1:
            st["interval"] = 1
        elif st["reps"] == 2:
            st["interval"] = 6
        else:
            st["interval"] = max(1, round(st["interval"] * st["ease"]))
        st["ease"] = max(
            MIN_EASE,
            round(st["ease"] + 0.1 - (5 - g) * (0.08 + (5 - g) * 0.02), 3))
        st["due"] = (today + timedelta(days=st["interval"])).isoformat()
    st["seen"] = True
    st["last_grade"] = g
    st_all["log"].append({"date": today.isoformat(), "id": args.id,
                          "grade": g, "interval": st["interval"]})
    save_state(d, st_all)
    print(json.dumps({args.id: st}, indent=1))


def cmd_stats(args):
    d = deck_dir(args.deck)
    today = parse_date(args.date)
    cards = load_cards(d)
    state = load_state(d)["cards"]
    new = due = relearn = learned = 0
    eases = []
    for cid, st in state.items():
        if not st["seen"]:
            new += 1
            continue
        learned += 1
        eases.append(st["ease"])
        if st["due"] and date.fromisoformat(st["due"]) <= today:
            if st["interval"] == 0:
                relearn += 1
            else:
                due += 1
    print(json.dumps({
        "total_cards": len(cards), "new": new, "due_today": due,
        "relearning": relearn, "learned": learned,
        "avg_ease": round(sum(eases) / len(eases), 2) if eases else None,
        "reviews_logged": len(load_state(d)["log"]),
    }, indent=1))


# ---------- export ----------

def esc_field(s):
    return s.replace("\t", " ").replace("\n", "<br>")


def cloze_to_highlight(s):
    return re.sub(r"\{\{c\d+::(.*?)\}\}", r"==\1==", s)


def cloze_to_plain(s):
    return re.sub(r"\{\{c\d+::(.*?)\}\}", r"[...]\1[...]", s)


def cmd_export(args):
    d = deck_dir(args.deck)
    cards = load_cards(d)
    deck = load_state(d).get("deck", d.name)
    ex = d / "exports"
    ex.mkdir(exist_ok=True)
    outs = {}
    if "anki" in args.formats:
        p = ex / "anki.tsv"
        p.write_text("".join(
            f"{esc_field(c['q'])}\t{esc_field(c['a'])}\t{' '.join(c['tags'])}\n"
            for c in cards), encoding="utf-8")
        outs["anki"] = str(p)
    if "md" in args.formats:
        p = ex / "deck.md"
        parts = [f"# Deck: {deck}\n"]
        for c in cards:
            t = f"  `{' '.join(c['tags'])}`" if c["tags"] else ""
            if c["type"] == "cloze":
                parts.append(f"### {c['id']}{t}\n\n{c['q']}\n")
            else:
                parts.append(f"### {c['id']}{t}\n\n**Q:** {c['q']}\n\n**A:** {c['a']}\n")
        p.write_text("\n".join(parts), encoding="utf-8")
        outs["md"] = str(p)
    if "obsidian" in args.formats:
        p = ex / "obsidian.md"
        parts = [f"<!-- deck: {deck} -->\n"]
        for c in cards:
            if c["type"] == "cloze":
                parts.append(cloze_to_highlight(c["q"]))
            else:
                parts.append(f"{c['q']}\n?\n{c['a']}")
        p.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
        outs["obsidian"] = str(p)
    if "mochi" in args.formats:
        p = ex / "mochi.md"
        parts = []
        for c in cards:
            q = (cloze_to_plain(c["q"]) if c["type"] == "cloze" else c["q"])
            a = c["a"] or "(see deletions)"
            if c["tags"]:
                a += "\n\n" + " ".join(f"#{t}" for t in c["tags"])
            parts.append(f"{q}\n---\n{a}")
        p.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
        outs["mochi"] = str(p)
    print(json.dumps(outs, indent=1))


def main():
    ap = argparse.ArgumentParser(prog="srs.py")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("deck")
    p.add_argument("--name")
    p.set_defaults(f=cmd_init)

    p = sub.add_parser("add")
    p.add_argument("deck")
    p.add_argument("file", help="JSONL file of cards, or - for stdin")
    p.set_defaults(f=cmd_add)

    p = sub.add_parser("lint", help="quality warnings for a draft JSONL "
                                    "file, or a deck dir's cards.jsonl")
    p.add_argument("path")
    p.set_defaults(f=cmd_lint)

    p = sub.add_parser("due")
    p.add_argument("deck")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--new", type=int, default=10,
                   help="max never-seen cards to include")
    p.add_argument("--date")
    p.set_defaults(f=cmd_due)

    p = sub.add_parser("grade")
    p.add_argument("deck")
    p.add_argument("id")
    p.add_argument("grade", type=int)
    p.add_argument("--date")
    p.set_defaults(f=cmd_grade)

    p = sub.add_parser("stats")
    p.add_argument("deck")
    p.add_argument("--date")
    p.set_defaults(f=cmd_stats)

    p = sub.add_parser("export")
    p.add_argument("deck")
    p.add_argument("--formats", nargs="+",
                   choices=["anki", "md", "obsidian", "mochi"],
                   default=["md", "anki"])
    p.set_defaults(f=cmd_export)

    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
