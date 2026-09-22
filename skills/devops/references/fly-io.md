# Fly.io

Fly builds the Dockerfile remotely and runs it on Machines. Deploys are
image-based under the hood but driven from the repo.

## Deploy

```bash
fly launch          # detects the Dockerfile, writes fly.toml, first deploy
fly deploy          # build + push + rolling update
fly status          # is it up?
```

- `fly launch` generates `fly.toml` — commit it; it is the deploy config.
- `internal_port` in `fly.toml` must match the port the app binds (and the
  Dockerfile's `EXPOSE`). Mismatch = app unreachable.
- The app must listen on `0.0.0.0`.

## Config, secrets, scale

```bash
fly secrets set KEY=value        # real secrets — never in fly.toml or the image
fly vars set KEY=value           # non-sensitive config
fly scale count 2                # machines
fly scale memory 512             # VM size
```

## Health checks and rollback

- Machines have their own health check config in `fly.toml` (`[checks]`) — a
  Dockerfile `HEALTHCHECK` is ignored. Define checks there.
- Rollback: `fly releases` to list, `fly rollback <version>` to revert.
- Logs: `fly logs`; SSH: `fly ssh console`.
