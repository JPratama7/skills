#!/usr/bin/env python3
"""graph-decompose plan builder.

Replaces hand-written JSON with incremental SQLite-backed node insertion.
Each add-node call validates the new node against existing nodes; export
runs full validation and emits JSON + Mermaid with a computed summary.

The LLM never writes JSON. It calls this script per node, then exports.
"""
import argparse
import json
import os
import re
import sqlite3
import sys

DEFAULT_DB = "plan.db"

BANNED_PROMPT_PHRASES = [
    "see above", "as discussed", "per the task", "previously",
    "you are a", "please", "your task is",
]
VAGUE_VERIFY_WORDS = ["review", "looks good", "ensure quality", "looks reasonable"]


def die(msg, code=1):
    print(f"graph.py: {msg}", file=sys.stderr)
    sys.exit(code)


# ---------- DB ----------

def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            prompt TEXT NOT NULL,
            verify TEXT NOT NULL,
            model TEXT,
            skills TEXT
        );
        CREATE TABLE IF NOT EXISTS deps (
            node_id TEXT, dep_id TEXT, PRIMARY KEY(node_id, dep_id)
        );
        CREATE TABLE IF NOT EXISTS inputs (
            node_id TEXT, dep_id TEXT, artifact TEXT
        );
        CREATE TABLE IF NOT EXISTS outputs (
            node_id TEXT, artifact TEXT
        );
        """
    )
    return conn


def set_meta(conn, k, v):
    conn.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, v))


def get_meta(conn, k, default=None):
    row = conn.execute("SELECT value FROM meta WHERE key=?", (k,)).fetchone()
    return row[0] if row else default


# ---------- commands ----------

def cmd_init(args):
    if not args.task:
        die("init requires --task")
    conn = connect(args.db)
    set_meta(conn, "task", args.task)
    set_meta(conn, "granularity", args.granularity)
    if args.model:
        set_meta(conn, "model", args.model)
    if args.skills:
        set_meta(conn, "skills", ",".join(args.skills))
    conn.commit()
    extras = []
    if args.model:
        extras.append(f"model={args.model!r}")
    if args.skills:
        extras.append(f"skills={','.join(args.skills)!r}")
    print(f"meta set: task={args.task!r} granularity={args.granularity}"
          + (f" {' '.join(extras)}" if extras else ""))


def cmd_add_node(args):
    conn = connect(args.db)
    for d in args.deps:
        if not conn.execute("SELECT 1 FROM nodes WHERE id=?", (d,)).fetchone():
            die(f"dep {d!r} does not exist yet — add it first")
    try:
        conn.execute(
            "INSERT INTO nodes(id,name,prompt,verify,model,skills) VALUES(?,?,?,?,?,?)",
            (
                args.id,
                args.name,
                args.prompt,
                args.verify,
                args.model,
                ",".join(args.skills) if args.skills else None,
            ),
        )
    except sqlite3.IntegrityError:
        die(f"duplicate id {args.id!r}")
    for d in args.deps:
        conn.execute(
            "INSERT OR IGNORE INTO deps(node_id,dep_id) VALUES(?,?)", (args.id, d)
        )
    for inp in args.inputs:
        if ":" not in inp:
            die(f"input {inp!r} must be 'dep_id:artifact'")
        dep_id, artifact = inp.split(":", 1)
        if dep_id not in args.deps:
            die(f"input {inp!r} names dep {dep_id!r} not in --deps")
        conn.execute(
            "INSERT INTO inputs(node_id,dep_id,artifact) VALUES(?,?,?)",
            (args.id, dep_id, artifact),
        )
    for out in args.outputs:
        conn.execute(
            "INSERT INTO outputs(node_id,artifact) VALUES(?,?)", (args.id, out)
        )
    conn.commit()
    print(f"added {args.id} ({args.name})")


def cmd_validate(args):
    conn = connect(args.db)
    nodes = load_graph(conn)
    violations = validate_all(conn, nodes)
    if not violations:
        print(f"OK — {len(nodes)} node(s), no violations")
        return
    for rule, msg in violations:
        print(f"[{rule}] {msg}", file=sys.stderr)
    sys.exit(1)


def cmd_export(args):
    conn = connect(args.db)
    task = get_meta(conn, "task")
    if not task:
        die("task is not set — run `init --task '...'` first")
    nodes = load_graph(conn)
    violations = validate_all(conn, nodes)
    if violations:
        for rule, msg in violations:
            print(f"[{rule}] {msg}", file=sys.stderr)
        die("plan has validation errors — fix before exporting")
    plan = build_plan(conn, nodes)
    with open(args.json, "w") as f:
        json.dump(plan, f, indent=2)
        f.write("\n")
    mermaid = build_mermaid(nodes)
    mmd_path = args.mermaid
    if not mmd_path and args.json.endswith(".json"):
        mmd_path = args.json[: -len(".json")] + ".mmd"
    if mmd_path:
        with open(mmd_path, "w") as f:
            f.write(mermaid)
    print(f"exported {len(nodes)} nodes -> {args.json}" + (f" + {mmd_path}" if mmd_path else ""))


def cmd_show(args):
    """Print current plan as JSON to stdout (no file write, no validation gate)."""
    conn = connect(args.db)
    nodes = load_graph(conn)
    plan = build_plan(conn, nodes)
    print(json.dumps(plan, indent=2))


# ---------- graph load / validation / summary ----------

def load_graph(conn):
    nodes = {}
    for r in conn.execute(
        "SELECT id,name,prompt,verify,model,skills FROM nodes ORDER BY rowid"
    ):
        nid, name, prompt, verify, model, skills = r
        nodes[nid] = {
            "id": nid,
            "name": name,
            "prompt": prompt,
            "verify": verify,
            "model": model,
            "skills": skills.split(",") if skills else None,
            "deps": [],
            "inputs": [],
            "outputs": [],
        }
    for r in conn.execute("SELECT node_id,dep_id FROM deps ORDER BY dep_id"):
        nodes[r[0]]["deps"].append(r[1])
    for r in conn.execute("SELECT node_id,dep_id,artifact FROM inputs"):
        nodes[r[0]]["inputs"].append(f"{r[1]}:{r[2]}")
    for r in conn.execute("SELECT node_id,artifact FROM outputs"):
        nodes[r[0]]["outputs"].append(r[1])
    return nodes


def validate_all(conn, nodes):
    """Return list of (rule_name, message) violations. Empty = valid."""
    v = []

    # 2. DAG — cycle detection
    cycle = find_cycle(nodes)
    if cycle:
        v.append(("DAG", f"cycle: {' -> '.join(cycle)}"))

    # 3. dangling refs
    for nid, n in nodes.items():
        for d in n["deps"]:
            if d not in nodes:
                v.append(("dangling-ref", f"{nid} depends on missing {d}"))

    # 4. input/dep alignment
    for nid, n in nodes.items():
        dep_set = set(n["deps"])
        in_deps = {inp.split(":", 1)[0] for inp in n["inputs"]}
        missing = dep_set - in_deps
        if missing:
            v.append(("input-dep-mismatch", f"{nid} has deps with no inputs: {sorted(missing)}"))
        extra = in_deps - dep_set
        if extra:
            v.append(("input-dep-mismatch", f"{nid} has inputs for non-deps: {sorted(extra)}"))

    # 5. output reachability — every output consumed or terminal
    consumed = set()
    for n in nodes.values():
        for inp in n["inputs"]:
            consumed.add(inp.split(":", 1)[1])
    for nid, n in nodes.items():
        for out in n["outputs"]:
            if out not in consumed and not is_terminal_output(nodes, nid, out):
                v.append(("dead-output", f"{nid} output {out!r} never consumed and not terminal"))

    # 6. terse self-contained prompts
    for nid, n in nodes.items():
        low = n["prompt"].lower()
        for phrase in BANNED_PROMPT_PHRASES:
            if phrase in low:
                v.append(("prompt-style", f"{nid} prompt contains {phrase!r}"))

    # 7. verify objectivity
    for nid, n in nodes.items():
        low = n["verify"].lower()
        for word in VAGUE_VERIFY_WORDS:
            if word in low:
                v.append(("vague-verify", f"{nid} verify contains {word!r}"))

    # 8. no dead nodes — every node has a downstream consumer or terminal output
    dependents = {nid: 0 for nid in nodes}
    for n in nodes.values():
        for d in n["deps"]:
            dependents[d] = dependents.get(d, 0) + 1
    for nid, n in nodes.items():
        if dependents[nid] == 0 and not any(is_terminal_output(nodes, nid, o) for o in n["outputs"]):
            v.append(("dead-node", f"{nid} has no consumers and no terminal output"))

    # 10. model sanity
    top_model = get_meta(conn, "model")
    if top_model is not None and not top_model.strip():
        v.append(("model-sanity", "top-level model is empty"))
    for nid, n in nodes.items():
        if n["model"] is not None and not n["model"].strip():
            v.append(("model-sanity", f"{nid} model is empty"))

    # 11. skills sanity
    top_skills = get_meta(conn, "skills")
    if top_skills is not None:
        for s in top_skills.split(","):
            if not s.strip():
                v.append(("skills-sanity", "top-level skills has empty entry"))
    for nid, n in nodes.items():
        if n["skills"]:
            for s in n["skills"]:
                if not s.strip():
                    v.append(("skills-sanity", f"{nid} skills has empty entry"))

    return v


def is_terminal_output(nodes, nid, out):
    """A terminal output is one that the graph is meant to produce as final
    product. We can't know intent, so treat the last-wave nodes' outputs as
    terminal — i.e. nodes with no dependents."""
    dependents = 0
    for n in nodes.values():
        if nid in n["deps"]:
            dependents += 1
    return dependents == 0


def find_cycle(nodes):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {nid: WHITE for nid in nodes}
    stack = []

    def dfs(u):
        color[u] = GRAY
        stack.append(u)
        for d in nodes[u]["deps"]:
            if d not in color:
                continue
            if color[d] == GRAY:
                idx = stack.index(d)
                return stack[idx:] + [d]
            if color[d] == WHITE:
                found = dfs(d)
                if found:
                    return found
        stack.pop()
        color[u] = BLACK
        return None

    for nid in nodes:
        if color[nid] == WHITE:
            found = dfs(nid)
            if found:
                return found
    return None


def longest_path(nodes):
    """Return the longest dep chain (list of ids, dep-first)."""
    memo = {}

    def lp(nid, seen):
        if nid in memo:
            return memo[nid]
        if nid in seen:
            return ([], 0)  # safety against cycles
        deps = nodes[nid]["deps"]
        if not deps:
            memo[nid] = ([nid], 1)
            return memo[nid]
        best = []
        for d in deps:
            path, length = lp(d, seen | {nid})
            if length > len(best):
                best = path
        memo[nid] = (best + [nid], len(best) + 1)
        return memo[nid]

    best_overall = []
    for nid in nodes:
        path, _ = lp(nid, set())
        if len(path) > len(best_overall):
            best_overall = path
    return best_overall


def articulation_points(nodes):
    """Nodes whose removal disconnects the undirected version of the graph."""
    adj = {nid: set() for nid in nodes}
    for nid, n in nodes.items():
        for d in n["deps"]:
            adj[nid].add(d)
            adj[d].add(nid)
    visited, disc, low = set(), {}, {}
    aps = set()
    timer = [0]

    def dfs(u, parent):
        visited.add(u)
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0
        for v in adj[u]:
            if v not in visited:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if parent is None and children > 1:
                    aps.add(u)
                if parent is not None and low[v] >= disc[u]:
                    aps.add(u)
            elif v != parent:
                low[u] = min(low[u], disc[v])

    for nid in nodes:
        if nid not in visited:
            dfs(nid, None)
    return aps


def compute_summary(nodes):
    crit = longest_path(nodes)
    wave0 = [nid for nid, n in nodes.items() if not n["deps"]]
    dependents = {nid: 0 for nid in nodes}
    for n in nodes.values():
        for d in n["deps"]:
            dependents[d] += 1
    bottlenecks = sorted([nid for nid, c in dependents.items() if c > 8])
    aps = articulation_points(nodes)
    for ap in aps:
        if ap not in bottlenecks:
            bottlenecks.append(ap)
    bottlenecks.sort()
    if len(crit) == len(nodes) and len(nodes) > 1:
        honest = "Linear chain — no real parallelism gained."
    elif len(nodes) <= 1:
        honest = "Single node — no parallelism applicable."
    else:
        honest = (
            f"wave 0 has {len(wave0)} node(s); "
            f"critical path is {len(crit)} wave(s) vs {len(nodes)} linear."
        )
    return {
        "node_count": len(nodes),
        "wave_count": len(crit),
        "critical_path": crit,
        "bottlenecks": bottlenecks,
        "honest_parallelism": honest,
    }


def build_plan(conn, nodes):
    task = get_meta(conn, "task", "")
    granularity = get_meta(conn, "granularity", "single-subagent-call")
    top_model = get_meta(conn, "model")
    top_skills = get_meta(conn, "skills")
    plan = {"task": task, "granularity": granularity, "nodes": []}
    if top_model is not None:
        plan["model"] = top_model
    if top_skills is not None:
        plan["skills"] = top_skills.split(",")
    for nid in nodes:
        n = nodes[nid]
        node = {
            "id": n["id"],
            "name": n["name"],
            "prompt": n["prompt"],
            "deps": sorted(n["deps"]),
            "inputs": n["inputs"],
            "outputs": n["outputs"],
            "verify": n["verify"],
        }
        if n["model"] is not None:
            node["model"] = n["model"]
        if n["skills"]:
            node["skills"] = n["skills"]
        plan["nodes"].append(node)
    plan["summary"] = compute_summary(nodes)
    return plan


def build_mermaid(nodes):
    lines = ["graph LR"]
    for nid in nodes:
        n = nodes[nid]
        safe_name = n["name"].replace('"', "'")
        lines.append(f'  {nid}["{safe_name}"]')
    for nid in nodes:
        for d in sorted(nodes[nid]["deps"]):
            lines.append(f"  {d} --> {nid}")
    wave0 = [nid for nid, n in nodes.items() if not n["deps"]]
    if wave0:
        lines.append("classDef ready fill:#cfe,stroke:#080;")
        lines.append(f"class {','.join(sorted(wave0))} ready;")
    return "\n".join(lines) + "\n"


# ---------- arg parsing ----------

def split_csv(v):
    return [x for x in v.split(",") if x] if v else []


def main():
    p = argparse.ArgumentParser(prog="graph.py", description=__doc__)
    p.add_argument("--db", default=DEFAULT_DB, help=f"SQLite path (default: {DEFAULT_DB})")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init", help="set plan metadata (task required)")
    pi.add_argument("--task", required=True)
    pi.add_argument("--granularity", default="single-subagent-call")
    pi.add_argument("--model")
    pi.add_argument("--skills", help="comma-separated")
    pi.set_defaults(func=cmd_init)

    pa = sub.add_parser("add-node", help="append a node to the plan")
    pa.add_argument("--id", required=True)
    pa.add_argument("--name", required=True)
    pa.add_argument("--prompt", required=True)
    pa.add_argument("--verify", required=True)
    pa.add_argument("--deps", default="", help="comma-separated dep ids")
    pa.add_argument("--inputs", default="", help="comma-separated dep_id:artifact")
    pa.add_argument("--outputs", default="", help="comma-separated artifact names")
    pa.add_argument("--model")
    pa.add_argument("--skills", help="comma-separated")
    pa.set_defaults(func=cmd_add_node)

    pv = sub.add_parser("validate", help="run all validation rules")
    pv.set_defaults(func=cmd_validate)

    pe = sub.add_parser("export", help="validate + write JSON and Mermaid")
    pe.add_argument("--json", required=True, help="output JSON path")
    pe.add_argument("--mermaid", help="output Mermaid path (default: sibling .mmd)")
    pe.set_defaults(func=cmd_export)

    ps = sub.add_parser("show", help="print current plan as JSON to stdout")
    ps.set_defaults(func=cmd_show)

    args = p.parse_args()
    # normalize csv lists
    if hasattr(args, "deps") and isinstance(args.deps, str):
        args.deps = split_csv(args.deps)
    if hasattr(args, "inputs") and isinstance(args.inputs, str):
        args.inputs = split_csv(args.inputs)
    if hasattr(args, "outputs") and isinstance(args.outputs, str):
        args.outputs = split_csv(args.outputs)
    if hasattr(args, "skills") and isinstance(args.skills, str):
        args.skills = split_csv(args.skills)
    args.func(args)


if __name__ == "__main__":
    main()
