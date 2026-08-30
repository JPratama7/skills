# Handoff examples

Four directions + trivial case. Each shows the format, then explains the choices.

## 1. Subagent → parent (most common)

**Scenario:** A research subagent finished investigating caching libraries and needs to report back to the parent agent that will pick a winner.

---

Picked Redis as the cache layer. Tested four options against the load profile in `perf-baseline.md`; Redis hit p99 < 10ms on all 3 query patterns where the others fell over. Full results in `cache-eval/results.json`. One open question on persistence — see below.

## State
- Done: bench suite + write-up (`docs/cache-decision.md`)
- Files: `cache-eval/results.json` — raw benchmark numbers; `docs/cache-decision.md` — recommendation memo
- Decisions: Redis over Memcached — Memcached can't do persistence and ops requires restart-recovery; over KeyDB — single-team maintenance burden; over in-process (lru-cache) — doesn't survive deploys

## Open
- Question: ops wants persistence but also a 24h TTL on stale keys. Do we run two Redis instances (one persistent, one ephemeral) or use a single instance with maxmemory-policy=allkeys-lru?

## Context
- Goal: pick a cache that survives a single-node failure and handles 5k req/s sustained
- Constraints: must be OSS, must run on existing k8s, no new infra team

---

**Why this works:** prose leads with the verdict (Redis) and the reason (perf). Tail has only what the parent needs to verify or extend. Open question is one specific decision, not a vague "need to discuss persistence."

## 2. Parent → subagent (delegation brief)

**Scenario:** Parent is delegating "implement rate limiting on the /api/posts endpoint" to a fresh subagent.

---

Implement token-bucket rate limiting on `POST /api/posts` per the spec in `docs/rate-limit-spec.md`. Endpoint currently has no throttling; spec calls for 10 req/min per user, 429 with Retry-After on overflow. Match the existing middleware pattern in `src/middleware/auth.ts`.

## State
- Done: spec written, infra decision (use redis token buckets, see Decision)
- Pending: implementation, tests, integration with auth middleware
- Files: `docs/rate-limit-spec.md` — full requirements; `src/middleware/auth.ts` — pattern to follow; `src/redis.ts` — existing client wrapper

## Decisions
- Redis over in-process counters — multiple app instances, in-process can't enforce global limit
- Token bucket over fixed window — burst handling per spec §3

## Constraints
- Do NOT touch `src/middleware/auth.ts` itself — extend with a new file, not edits to auth
- Use `ioredis`, not `redis` package — already a project dep
- Match existing error response shape: `{error: string, code: string}`

## Context
- Goal: protect DB from write-storms on /api/posts (saw 3 incidents last month)
- Assumptions: spec is final; user identity comes from auth middleware's `req.user.id`

---

**Why this works:** prose says exactly what to do and where to look. Constraints come BEFORE context because they're the hard rules the subagent must not violate. Open section is omitted because nothing is blocked.

## 3. Peer → peer (chained)

**Scenario:** Agent A finished the data layer; Agent B is now picking up the API layer with the same overall goal.

---

Data layer is done and the schema is live in staging. API layer picks up from `src/models/` — types are exported, migrations are applied. Two things to know: timestamps are stored as ISO strings not Date objects (see Decision), and the soft-delete pattern is required by the spec (every model has `deletedAt`).

## State
- Done: schema, migrations, seed data, base model classes
- Files: `src/models/index.ts` — barrel exports; `prisma/schema.prisma` — source of truth; `src/lib/soft-delete.ts` — helper for the soft-delete pattern
- Decisions: ISO strings over Date objects — JSON serialization loses Date fidelity and we hit this in v1; soft delete over hard delete — legal hold requirement

## Constraints
- All API responses must serialize datetimes as ISO 8601 strings
- Never `DELETE` a row — use `softDelete()` from the helper
- New models must follow `BaseModel` shape (id, createdAt, updatedAt, deletedAt)

---

**Why this works:** state and constraints are the bulk — this is mostly a "here are the rules you must follow" handoff. Prose gives the 30-second read; the constraints prevent the most common mistakes.

## 4. Session → future session

**Scenario:** End of a long session, picking back up tomorrow.

---

Stopped at the OAuth refresh-token bug — see Open. Got sidetracked into the audit log refactor after that and didn't finish; current state has the audit log half-converted.

## State
- Done: rate limiting (deployed), OAuth login flow, audit log schema
- In progress: audit log refactor (commit `a3f8e2` was last clean state)
- Pending: OAuth refresh bug fix, finish audit log refactor, write runbook for token rotation
- Files: `src/auth/oauth.ts` — has the buggy refresh logic; `docs/audit-log-plan.md` — what was planned

## Open
- Blocker: refresh tokens are expiring faster than expected — issue is either in the expiry calculation or the rotation cadence; need to read the IdP docs again
- Risk: audit log refactor is half-done; if you commit other changes on top without finishing, migrations will diverge

## Context
- Goal: complete the OAuth + audit log work, then move to the rate-limit-v2 design doc
- Assumptions: IdP is Auth0 (not changing); audit log will go to the same Postgres DB

---

**Why this works:** prose states exactly where to pick up. The "Risk" entry is the important one — it warns the future agent about a divergence trap. Constraints section is omitted because none are non-obvious.

## 5. Trivial case (skip the structure)

**Scenario:** Subagent ran a single shell command and the answer is one line.

---

Done. Build is green, no warnings.

That's it. Don't reach for headers when the prose carries everything. The format exists to organize complexity, not to dress up simplicity.