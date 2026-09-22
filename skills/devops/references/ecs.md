# AWS ECS / Fargate

Registry-based: you push an image to ECR, a task definition runs it, a service
keeps the desired count.

## Deploy

```bash
# 1. Authenticate to ECR
aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin <acct>.dkr.ecr.<region>.amazonaws.com

# 2. Build and push (amd64 for Fargate)
docker build --platform linux/amd64 -t <acct>.dkr.ecr.<region>.amazonaws.com/REPO:$(git rev-parse --short HEAD) .
docker push <acct>.dkr.ecr.<region>.amazonaws.com/REPO:$(git rev-parse --short HEAD)

# 3. Point the service at the new image (update task def revision if needed)
aws ecs update-service --cluster CLUSTER --service SERVICE --force-new-deployment
```

## Task definition requirements

- Container image URI, port mappings, and the container's env.
- Env vars: plaintext via `environment` is fine for non-secrets; secrets via
  Secrets Manager or SSM Parameter Store references (`secrets:` in the task
  def), never plaintext and never baked into the image.
- Health check: Fargate ignores the Dockerfile `HEALTHCHECK` unless the task
  definition sets `healthCheck` (with `startPeriod`) — configure it there.
- Set memory/CPU limits explicitly; Fargate has no host defaults.

## Operations

- Rollback: redeploy the previous task definition revision
  (`aws ecs update-service --task-definition family:revision`).
- Watch a deploy: `aws ecs wait services-stable --cluster X --services Y`.
- Debugging crashes: `aws logs tail LOG_GROUP --follow` — the stopped-container
  reason in `describe-tasks` usually names the real error.
