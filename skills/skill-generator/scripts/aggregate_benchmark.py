#!/usr/bin/env python3
"""Aggregate eval run results into benchmark.json and benchmark.md."""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def stats(values: list) -> dict:
    values = [v for v in values if isinstance(v, (int, float))]
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    n = len(values)
    mean = sum(values) / n
    stddev = 0.0
    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def load_grading(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def normalize_checks(grading: dict) -> list:
    """The checks list, named `expectations` (documented) or `checks` (variant)."""
    checks = grading.get("expectations") or grading.get("checks") or []
    return checks if isinstance(checks, list) else []


def normalize_summary(grading: dict) -> dict:
    """Coerce grading.json into the canonical summary dict.

    Verifiers in the wild write `summary` as either the documented dict
    ({passed, failed, total, pass_rate}) or a human-readable string. When
    stats are missing, derive them from the checks list, which may be
    named `expectations` (documented) or `checks` (common variant).
    """
    checks = normalize_checks(grading)
    summary = grading.get("summary")
    if isinstance(summary, dict) and "total" in summary:
        passed = summary.get("passed", 0)
        total = summary.get("total", 0)
        pass_rate = summary.get("pass_rate")
        if not isinstance(pass_rate, (int, float)):
            pass_rate = passed / total if total else 0.0
        return {
            "passed": passed,
            "failed": summary.get("failed", total - passed),
            "total": total,
            "pass_rate": pass_rate,
        }
    total = len(checks)
    passed = sum(1 for c in checks if isinstance(c, dict) and c.get("passed"))
    failed = total - passed
    return {
        "passed": passed,
        "failed": failed,
        "total": total,
        "pass_rate": passed / total if total else 0.0,
    }


def normalize_timing(grading: dict, timing_file: Path) -> dict:
    timing = grading.get("timing")
    if not isinstance(timing, dict):
        timing = {}
    if not timing and timing_file.exists():
        try:
            with open(timing_file) as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    timing = loaded
        except (json.JSONDecodeError, OSError):
            pass
    seconds = timing.get("total_duration_seconds")
    if not isinstance(seconds, (int, float)):
        ms = timing.get("duration_ms")
        seconds = ms / 1000.0 if isinstance(ms, (int, float)) else 0.0
    return {"total_duration_seconds": seconds}


def collect_runs(benchmark_dir: Path) -> dict:
    """Collect results grouped by configuration name."""
    results: dict[str, list] = {}

    for eval_dir in sorted(benchmark_dir.glob("eval-*")):
        if not eval_dir.is_dir():
            continue
        metadata_path = eval_dir / "eval_metadata.json"
        eval_id = 0
        eval_name = eval_dir.name
        if metadata_path.exists():
            try:
                with open(metadata_path) as f:
                    meta = json.load(f)
                    eval_id = meta.get("eval_id", 0)
                    eval_name = meta.get("eval_name") or meta.get("name") or eval_dir.name
            except (json.JSONDecodeError, OSError):
                pass

        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            config = config_dir.name
            if config not in results:
                results[config] = []

            run_dirs = sorted(config_dir.glob("run-*")) if list(config_dir.glob("run-*")) else [config_dir]
            for run_dir in run_dirs:
                grading_file = run_dir / "grading.json"
                timing_file = run_dir / "timing.json"
                if not grading_file.exists():
                    continue

                try:
                    grading = load_grading(grading_file)
                except (json.JSONDecodeError, OSError) as e:
                    print(f"Warning: cannot read {grading_file}: {e}")
                    continue

                summary = normalize_summary(grading)
                timing = normalize_timing(grading, timing_file)

                metrics = grading.get("execution_metrics", {})
                if not isinstance(metrics, dict):
                    metrics = {}

                results[config].append({
                    "eval_id": eval_id,
                    "eval_name": eval_name,
                    "run_number": int(run_dir.name.split("-")[1]) if run_dir.name.startswith("run-") else 1,
                    "pass_rate": summary["pass_rate"],
                    "passed": summary["passed"],
                    "failed": summary["failed"],
                    "total": summary["total"],
                    "time_seconds": timing["total_duration_seconds"],
                    "tokens": metrics.get("output_chars", 0),
                    "tool_calls": metrics.get("total_tool_calls", 0),
                    "errors": metrics.get("errors_encountered", 0),
                    "expectations": normalize_checks(grading),
                    "notes": [],
                })

    return results


def build_benchmark(results: dict, skill_name: str, skill_path: str) -> dict:
    runs: list[dict] = []
    for config, config_runs in results.items():
        for r in config_runs:
            runs.append({
                "eval_id": r["eval_id"],
                "eval_name": r["eval_name"],
                "configuration": config,
                "run_number": r["run_number"],
                "result": {
                    "pass_rate": r["pass_rate"],
                    "passed": r["passed"],
                    "failed": r["failed"],
                    "total": r["total"],
                    "time_seconds": r["time_seconds"],
                    "tokens": r["tokens"],
                    "tool_calls": r["tool_calls"],
                    "errors": r["errors"],
                },
                "expectations": r["expectations"],
                "notes": r["notes"],
            })

    run_summary: dict = {}
    for config, config_runs in results.items():
        run_summary[config] = {
            "pass_rate": stats([r["pass_rate"] for r in config_runs]),
            "time_seconds": stats([r["time_seconds"] for r in config_runs]),
            "tokens": stats([r["tokens"] for r in config_runs]),
        }

    configs = list(results.keys())
    # Delta reads as "candidate - baseline": prefer with_skill as primary so
    # improvement evals (vs old_skill/without_skill) get a positive delta.
    order = ["with_skill"] + [c for c in configs if c != "with_skill"]
    if len(order) >= 2:
        primary = run_summary[order[0]]
        baseline = run_summary[order[1]]
    elif configs:
        primary = run_summary[configs[0]]
        baseline = {}
    else:
        primary = baseline = {}

    run_summary["delta"] = {
        "pass_rate": f"{primary.get('pass_rate', {}).get('mean', 0) - baseline.get('pass_rate', {}).get('mean', 0):+.2f}",
        "time_seconds": f"{primary.get('time_seconds', {}).get('mean', 0) - baseline.get('time_seconds', {}).get('mean', 0):+.1f}",
        "tokens": f"{primary.get('tokens', {}).get('mean', 0) - baseline.get('tokens', {}).get('mean', 0):+.0f}",
    }

    return {
        "metadata": {
            "skill_name": skill_name or "<skill-name>",
            "skill_path": skill_path or "<path/to/skill>",
            "executor_model": "<model-id>",
            "analyzer_model": "<model-id>",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run": sorted({r["eval_id"] for r in runs}),
            "runs_per_configuration": max(len(r) for r in results.values()) if results else 0,
        },
        "runs": runs,
        "run_summary": run_summary,
        "notes": [],
    }


def build_markdown(benchmark: dict) -> str:
    meta = benchmark["metadata"]
    run_summary = benchmark["run_summary"]
    configs = [k for k in run_summary if k != "delta"]

    lines = [
        f"# Benchmark: {meta['skill_name']}",
        "",
        f"- Model: {meta['executor_model']}",
        f"- Date: {meta['timestamp']}",
        "",
        "| Config | Pass Rate | Time | Tokens |",
        "|--------|-----------|------|--------|",
    ]

    for config in configs:
        s = run_summary[config]
        pr = s["pass_rate"]
        t = s["time_seconds"]
        tok = s["tokens"]
        lines.append(
            f"| {config} | {pr['mean']*100:.0f}% ± {pr['stddev']*100:.0f}% | "
            f"{t['mean']:.1f}s ± {t['stddev']:.1f}s | {tok['mean']:.0f} ± {tok['stddev']:.0f} |"
        )

    delta = run_summary.get("delta", {})
    lines.append(
        f"| Delta | {delta.get('pass_rate', '—')} | {delta.get('time_seconds', '—')} | {delta.get('tokens', '—')} |"
    )

    if benchmark.get("notes"):
        lines.extend(["", "## Notes", ""])
        for note in benchmark["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Aggregate eval results into benchmark.json")
    parser.add_argument("benchmark_dir", type=Path, help="Path to the iteration directory")
    parser.add_argument("--skill-name", default="", help="Skill name")
    parser.add_argument("--skill-path", default="", help="Skill path")
    parser.add_argument("-o", "--output", type=Path, help="Output JSON path")
    args = parser.parse_args()

    if not args.benchmark_dir.exists():
        print(f"Directory not found: {args.benchmark_dir}")
        sys.exit(1)

    results = collect_runs(args.benchmark_dir)
    benchmark = build_benchmark(results, args.skill_name, args.skill_path)

    out_json = args.output or (args.benchmark_dir / "benchmark.json")
    out_md = out_json.with_suffix(".md")

    with open(out_json, "w") as f:
        json.dump(benchmark, f, indent=2)
    print(f"Wrote {out_json}")

    with open(out_md, "w") as f:
        f.write(build_markdown(benchmark))
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
