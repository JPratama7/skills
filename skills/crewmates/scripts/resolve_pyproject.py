"""Resolve a cherry-pick conflict in a pyproject.toml whose only change on their side is dependencies or extras.

Usage: python3 resolve_pyproject.py PATH   (run inside the repository, during a conflicted cherry-pick)

The result is ours (index stage 2), plus the dependencies and optional extras their side (stage 3) added. Each added
entry keeps the comment lines right above it, and the dependency list is sorted. Exits 1, leaving the file untouched,
when their side changed anything else relative to the base (stage 1), so a real edit is never dropped silently.
"""

import re
import subprocess
import sys
import tomllib

DEPS = re.compile(r"(dependencies = \[\n)(.*?)(\n\])", re.S)
EXTRAS = re.compile(r"\[project\.optional-dependencies\]\n(.*?)(?=\n\[|\Z)", re.S)


def stage(path: str, n: int) -> str:
    return subprocess.run(["git", "show", f":{n}:{path}"], capture_output=True, text=True, check=True).stdout


def without_deps(text: str) -> dict:
    data = tomllib.loads(text)
    data.get("project", {}).pop("dependencies", None)
    data.get("project", {}).pop("optional-dependencies", None)
    return data


def entries(block: str, key) -> dict[str, str]:
    """Each entry line, keyed by `key(line)`, with the comment lines directly above it."""
    out, pending = {}, ""
    for line in block.splitlines(keepends=True):
        if line.strip().startswith("#"):
            pending += line
        elif line.strip():
            out.setdefault(key(line), pending + line)
            pending = ""
    return out


def merge_deps(ours: str, theirs: str) -> str:
    mo, mt = DEPS.search(ours), DEPS.search(theirs)
    if not mo or not mt:
        return ours
    items = entries(mo.group(2) + "\n", str.strip)
    for k, v in entries(mt.group(2) + "\n", str.strip).items():
        items.setdefault(k, v)
    body = "".join(items[k] for k in sorted(items, key=str.lower)).rstrip("\n")
    return ours[: mo.start(2)] + body + ours[mo.end(2) :]


def extra_name(line: str) -> str:
    return line.split("=", 1)[0].strip()


def merge_extras(merged: str, ours: str, theirs: str) -> str:
    mo, mt = EXTRAS.search(ours), EXTRAS.search(theirs)
    o = entries(mo.group(1), extra_name) if mo else {}
    t = entries(mt.group(1), extra_name) if mt else {}
    clash = [n for n in t if n in o and o[n].strip() != t[n].strip()]
    if clash:
        sys.exit(f"extras changed on both sides: {clash}")
    added = "".join(v for n, v in t.items() if n not in o)
    if not added:
        return merged
    if not mo:
        return merged.replace("\n[build-system]", "\n[project.optional-dependencies]\n" + added + "\n[build-system]", 1)
    m = EXTRAS.search(merged)
    return merged[: m.end(1)].rstrip("\n") + "\n" + added.rstrip("\n") + "\n" + merged[m.end(1) :]


def main() -> None:
    path = sys.argv[1]
    base, ours, theirs = stage(path, 1), stage(path, 2), stage(path, 3)
    if without_deps(theirs) != without_deps(base):
        sys.exit(f"{path}: their side changed more than dependencies/extras")
    merged = merge_extras(merge_deps(ours, theirs), ours, theirs)
    tomllib.loads(merged)  # must still parse
    with open(path, "w") as f:
        f.write(merged)


if __name__ == "__main__":
    main()
