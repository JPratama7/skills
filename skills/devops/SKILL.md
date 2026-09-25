---
name: devops
version: 2.1.0
description: Deploy, containerize, and operate applications, plus the DevOps around them — CI/CD pipelines, secrets and environment management, health checks, and monitoring. Use whenever the user wants to deploy a service, dockerize or containerize an app, write a Dockerfile or compose setup, set up GitHub Actions or any CI pipeline, manage env vars or secrets across environments, write Kubernetes manifests, or asks "how do I get this into production" or "why won't it deploy" — even if they only say "deploy this" or "set up CI". Covers Docker/compose, Railway, Fly.io, Cloud Run, ECS, Kubernetes, plain VPS, and static hosts; defers to platform-specific skills or MCPs when the harness has them.
---

# DevOps

Take the app in front of you to a running, verifiable deployment — and wire up what surrounds it (CI, secrets, health checks) so it stays running.

## Read the app, then interview the user

A deploy has two inputs, and they come from different places. The repo tells you the app — read it. The deploy itself — where it runs, who triggers it, where secrets live — only the user can tell you. **Never infer deploy details from repo clues**: an existing Dockerfile doesn't say which platform builds it, and a guessed target produces work the user throws away.

### Read from the repo

Runtime and version from manifests and lock files (`package.json` engines, `.nvmrc`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, `composer.json`), framework and build step, the port it actually listens on (check code and config; do not guess), and external dependencies with the env vars they need.

Existing infra config (Dockerfile, compose, CI workflows, k8s manifests, Terraform) means *improve*, not replace. Read it first and preserve intentional choices.

### Interview the user — always, before writing files

Ask before building anything, even when the repo has clues. Batch the questions into one numbered message so the user can answer fast; skip items the request or existing infra already settles, and say which you're skipping and why.

1. **Target** — where should this run? Platform, cluster, VPS, or "recommend one" — a recommendation request is a valid answer; make it and confirm before building.
2. **Scope** — deploy only, or deploy + CI + secrets + observability? Build the smallest thing that satisfies the request; name the next step rather than building it unasked.
3. **Environments** — is this dev, staging, or prod? Do several environments exist or is this the only one?
4. **Trigger** — manual deploy, on merge, on tag? Existing CI pipeline that must stay?
5. **Traffic** — public URL or internal service? Domain and TLS already set up, or part of this work?
6. **Secrets and config** — which env vars does it need, and where do the real values live today (platform UI, `.env` file, vault)?
7. **State and access** — database, volumes, or other services it must reach? Who applies changes to the target — the user's SSH session, CI, or the platform itself?

If every question is already settled, list what's settled in one line and proceed. Asking anyway is how the skill earns trust — a two-line confirmation costs nothing next to a wrong-target rebuild.

## Workflow

1. Choose the deploy path
2. Package the app
3. Wire CI/CD (if in scope)
4. Configure secrets and environments (if in scope)
5. Deploy and verify
6. Hand back a runbook

### 1. Choose the deploy path

The interview answers the target; this step routes on it:

- **Static site, no server logic** → static host/CDN (Cloudflare Pages, Netlify, Vercel, S3+CDN). Docker adds a server nobody needs — say so when it applies.
- **Framework-native** (Next.js on Vercel, etc.) → the platform builds and deploys the repo directly; a Dockerfile opts you out of its edge features.
- **Long-running service** → container image or buildpack platform, whichever the target supports.
- **Target already fixed** (k8s cluster, VPS, ECS) → package for that target; don't relitigate the platform choice.

### 2. Package the app

For containers, the default production shape — deviate only with a reason:

- **Multi-stage** — build tools and compilers stay out of the final image.
- **Pin the base** — `node:22-alpine`, never `node:latest`. Prefer alpine/slim for size unless native deps need glibc.
- **Order layers by change frequency** — manifests and dependency install first, source last, so source edits don't bust the dependency cache.
- **Non-root user** — costs nothing, required by hardened runtimes.
- **No secrets in the image** — inject at runtime; BuildKit `--secret` if a build step truly needs one, never `ARG` baked into layers.
- **`.dockerignore` always** — exclude `node_modules`, `.git`, `.env*`, build output. Context size is the most common silent slowdown.
- **Health check** — `HEALTHCHECK` where the platform uses it (plain Docker, ECS); skip where the platform has its own probes (k8s, Fly, Railway) and say which applies.

Per-stack Dockerfile recipes and compose for local dev → `references/docker.md`.

### 3. Wire CI/CD

The pipeline spine: install → lint → test → build → deploy, each stage gating the next. Deploy only from green builds, tag artifacts with the git SHA, authenticate to clouds with short-lived OIDC tokens rather than long-lived keys.

→ `references/ci-cd.md`

### 4. Configure secrets and environments

Secrets live in the platform's secret store, referenced by name — never in git, images, or CI logs. Repos carry `.env.example` with placeholders. Environments (dev/staging/prod) differ by configuration, never by code.

→ `references/secrets.md`

### 5. Deploy and verify

Every registry-based target shares the spine:

```bash
docker build --platform linux/amd64 -t REGISTRY/IMAGE:$(git rev-parse --short HEAD) .
docker push REGISTRY/IMAGE:$(git rev-parse --short HEAD)
# point the platform at the image or Dockerfile
```

Registry logins: Docker Hub `docker login` · GHCR `echo $GITHUB_TOKEN | docker login ghcr.io -u USER --password-stdin` · ECR `aws ecr get-login-password | docker login --username AWS --password-stdin <acct>.dkr.ecr.<region>.amazonaws.com` · GCP `gcloud auth configure-docker <region>-docker.pkg.dev`.

Tag with the git SHA, not `latest` — `latest` makes rollbacks ambiguous.

Build-from-source platforms (Railway, Fly, Cloud Run, Render) skip the push: they build the Dockerfile from the repo.

After deploy, smoke-test the live endpoint (`curl` the health route) before declaring success. A deploy you have not verified is a guess.

Platform steps → `references/railway.md` · `references/fly-io.md` · `references/cloud-run.md` · `references/ecs.md` · `references/kubernetes.md` · `references/vps.md` · `references/static-hosting.md`

If a platform-specific skill or MCP is available in the harness (e.g. a Railway skill), prefer it for that platform's operations — this skill supplies the judgment around it.

### 6. Runbook

Close every deploy with: the exact commands run, required env vars and where to set them, the live URL or endpoint, and how to roll back (previous tag + redeploy, or the platform's rollback command).

## Hard rules

- Ask before you build — deploy details come from the user, not repo clues or defaults.
- Never commit or echo secrets — not in git, not in images, not in CI logs. `.env.example` carries placeholders only.
- Don't build infrastructure the app doesn't need — no Kubernetes for a hobby site, no Docker for a static page. Compose earns its place running sibling services locally; on a plain VPS it's also a legitimate *optional* deploy wrapper for a single service — offer it, never require it, and always show the plain `docker run` path alongside.
- Match the repo's conventions — extend existing infra config instead of adding a parallel system.
- Report the measurable facts — image size, build time, pipeline duration, deploy URL. They regress silently.
- Verify before handing over — build the image, curl the endpoint. If a tool is unavailable in the environment, say so explicitly and give the user the exact commands to run.

## Reference files (load on demand)

- Writing or improving a Dockerfile, `.dockerignore`, or compose setup → `references/docker.md`
- Deploying to Railway → `references/railway.md`
- Deploying to Fly.io → `references/fly-io.md`
- Deploying to GCP Cloud Run → `references/cloud-run.md`
- Deploying to AWS ECS/Fargate → `references/ecs.md`
- Writing k8s manifests or Helm values → `references/kubernetes.md`
- Deploying to a plain VPS → `references/vps.md`
- Static site or framework-native hosting → `references/static-hosting.md`
- Setting up CI/CD → `references/ci-cd.md`
- Secrets and environment management → `references/secrets.md`
- Health checks, logging, monitoring → `references/observability.md`
