#!/usr/bin/env python3
"""Generate a standalone review.html from an eval iteration directory.

Stdlib only; no server needed. Scans iteration-N/ for eval-*/<config>/ runs,
embeds outputs and grading, and adds a feedback form whose button downloads:

    {"reviews": [{"run_id": "...", "feedback": "..."}]}

Usage:
    python make_review.py <iteration-dir> --skill-name <skill> [-o review.html]
                          [--previous-feedback old-feedback.json]
"""

import argparse
import base64
import json
import sys
from html import escape
from pathlib import Path

METADATA_FILES = {"eval_metadata.json", "grading.json", "timing.json", "metrics.json"}
TEXT_EXTS = {
    ".md", ".markdown", ".txt", ".json", ".jsonl", ".csv", ".tsv", ".py", ".js",
    ".mjs", ".ts", ".tsx", ".jsx", ".html", ".css", ".yaml", ".yml", ".toml",
    ".sh", ".env", ".ini", ".cfg", ".xml", ".sql", ".rs", ".go", ".c", ".h",
    ".cpp", ".hpp", ".rb", ".php", ".java", ".kt", ".swift", ".log",
}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".pdf": "application/pdf",
}
MAX_TEXT_CHARS = 200_000


def esc(value) -> str:
    return escape(str(value))

CSS = """
body{font-family:system-ui,sans-serif;margin:0;background:#141414;color:#ddd}
header{padding:16px 24px;background:#1c1c1c;border-bottom:1px solid #333}
h1{font-size:18px;margin:0 0 8px}.sub{color:#888;font-size:13px;margin-top:6px}
table{border-collapse:collapse;font-size:13px;margin-top:8px}
td,th{border:1px solid #333;padding:4px 10px;text-align:left}
main{max-width:1100px;margin:0 auto;padding:16px}
.eval{border:1px solid #333;border-radius:8px;margin:20px 0;overflow:hidden}
.eval>h2{font-size:15px;margin:0;padding:10px 14px;background:#1c1c1c}
.prompt{padding:10px 14px;color:#999;font-size:13px;white-space:pre-wrap}
.run{padding:12px 14px;border-top:1px solid #2a2a2a}
.run h3{font-size:13px;margin:0 0 8px;color:#8ab4f8}
.muted{color:#777;font-size:12px}
details{margin:6px 0}summary{cursor:pointer;color:#8ab4f8;font-size:13px}
pre{background:#191919;border:1px solid #2a2a2a;border-radius:4px;padding:8px;
    font-size:12px;max-height:420px;overflow:auto;white-space:pre-wrap}
textarea{width:100%;box-sizing:border-box;min-height:56px;background:#191919;
         color:#ddd;border:1px solid #333;border-radius:4px;padding:6px;font:inherit}
button{background:#2e7d32;color:#fff;border:0;border-radius:4px;padding:8px 16px;
       font:inherit;cursor:pointer;margin:12px 0}
img{max-width:100%}
"""


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def collect_outputs(outputs_dir: Path) -> list[dict]:
    files = []
    for f in sorted(outputs_dir.rglob("*")):
        if not f.is_file() or f.name in METADATA_FILES:
            continue
        rel = f.relative_to(outputs_dir).as_posix()
        ext = f.suffix.lower()
        if ext in TEXT_EXTS:
            try:
                content = f.read_text(errors="replace")
            except OSError:
                content = "(unreadable)"
            if len(content) > MAX_TEXT_CHARS:
                content = content[:MAX_TEXT_CHARS] + "\n... (truncated)"
            files.append({"name": rel, "type": "text", "content": content})
        else:
            try:
                raw = f.read_bytes()
            except OSError:
                files.append({"name": rel, "type": "error", "content": "(unreadable)"})
                continue
            b64 = base64.b64encode(raw).decode("ascii")
            if ext in MIME:
                mime = MIME[ext]
                kind = "pdf" if ext == ".pdf" else "image"
                files.append({"name": rel, "type": kind, "mime": mime, "b64": b64})
            else:
                files.append({"name": rel, "type": "binary",
                              "mime": "application/octet-stream", "b64": b64})
    return files


def build_run(root: Path, run_dir: Path) -> dict | None:
    meta = {}
    for cand in (run_dir / "eval_metadata.json", run_dir.parent / "eval_metadata.json"):
        if cand.exists():
            meta = load_json(cand) or {}
            if meta.get("prompt"):
                break

    grading = None
    grading_file = run_dir / "grading.json"
    if grading_file.exists():
        data = load_json(grading_file)
        if isinstance(data, dict):
            grading = data if "expectations" in data else {"expectations": data.get("expectations", []),
                                                           "summary": data.get("summary", {})}

    timing = None
    timing_file = run_dir / "timing.json"
    if timing_file.exists():
        timing = load_json(timing_file)

    return {
        "id": run_dir.relative_to(root).as_posix(),
        "dir": run_dir,
        "config": run_dir.name,
        "eval_id": meta.get("eval_id", 0),
        "eval_name": meta.get("eval_name", run_dir.parent.name),
        "prompt": meta.get("prompt", ""),
        "outputs": collect_outputs(run_dir / "outputs"),
        "grading": grading,
        "timing": timing,
    }


def find_runs(root: Path) -> list[dict]:
    runs = []
    for path in sorted(root.rglob("*")):
        if not path.is_dir() or not (path / "outputs").is_dir():
            continue
        if any(r["dir"] in path.parents for r in runs):
            continue
        run = build_run(root, path)
        if run:
            runs.append(run)
    runs.sort(key=lambda r: (r["eval_id"], r["id"]))
    return runs


def render_run(run: dict) -> str:
    parts = [f'<div class="run"><h3>{esc(run["config"])}</h3>']
    if run.get("timing") and run["timing"].get("duration_ms") is not None:
        parts.append(f'<div class="muted">timing: {esc(run["timing"])}</div>')
    exps = (run.get("grading") or {}).get("expectations") or []
    if exps:
        rows = "".join(
            f'<tr><td class="{"ok" if e.get("passed") else "bad"}">'
            f'{"PASS" if e.get("passed") else "FAIL"}</td>'
            f'<td>{esc(e.get("text", ""))}</td>'
            f'<td>{esc(e.get("evidence", ""))}</td></tr>'
            for e in exps
        )
        s = (run.get("grading") or {}).get("summary", {})
        parts.append(f'<div class="muted">grading: {esc(s.get("passed", "?"))}/'
                     f'{esc(s.get("total", "?"))} passed</div>'
                     f'<table><tr><th>result</th><th>assertion</th><th>evidence</th></tr>{rows}</table>')
    else:
        parts.append('<div class="muted">no grading.json</div>')
    for out in run["outputs"]:
        name = esc(out["name"])
        if out["type"] == "text":
            parts.append(f'<details><summary>{name}</summary><pre>{esc(out["content"])}</pre></details>')
        elif out["type"] == "image":
            parts.append(f'<details><summary>{name}</summary>'
                         f'<img alt="{name}" src="data:{out['mime']};base64,{out['b64']}"></details>')
        elif out["type"] == "pdf":
            parts.append(f'<details><summary>{name}</summary>'
                         f'<a download="{name}" href="data:application/pdf;base64,{out["b64"]}">download</a></details>')
        else:
            parts.append(f'<details><summary>{name}</summary>'
                         f'<a download="{name}" href="data:application/octet-stream;base64,{out['b64']}">download</a></details>')
    parts.append(f'<textarea placeholder="feedback for this run" data-run="{esc(run['id'])}"></textarea>')
    parts.append("</div>")
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Generate standalone review.html")
    ap.add_argument("iteration_dir", type=Path)
    ap.add_argument("--skill-name", default="")
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--previous-feedback", type=Path, default=None,
                    help="Prefill textareas from a previous feedback.json")
    args = ap.parse_args()

    root = args.iteration_dir
    if not root.is_dir():
        sys.exit(f"Directory not found: {root}")

    runs = find_runs(root)
    if not runs:
        sys.exit("No runs found (expected eval-*/<config>/outputs/ directories)")

    previous: dict[str, str] = {}
    if args.previous_feedback and args.previous_feedback.exists():
        data = load_json(args.previous_feedback) or {}
        previous = {r.get("run_id", ""): r.get("feedback", "")
                    for r in data.get("reviews", []) if r.get("feedback", "").strip()}

    configs: dict[str, list] = {}
    for r in runs:
        configs.setdefault(r["config"], []).append(r)
    summary_rows = "".join(
        f'<tr><td>{esc(c)}</td><td>{len(rs)}</td>'
        f'<td>{sum(((x.get("grading") or {}).get("summary", {}).get("pass_rate", 0.0) for x in rs), 0.0) / len(rs):.0%}</td></tr>'
        for c, rs in configs.items()
    )

    body = []
    for eval_id in sorted({r["eval_id"] for r in runs}):
        group = [r for r in runs if r["eval_id"] == eval_id]
        body.append(f'<div class="eval"><h2>eval {esc(eval_id)}: {esc(group[0]["eval_name"])}</h2>'
                    f'<div class="prompt">{esc(group[0]["prompt"])}</div>')
        for r in group:
            body.append(render_run(r))
        body.append("</div>")

    prev_json = json.dumps(previous).replace("</", "<\\/")

    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Review: {esc(args.skill_name)}</title>
<style>{CSS}</style></head><body>
<header><h1>Skill review: {esc(args.skill_name)}</h1>
<div class="sub">{len(runs)} runs across {len(configs)} configuration(s) &middot;
leave feedback (empty = fine), then download feedback.json</div>
<table><tr><th>configuration</th><th>runs</th><th>mean pass rate</th></tr>{summary_rows}</table>
</header><main>{''.join(body)}
<button onclick="downloadFeedback()">Download feedback.json</button>
<span class="muted" id="count"></span></main>
<script>
const PREVIOUS = {prev_json};
const reviews = {{}};
document.querySelectorAll('textarea[data-run]').forEach(t => {{
  const pre = PREVIOUS[t.dataset.run];
  if (pre) {{ t.value = pre; reviews[t.dataset.run] = pre; }}
  t.addEventListener('input', () => {{ reviews[t.dataset.run] = t.value; }});
}});
function downloadFeedback() {{
  const out = {{reviews: Object.entries(reviews)
    .filter(([, v]) => v && v.trim())
    .map(([run_id, feedback]) => ({{run_id, feedback}}))}};
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)],
    {{type: 'application/json'}}));
  a.download = 'feedback.json';
  a.click();
}}
document.getElementById('count').textContent =
  '{len(runs)} runs, ' + document.querySelectorAll('.eval').length + ' evals';
</script></body></html>"""

    out = args.output or (root / "review.html")
    out.write_text(html)
    print(f"Wrote {out} ({len(runs)} runs)")


if __name__ == "__main__":
    main()
