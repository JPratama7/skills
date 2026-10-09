#!/usr/bin/env python3
"""Run deterministic eval assertions against a run's outputs directory."""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

def resolve_output(outputs_dir: Path, relative: str) -> Path:
    path = (outputs_dir / relative).resolve()
    root = outputs_dir.resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"file escapes outputs directory: {relative}")
    return path


def json_path_value(value, path: str):
    current = value
    for part in path.split(".") if path else []:
        if isinstance(current, list):
            current = current[int(part)]
        else:
            current = current[part]
    return current


def check(assertion: dict, outputs_dir: Path) -> tuple[bool, str]:
    kind = assertion["type"]
    path = resolve_output(outputs_dir, assertion["file"])

    if kind == "file_exists":
        passed = path.is_file()
        return passed, f"{'Found' if passed else 'Missing'} {assertion['file']}"

    if not path.is_file():
        return False, f"Missing {assertion['file']}"

    if kind == "text_contains":
        found = assertion["text"] in path.read_text(encoding="utf-8")
        return found, f"{'Found' if found else 'Did not find'} expected text in {assertion['file']}"

    if kind == "regex":
        found = re.search(assertion["pattern"], path.read_text(encoding="utf-8"),
                          re.MULTILINE) is not None
        return found, f"{'Matched' if found else 'Did not match'} pattern in {assertion['file']}"

    if kind in {"json_valid", "json_value_eq"}:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            return False, f"Invalid JSON in {assertion['file']}: {error}"
        if kind == "json_valid":
            return True, f"Parsed valid JSON from {assertion['file']}"
        try:
            actual = json_path_value(data, assertion["path"])
        except (KeyError, IndexError, TypeError, ValueError) as error:
            return False, f"Could not resolve JSON path {assertion['path']!r}: {error}"
        expected = assertion["expected"]
        passed = type(actual) is type(expected) and actual == expected
        return passed, f"{assertion['path']} was {actual!r}; expected {expected!r}"

    if kind == "csv_row_count":
        with path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.reader(stream))
        count = len(rows) - (1 if assertion.get("header", True) and rows else 0)
        passed = count == assertion["expected"]
        return passed, f"Found {count} data rows; expected {assertion['expected']}"

    raise ValueError(f"unsupported assertion type: {kind}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assertions", type=Path, help="JSON file containing an assertion array")
    parser.add_argument("outputs_dir", type=Path, help="Run outputs directory")
    parser.add_argument("-o", "--output", type=Path, default=Path("grading.json"),
                        help="Write deterministic grading JSON (default: grading.json)")
    args = parser.parse_args()

    try:
        assertions = json.loads(args.assertions.read_text(encoding="utf-8"))
        if not isinstance(assertions, list):
            raise ValueError("assertions file must contain a JSON array")
        checks = []
        seen_ids = set()
        for assertion in assertions:
            if not isinstance(assertion, dict):
                raise ValueError("each assertion must be a JSON object")
            for field in ("id", "type", "file"):
                if field not in assertion:
                    raise ValueError(f"assertion is missing required field {field!r}")
            if not isinstance(assertion["id"], str) or not assertion["id"]:
                raise ValueError("assertion id must be a non-empty string")
            if assertion["id"] in seen_ids:
                raise ValueError(f"duplicate assertion id: {assertion['id']}")
            seen_ids.add(assertion["id"])
            passed, evidence = check(assertion, args.outputs_dir)
            checks.append({"text": assertion["id"], "passed": passed, "evidence": evidence})
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, re.error) as error:
        print(f"Invalid assertion contract or check error: {error}", file=sys.stderr)
        return 2

    passed = sum(check_result["passed"] for check_result in checks)
    total = len(checks)
    grading = {
        "expectations": checks,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": passed / total if total else 1.0,
        },
    }
    rendered = json.dumps(grading, indent=2) + "\n"
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
