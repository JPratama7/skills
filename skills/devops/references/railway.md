# Railway

Railway builds from the repo (Dockerfile or Nixpacks autodetect) — no image
push needed.

## Deploy

```bash
railway up                    # deploy the current directory; links project on first run
railway status                # verify environment + services
```

- `railway init` / `railway link` to create or attach a project.
- Prefer a Dockerfile in the repo for deterministic builds; Nixpacks is the
  fallback when none exists.

## Requirements

- The app must listen on `0.0.0.0` and read `$PORT` if set.
- Env vars: `railway variables set KEY=value` (scoped to an environment with
  `--environment`) or the dashboard. Real secrets go here, not in the repo.
- Databases: provision via `railway add --database postgres` (or plugins) —
  Railway injects `DATABASE_URL` automatically.

## Health checks and rollback

- Configure health checks in the service settings; a Dockerfile `HEALTHCHECK`
  is not used by Railway's deploy gating.
- Rollback: `railway rollback` (previous deployment) — which is why traceable
  image tags / commit-based deploys matter.

## When a Railway skill or MCP exists

If the harness has a Railway skill or MCP (check available skills/tools), prefer
it over raw CLI commands — it handles auth, project selection, and variable
management with more context.
