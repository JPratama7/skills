# Plain VPS

The user controls a server and runs Docker on it. Compose is the convenient
production mechanism here — restart policy, ports, and env in one declarative
file — but for a single service it's optional. Always show the equivalent
`docker run -d --restart unless-stopped -p ...` so the user isn't locked into
the compose plugin.

## Deploy

```bash
# with an image pulled from a registry:
docker compose pull && docker compose up -d
# or build on the host:
docker compose up -d --build

# without compose (single service):
docker run -d --name app --restart unless-stopped -p 127.0.0.1:3000:3000 \
  --env-file .env REGISTRY/IMAGE:TAG
```

## Production compose shape

- `restart: unless-stopped` on every service.
- Published ports only for what must be reachable; internal services talk over
  the compose network.
- `env_file: .env` for runtime config; `.env` lives on the host, never in git.
- No source bind-mounts — the image bakes the code.
- Pin image tags (git SHA), so rollback is a re-pull.

## TLS and exposure

Put TLS termination in front — Caddy (automatic certs) or nginx + certbot.
Don't expose the app container's port directly to the internet if you can
avoid it.

```yaml
# caddy fronting the app, same compose network
services:
  caddy:
    image: caddy:2-alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy-data:/data
```

## Operations

- Rollback: `docker compose pull` the previous tag + `up -d` — which is why SHA
  tags matter.
- Logs: `docker compose logs -f app`.
- Updates: `docker compose pull && docker compose up -d` in a cron/systemd timer
  if the user wants auto-updates — but say what unattended upgrades imply.
- `docker system prune` reclaims space from old images; suggest it when disk
  fills, not preemptively.
