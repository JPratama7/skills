#!/usr/bin/env python3
"""Package a skill folder into a .skill zip."""

import argparse
import fnmatch
import sys
import zipfile
from pathlib import Path

from quick_validate import validate_skill

EXCLUDE_DIRS = {"__pycache__", ".git", ".local", ".venv", "node_modules", "evals"}
EXCLUDE_GLOBS = {"*.pyc", "*.pyo", ".DS_Store"}


def should_exclude(rel_path: Path) -> bool:
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if any(fnmatch.fnmatch(rel_path.name, pat) for pat in EXCLUDE_GLOBS):
        return True
    # Exclude root-level 'evals/' directory.
    if len(parts) > 1 and parts[1] == "evals":
        return True
    return False


def package_skill(skill_path: Path, output_dir: Path | None = None) -> Path | None:
    skill_path = skill_path.resolve()
    if not skill_path.is_dir():
        print(f"Error: not a directory: {skill_path}")
        return None

    print("Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"Validation failed: {message}")
        return None
    print(f"  {message}")

    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd()

    out_file = output_dir / f"{skill_path.name}.skill"

    with zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob("*"):
            if not file_path.is_file():
                continue
            arcname = file_path.relative_to(skill_path)
            if should_exclude(arcname):
                print(f"  skipped: {arcname}")
                continue
            zf.write(file_path, arcname)
            print(f"  added: {arcname}")

    print(f"Packaged to: {out_file}")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="Package a skill into a .skill file")
    parser.add_argument("skill_dir", type=Path, help="Path to the skill directory")
    parser.add_argument("-o", "--output", type=Path, help="Output directory")
    args = parser.parse_args()

    out = package_skill(args.skill_dir, args.output)
    sys.exit(0 if out else 1)


if __name__ == "__main__":
    main()
