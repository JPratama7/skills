# Worked examples — good vs bad decompositions

Use these to calibrate. Each example shows the task, a bad decomposition (and why), and a good one.

## Example 1: "Build a CRUD API for users from an OpenAPI spec"

### Bad — list disguised as graph

```json
{
  "task": "Build a CRUD API for users from an OpenAPI spec",
  "nodes": [
    { "id": "n1", "name": "read spec", "deps": [], "prompt": "Read openapi.yaml ..." },
    { "id": "n2", "name": "gen types", "deps": ["n1"], "prompt": "Generate TS types from the spec ..." },
    { "id": "n3", "name": "gen handlers", "deps": ["n2"], "prompt": "Generate route handlers ..." },
    { "id": "n4", "name": "wire routes", "deps": ["n3"], "prompt": "Wire handlers into Express ..." },
    { "id": "n5", "name": "add tests", "deps": ["n4"], "prompt": "Add tests ..." },
    { "id": "n6", "name": "run tests", "deps": ["n5"], "prompt": "Run the test suite ..." }
  ]
}
```

Why bad: every node depends on the previous. Zero parallelism. This is a todo list with extra JSON. Either the deps are fake (test author could start from the spec in parallel with handler gen) or the task genuinely is linear — in which case `honest_parallelism` should say so, not pretend.

### Good — real parallelism

Built with `scripts/graph.py` (each call is one node; the script validates as you go and computes the summary on export):

```bash
python scripts/graph.py init --task "Build a CRUD API for users from an OpenAPI spec" \
  --model cheap --skills ponytail

python scripts/graph.py add-node --id read-spec \
  --name "Extract user resource schema from openapi.yaml" \
  --prompt "Read openapi.yaml. Extract the /users paths, User schema, error response schemas. Write extracted.md with three sections — ## paths, ## userSchema, ## errorSchemas — each containing the verbatim YAML." \
  --verify "extracted.md exists, has ## paths, ## userSchema, ## errorSchemas headers, and each section contains YAML." \
  --outputs extracted.md

python scripts/graph.py add-node --id gen-types --model strong \
  --name "Generate TypeScript types from extracted schema" \
  --prompt "From the user schema in extracted.md (below), generate src/types/user.ts: User interface + CreateUser/UpdateUser partial variants. Use the project's TS config (strict).\n\n<paste extracted.md userSchema section>" \
  --verify "tsc --noEmit src/types/user.ts passes; file exports User, CreateUser, UpdateUser." \
  --deps read-spec --inputs read-spec:extracted.md --outputs src/types/user.ts

python scripts/graph.py add-node --id gen-handlers --model strong \
  --name "Generate Express route handlers for /users CRUD" \
  --prompt "Generate src/routes/users.ts: Express router with GET/POST/PUT/DELETE on /users, in-memory Map<string,User> store, import User from ../types/user. Match the spec paths:\n\n<paste extracted.md paths section>" \
  --verify "File exists, exports a router, registers all 4 verbs on /users, imports from ../types/user." \
  --deps read-spec --inputs read-spec:extracted.md --outputs src/routes/users.ts

python scripts/graph.py add-node --id wire-routes \
  --name "Wire users router into the Express app" \
  --prompt "In src/app.ts (or src/index.ts), import the users router from ./routes/users and mount at /users. Don't touch other routes." \
  --verify "git diff src/app.ts shows only an import and an app.use('/users', usersRouter)." \
  --deps gen-handlers --inputs gen-handlers:src/routes/users.ts --outputs app-diff

python scripts/graph.py add-node --id gen-tests --skills tdd \
  --name "Write integration tests for /users CRUD" \
  --prompt "Write test/users.test.ts with supertest against the Express app. Cover: list empty, create+list, create+get one, update, delete, get-after-delete 404. Import app from src/app." \
  --verify "File exists, has >=6 test cases, uses supertest." \
  --deps wire-routes --inputs wire-routes:app-diff --outputs test/users.test.ts

python scripts/graph.py add-node --id run-tests \
  --name "Run the test suite and report" \
  --prompt "Run npm test. Report pass/fail counts + any failure output verbatim." \
  --verify "Output contains 'passing' and a number; if 'failing' > 0, verify fails." \
  --deps gen-tests,gen-types --inputs gen-tests:test/users.test.ts,gen-types:src/types/user.ts \
  --outputs test-report

python scripts/graph.py validate
python scripts/graph.py export --json plan.json --mermaid plan.mmd
```

The exported `plan.json` (produced by the script — not hand-written):

```json
{
  "task": "Build a CRUD API for users from an OpenAPI spec",
  "granularity": "single-subagent-call",
  "model": "cheap",
  "skills": ["ponytail"],
  "nodes": [
    { "id": "read-spec", "name": "Extract user resource schema from openapi.yaml",
      "prompt": "Read openapi.yaml. Extract the /users paths, User schema, error response schemas. Write extracted.md with three sections — ## paths, ## userSchema, ## errorSchemas — each containing the verbatim YAML.",
      "deps": [], "inputs": [], "outputs": ["extracted.md"],
      "verify": "extracted.md exists, has ## paths, ## userSchema, ## errorSchemas headers, and each section contains YAML." },
    { "id": "gen-types", "model": "strong", "name": "Generate TypeScript types from extracted schema",
      "prompt": "From the user schema in extracted.md (below), generate src/types/user.ts: User interface + CreateUser/UpdateUser partial variants. Use the project's TS config (strict).\n\n<paste extracted.md userSchema section>",
      "deps": ["read-spec"], "inputs": ["read-spec:extracted.md"], "outputs": ["src/types/user.ts"],
      "verify": "tsc --noEmit src/types/user.ts passes; file exports User, CreateUser, UpdateUser." },
    { "id": "gen-handlers", "model": "strong", "name": "Generate Express route handlers for /users CRUD",
      "prompt": "Generate src/routes/users.ts: Express router with GET/POST/PUT/DELETE on /users, in-memory Map<string,User> store, import User from ../types/user. Match the spec paths:\n\n<paste extracted.md paths section>",
      "deps": ["read-spec"], "inputs": ["read-spec:extracted.md"], "outputs": ["src/routes/users.ts"],
      "verify": "File exists, exports a router, registers all 4 verbs on /users, imports from ../types/user." },
    { "id": "wire-routes", "name": "Wire users router into the Express app",
      "prompt": "In src/app.ts (or src/index.ts), import the users router from ./routes/users and mount at /users. Don't touch other routes.",
      "deps": ["gen-handlers"], "inputs": ["gen-handlers:src/routes/users.ts"], "outputs": ["app-diff"],
      "verify": "git diff src/app.ts shows only an import and an app.use('/users', usersRouter)." },
    { "id": "gen-tests", "skills": ["tdd"], "name": "Write integration tests for /users CRUD",
      "prompt": "Write test/users.test.ts with supertest against the Express app. Cover: list empty, create+list, create+get one, update, delete, get-after-delete 404. Import app from src/app.",
      "deps": ["wire-routes"], "inputs": ["wire-routes:app-diff"], "outputs": ["test/users.test.ts"],
      "verify": "File exists, has >=6 test cases, uses supertest." },
    { "id": "run-tests", "name": "Run the test suite and report",
      "prompt": "Run npm test. Report pass/fail counts + any failure output verbatim.",
      "deps": ["gen-tests", "gen-types"], "inputs": ["gen-tests:test/users.test.ts", "gen-types:src/types/user.ts"],
      "outputs": ["test-report"], "verify": "Output contains 'passing' and a number; if 'failing' > 0, verify fails." }
  ],
  "summary": {
    "node_count": 6, "wave_count": 5,
    "critical_path": ["read-spec", "gen-handlers", "wire-routes", "gen-tests", "run-tests"],
    "bottlenecks": [],
    "honest_parallelism": "wave 0 has 1 node(s); critical path is 5 wave(s) vs 6 linear."
  }
}
```

Why good: `gen-types` and `gen-handlers` actually run in parallel (both depend only on `read-spec`). `run-tests` correctly declares both `gen-tests` AND `gen-types` as deps (needs the test file and the types it imports). `honest_parallelism` admits the gain is modest — one wave saved over linear. `read-spec` is a fan-in point (everything depends on it) but not a `bottlenecks` entry because the threshold is >8 direct dependents; the script reserves that label for genuine gridlock.

Model config demo: the user said "cheap model for the mechanical nodes, strong for the codegen ones". Top-level `--model cheap` covers `read-spec`, `wire-routes`, `gen-tests`, and `run-tests`; `gen-types` and `gen-handlers` override with `--model strong`. Node wins over top-level; unmentioned plans get no `model` field at all and run on the harness default.

Skill config demo: the user said "preload ponytail everywhere, and tdd for the test node". Top-level `--skills ponytail` applies to every node; `gen-tests` overrides with `--skills tdd` (override replaces, not merges — the user asked for tdd there, not ponytail + tdd). Plans without a skill mention carry no `skills` field and nodes run without skill instructions.

## Example 2: "Refactor this 800-line function into smaller functions"

### Bad — over-split

Splitting into 30 nodes, one per extracted function. Each node is a one-line "extract function X" that immediately gets consumed by the next. That's a list, and the nodes are too fine — none is a meaningful subagent call.

### Good — split by concern, not by function

3 nodes:

1. `map-concerns` — read the function, output a list of concern groups (each a set of lines + proposed function name). Verify: output is a JSON list with line ranges and names.
2. `extract-group-a` / `extract-group-b` / `extract-group-c` (parallel, all depend on `map-concerns`) — each takes one concern group, extracts it into a named function, replaces the original lines with a call. Verify: function exists, original lines replaced, file still parses.
3. `verify-whole` — run the project's tests + lint on the refactored file. Depends on all three extract nodes.

The 3 extract nodes run in parallel because they touch different line ranges and don't conflict. The dependency on `map-concerns` is real (they need the line ranges), not sequencing bias.

## Example 3: "Research and write a comparison of Postgres vs MySQL for our workload"

### Bad — fake parallelism

`research-postgres` and `research-mysql` in parallel, then `write-comparison` depending on both. Looks parallel, but the two research nodes will overlap heavily (both cover indexing, both cover replication). The "parallelism" duplicates work.

### Good — parallel by non-overlapping dimension

Split the comparison dimensions instead of the products:

1. `dim-indexing` — indexing & query planning, both products.
2. `dim-replication` — replication & failover, both products.
3. `dim-extensibility` — extensions, custom types, PL/langs, both products.
4. `synthesis` — depends on 1-3, writes the comparison using our workload profile.

Three research nodes run in parallel with no overlap. Synthesis fans in. Real parallelism, no duplicated work.

## Calibration takeaways

- Parallelism is real only when the nodes do **non-overlapping** work. Two nodes covering the same ground from different angles is not parallelism, it's duplication.
- A linear chain is fine if the task is genuinely sequential — just say so in `honest_parallelism`. Don't manufacture fake parallelism to justify the skill.
- When a single node feeds many, ask whether those many could instead be split by a different axis so they share fewer upstream deps. The bottleneck is often a sign the decomposition axis is wrong.
- Verify checks should be cheap and objective. If you can't write a `verify`, the node's output isn't concrete enough — refine the node.
