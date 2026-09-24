#!/usr/bin/env python3
"""Quick validation for SKILL.md-based skills. Stdlib only."""

import re
import sys
from pathlib import Path

ALLOWED_KEYS = {
    "name",
    "version",
    "description",
    "compatibility",
    "metadata",
    "license",
    "allowed-tools",
    "harness",
}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+.]?[A-Za-z0-9-]+)*$")


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(block: str) -> dict:
    """Parse a flat subset of YAML: top-level scalars plus one nesting level.

    Sufficient for skill frontmatter validation; not a general YAML parser.
    """
    fm: dict = {}
    last = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] not in " \t":
            m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", raw)
            if not m:
                continue
            fm[m.group(1)] = _unquote(m.group(2).strip())
            last = m.group(1)
        elif last:
            fm[last] = f"{fm[last]} {raw.strip()}".strip()
    return {k: _unquote(v) for k, v in fm.items()}


def validate_skill(skill_path: Path):
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter = parse_frontmatter(match.group(1))

    unexpected = set(frontmatter.keys()) - ALLOWED_KEYS
    if unexpected:
        return False, f"Unexpected frontmatter key(s): {', '.join(sorted(unexpected))}"

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"

    name = frontmatter.get("name", "")
    if not name:
        return False, "'name' must be a non-empty string"
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"Name '{name}' must be kebab-case (lowercase, digits, hyphens)"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' has invalid hyphen placement"
    if len(name) > 64:
        return False, f"Name '{name}' is too long ({len(name)} > 64)"

    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"
    description = frontmatter.get("description", "")
    if not description:
        return False, "'description' must be a non-empty string"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return False, f"Description is too long ({len(description)} > 1024)"

    if "version" in frontmatter:
        version = frontmatter.get("version", "")
        if not version:
            return False, "'version' must be a non-empty string"
        if not SEMVER_RE.match(version):
            return False, f"Version '{version}' does not look like semver"

    if "compatibility" in frontmatter and len(frontmatter["compatibility"]) > 500:
        return False, "'compatibility' is too long (> 500)"

    return True, f"Skill '{frontmatter['name']}' is valid"


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <skill-directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
