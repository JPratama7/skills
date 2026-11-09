#!/usr/bin/env python3
"""inbox.py — crew inbox tool. The file is the store; this is the only
way members should touch it — one-off commands drift from the format and
silently consume nothing.

  inbox.py send NAME TEXT... [--from SENDER]   append `- from SENDER: TEXT`
  inbox.py list [NAME]                         print inbox lines
  inbox.py consume NAME [--match TEXT]         print matched lines AND
                                               remove them, in one locked
                                               read-modify-write — a miss
                                               prints nothing, never eats

--match is a plain substring (prefix-matching is how lines get missed);
anchor it yourself if you need a line-start. consume without --match
takes every line. Inbox dir: --dir, default .crew/inbox.
"""

import argparse
import fcntl
import os
import sys


def inbox_path(args, name: str) -> str:
    return os.path.join(args.dir, f"{name}.md")


def cmd_send(args) -> int:
    path = inbox_path(args, args.name)
    os.makedirs(args.dir, exist_ok=True)
    sender = args.sender or os.environ.get("CREW_SENDER") or "unknown"
    line = f"- from {sender}: {' '.join(args.text)}\n"
    with open(path, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line)
    print(f"sent → {args.name}: {' '.join(args.text)}", file=sys.stderr)
    return 0


def _lines(path: str) -> list[str]:
    return open(path).read().splitlines(keepends=True) if os.path.exists(path) else []


def cmd_list(args) -> int:
    names = [args.name] if args.name else sorted(
        f[:-3] for f in os.listdir(args.dir) if f.endswith(".md")
    ) if os.path.isdir(args.dir) else []
    for name in names:
        lines = _lines(inbox_path(args, name))
        if lines:
            print(f"== {name} ==")
            print("".join(lines), end="")
    return 0


def cmd_consume(args) -> int:
    path = inbox_path(args, args.name)
    lines = _lines(path)
    matched = [l for l in lines if args.match is None or args.match in l]
    rest = [l for l in lines if l not in matched]
    if os.path.exists(path):
        with open(path, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            f.truncate()
            f.writelines(rest)
    print("".join(matched), end="")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--dir", default=".crew/inbox")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("send")
    s.add_argument("name")
    s.add_argument("text", nargs="+")
    s.add_argument("--from", dest="sender")
    s.set_defaults(fn=cmd_send)

    s = sub.add_parser("list")
    s.add_argument("name", nargs="?")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("consume")
    s.add_argument("name")
    s.add_argument("--match")
    s.set_defaults(fn=cmd_consume)

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
