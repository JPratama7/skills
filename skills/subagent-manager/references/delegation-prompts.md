# Delegation prompt examples

Three worked briefs covering the common delegation shapes. Each follows the
template from `SKILL.md`: Task → Start here → Context → Constraints → Scope →
Output contract → Defaults. Note how much context each one carries — that's
the point. The subagent sees *only* this text.

## Example 1: explore agent (read-only)

> **Task:** Locate where webhook retry logic is implemented and how it's
> configured.
>
> **Start here:** `src/webhooks/dispatcher.ts` — likely entry point.
>
> **Context:** We're seeing duplicate deliveries after a provider timeout and
> suspect the retry path ignores the provider's 409 response. I need a map of
> the retry flow before deciding whether to fix it or replace it. The codebase
> is a Node monorepo; webhook code lives under `src/webhooks/`, shared HTTP
> helpers under `src/lib/http/`.
>
> **Constraints:**
> - Critical: read-only — do NOT modify files
> - Required: trace the actual code path, not just filenames; note where the
>   retry count and backoff are configured
>
> **Scope:** investigate only. Owns nothing.
>
> **Output contract:** Return (1) the file:line range of the retry loop,
> (2) where retry config comes from, (3) whether 409 responses halt retries —
> with the code evidence, (4) a 2-sentence summary. Telegraphic: findings
> only, no filler. Under 300 words.
>
> **Defaults:** If multiple retry paths exist, report the one handling
> outbound delivery; note the others in one line each.

Why it works: the agent knows the *hypothesis* (409 ignored) so it reads with
purpose, knows it's read-only, and knows the exact shape of the answer.

## Example 2: build agent (write-capable)

> **Task:** Add a `DELETE /sessions/:id` endpoint that revokes a session.
>
> **Start here:** `src/routes/sessions.ts` — siblings show the route pattern.
>
> **Context:** Users need to log out other devices. Sessions live in Redis
> (`session:<id>` keys); the session middleware is in
> `src/middleware/session.ts`. We chose Redis DEL over a revocation list
> because sessions already expire — simpler, no new state.
>
> **Constraints:**
> - Critical: auth required — reuse the `@requireAuth` decorator from sibling
>   routes; do NOT write a new auth check
> - Critical: a user may only delete their own sessions
> - Required: return 204 on success, 404 if the session doesn't exist or
>   belongs to another user; add tests for happy path + 404 + 401
>
> **Scope:** you may create/edit files under `src/routes/`, `src/services/`,
> and `tests/`. Do not touch `src/middleware/session.ts`.
>
> **Output contract:** List files changed, paste the test output showing
> pass/fail counts, and flag anything you assumed that isn't in this brief.
>
> **Defaults:** If `requireAuth` doesn't expose the current user id, use
> `req.session.userId` — grep `src/routes/` for precedent first.

Why it works: Critical vs Required tells the agent what it can't break vs.
what it must deliver. The ownership boundary prevents it from stomping on
files another agent (or the parent) is editing. The default answers the most
likely blocker.

## Example 3: review agent (verifies a diff)

> **Task:** Review the uncommitted changes in this repo for correctness
> against the ticket below.
>
> **Start here:** `git diff` in `/repo`, then the ticket at `.local/ticket.md`.
>
> **Context:** The diff implements rate limiting on the login endpoint
> (ticket: max 5 attempts per IP per 10 minutes, then 429). A previous review
> found the counter wasn't reset on successful login — that fix is in this
> diff and needs re-checking.
>
> **Constraints:**
> - Critical: read-only — report findings, don't fix them
> - Required: check the reset-on-success path explicitly; check that the 429
>   response matches the API error shape in `src/lib/errors.ts`
>
> **Scope:** investigate only.
>
> **Output contract:** One line per finding — `file:line, problem, suggested
> fix` — or "No findings" plus one line on what you verified. Max 10 findings,
> ordered by severity.
>
> **Defaults:** If the diff is empty, report that and stop — don't review the
> whole repo.

Why it works: the agent knows what a previous reviewer already caught (so it
doesn't relitigate), has an explicit checklist item for the regression risk,
and has a hard output format that makes the result trivially scannable.

## The pattern across all three

- The **task sentence** carries no context — the Context block does. Keep them
  separate; a fused paragraph hides the instruction.
- **Scope doubles as a write lock.** In parallel runs, scope is what keeps two
  agents from colliding on the same file.
- **Defaults are pre-answered questions.** If you can predict the question,
  answer it in the brief. If you can't safely answer it, it's a blocker —
  resolve it before spawning.
- **Output contracts are checkable.** Each one could be graded mechanically:
  did it return the right shape, within the size cap, with the evidence
  requested?
