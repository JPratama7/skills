# Health checks, logging, monitoring

The deploy isn't done when the command exits — it's done when the endpoint
responds and the logs look alive.

## Health endpoints

Two distinct questions, often conflated:

- **Liveness** — is the process wedged? Should be cheap and dependency-free:
  if this fails, the platform restarts the container.
- **Readiness** — can this instance serve traffic? May check the database;
  failing removes the instance from the load balancer without restarting it.

Expose both (commonly `/healthz` and `/readyz`, or one endpoint with a `?deep`
variant). A health check that only returns 200 unconditionally tells you
nothing.

## Where probes are configured

| Platform | Mechanism | Dockerfile HEALTHCHECK |
|----------|-----------|------------------------|
| Plain docker | `HEALTHCHECK` | used |
| ECS/Fargate | task definition healthCheck | ignored unless set there |
| Kubernetes | livenessProbe / readinessProbe | ignored |
| Fly.io | `[checks]` in fly.toml | ignored |
| Railway | service settings | not used for deploy gating |
| Cloud Run | startup/liveness probes in service config | not needed |

Configure the probe where the platform reads it — a Dockerfile HEALTHCHECK on
k8s is dead weight.

## Logging

- **Log to stdout/stderr** — the platform's `logs` command (docker logs, kubectl
  logs, fly logs, `gcloud run services logs read`) collects it. Never log to
  files inside the container.
- **Structured lines** (JSON) with timestamp, level, request ID — parseable
  beats pretty.
- **Log the useful failure, not the stack trace only**: which request, which
  input, which dependency timed out.
- Don't log secrets or full request bodies; redact by default.

## Monitoring

Start with the RED metrics per service: **R**ate, **E**rrors, **D**uration.
Every platform above ships basic metrics (requests, latency, restarts, CPU/MEM)
— point the user at the dashboard before suggesting a monitoring stack.

Alert on symptoms users feel (error rate, latency, saturation), not causes
(CPU spikes at 3am that self-resolve). If the app has no health endpoint and
structured logs, adding those is the first observability investment — before
any third-party tooling.
