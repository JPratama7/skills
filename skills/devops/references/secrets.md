# Secrets and environments

Secrets are credentials, keys, tokens, connection strings with passwords. The
rules exist because each leak path has bitten someone:

- **Never in git** — not in code, not in `.env` committed "temporarily", not in
  CI logs. Assume anything pushed is public forever.
- **Never baked into images** — `ARG`/`ENV` values persist in layers and are
  trivially extracted from a pushed image. BuildKit `--secret` mounts a secret
  for a build step without persisting it.
- **Never echoed** — `echo $SECRET` in CI prints it into logs. Masked or not,
  don't.

## The repo carries shape, not values

`.env.example` documents every required variable with a placeholder:

```
DATABASE_URL=postgres://user:password@localhost:5432/app
SESSION_SECRET=changeme
```

The app reads the same var names locally and in production — only the source
of the values differs.

## Where secrets live per platform

| Platform | Mechanism |
|----------|-----------|
| GitHub Actions | Repo/environment secrets; OIDC for cloud auth |
| Railway | `railway variables set` (per environment) |
| Fly.io | `fly secrets set` |
| Cloud Run | Secret Manager references (`--set-secrets`) |
| ECS | Secrets Manager / SSM references in the task definition |
| Kubernetes | `Secret` resources, ideally external-secrets operator syncing a real vault |
| VPS | `.env` on the host, root-readable only; never in the image |

## Environments

Dev/staging/prod differ by configuration, never by code:

- Same image promoted through environments; config (env vars, secrets, scale)
  changes per environment.
- Staging mirrors production shape (same runtime, smaller resources) or it
  doesn't predict production behavior.
- One-off scripts and migrations run in the target environment with the
  target's config — not from a developer laptop.

## Rotation and scope

- Give each integration the least privilege that works (a deploy key, not an
  admin token).
- When a secret leaks: rotate first, clean history second. Rotating invalidates
  the leak; history rewriting doesn't.
