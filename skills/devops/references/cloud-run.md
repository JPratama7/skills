# GCP Cloud Run

Cloud Run builds from source (via Cloud Build) or runs a pushed Artifact
Registry image.

## Deploy

```bash
gcloud run deploy SERVICE --source .        # builds the Dockerfile for you
# or from a pushed image:
gcloud run deploy SERVICE --image REGION-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG
```

## Hard requirements

- The container MUST listen on `$PORT` (default 8080) on `0.0.0.0`. A
  mismatched port is the #1 Cloud Run failure — the service health-checks the
  port it expects, not the one your app uses.
- Region matters: set `--region` explicitly; defaults surprise people.

## Secrets and env

```bash
gcloud run deploy SERVICE --set-secrets KEY=secret-name:latest
```

- Never `--set-env-vars` for real secrets — they land in the service spec and
  logs. Use Secret Manager references.
- Grant the runtime service account `roles/secretmanager.secretAccessor` on the
  secret.

## Operations

- Rollback: deploy the previous revision's image, or split traffic back:
  `gcloud run services update-traffic SERVICE --to-revisions PREV=100`.
- Set `--min-instances=1` if cold starts are unacceptable; otherwise the
  default scale-to-zero is the cheapest correct choice.
- Health check: Cloud Run probes `$PORT` itself; no Dockerfile `HEALTHCHECK`
  needed.
