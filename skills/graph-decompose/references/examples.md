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

```json
{
  "task": "Build a CRUD API for users from an OpenAPI spec",
  "nodes": [
    {
      "id": "read-spec",
      "name": "Extract user resource schema from openapi.yaml",
      "prompt": "Read openapi.yaml and extract: the /users paths, the User schema, and the error response schemas. Output a single file `extracted.md` with three sections (paths, userSchema, errorSchemas) containing the verbatim YAML for each.",
      "deps": [],
      "inputs": [],
      "outputs": ["extracted.md"],
      "verify": "extracted.md exists, has '## paths', '## userSchema', '## errorSchemas' headers, and each section contains YAML."
    },
    {
      "id": "gen-types",
      "name": "Generate TypeScript types from extracted schema",
      "prompt": "From the user schema in extracted.md (below), generate `src/types/user.ts` with a User interface and CreateUser/UpdateUser partial variants. Use the existing project's TS config (strict mode).\n\n<paste extracted.md userSchema section>",
      "deps": ["read-spec"],
      "inputs": ["read-spec:extracted.md"],
      "outputs": ["src/types/user.ts"],
      "verify": "tsc --noEmit src/types/user.ts passes; file exports User, CreateUser, UpdateUser."
    },
    {
      "id": "gen-handlers",
      "name": "Generate Express route handlers for /users CRUD",
      "prompt": "Generate `src/routes/users.ts` with Express router implementing GET/POST/PUT/DELETE for /users. Use an in-memory Map<string, User> as the store. Import User types from ../types/user. Match the paths in the spec:\n\n<paste extracted.md paths section>",
      "deps": ["read-spec"],
      "inputs": ["read-spec:extracted.md"],
      "outputs": ["src/routes/users.ts"],
      "verify": "File exists, exports a router, registers all 4 verbs on /users, imports from ../types/user."
    },
    {
      "id": "wire-routes",
      "name": "Wire users router into the Express app",
      "prompt": "In src/app.ts (or src/index.ts), import the users router from ./routes/users and mount it at /users. Don't touch other routes.",
      "deps": ["gen-handlers"],
      "inputs": ["gen-handlers:src/routes/users.ts"],
      "outputs": ["app-diff"],
      "verify": "git diff src/app.ts shows only an import and an app.use('/users', usersRouter)."
    },
    {
      "id": "gen-tests",
      "name": "Write integration tests for /users CRUD",
      "prompt": "Write `test/users.test.ts` using supertest against the Express app. Cover: list empty, create + list, create + get one, update, delete, get-after-delete 404. Import the app from src/app.",
      "deps": ["wire-routes"],
      "inputs": ["wire-routes:app-diff"],
      "outputs": ["test/users.test.ts"],
      "verify": "File exists, has ≥6 test cases, uses supertest."
    },
    {
      "id": "run-tests",
      "name": "Run the test suite and report",
      "prompt": "Run `npm test` and report pass/fail counts plus any failure output verbatim.",
      "deps": ["gen-tests", "gen-types"],
      "inputs": ["gen-tests:test/users.test.ts", "gen-types:src/types/user.ts"],
      "outputs": ["test-report"],
      "verify": "Output contains 'passing' and a number; if 'failing' > 0, verify fails."
    }
  ],
  "summary": {
    "node_count": 6,
    "wave_count": 4,
    "critical_path": ["read-spec", "gen-handlers", "wire-routes", "gen-tests", "run-tests"],
    "bottlenecks": ["read-spec"],
    "honest_parallelism": "gen-types and gen-handlers run in parallel after read-spec (wave 1 has 2 nodes). Critical path is 5 waves; the parallel branch saves 1 wave vs linear. read-spec is the bottleneck — everything depends on it."
  }
}
```

Why good: `gen-types` and `gen-handlers` actually run in parallel (both depend only on `read-spec`). `run-tests` correctly declares both `gen-tests` AND `gen-types` as deps (needs the test file and the types it imports). `honest_parallelism` admits the gain is modest and names the bottleneck.

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
