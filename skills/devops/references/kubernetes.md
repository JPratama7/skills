# Kubernetes

Write manifests (or Helm values) pointing at a pushed image. k8s ignores the
Dockerfile `HEALTHCHECK` — probes live in the pod spec.

## Minimal deployment shape

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels: { app: app }
  template:
    metadata:
      labels: { app: app }
    spec:
      containers:
        - name: app
          image: REGISTRY/IMAGE:GIT_SHA     # pinned tag, never :latest
          ports: [{ containerPort: 3000 }]
          envFrom:
            - configMapRef: { name: app-config }
            - secretRef: { name: app-secrets }
          readinessProbe:
            httpGet: { path: /health, port: 3000 }
          livenessProbe:
            httpGet: { path: /health, port: 3000 }
            initialDelaySeconds: 10
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { memory: 512Mi }
---
apiVersion: v1
kind: Service
metadata: { name: app }
spec:
  selector: { app: app }
  ports: [{ port: 80, targetPort: 3000 }]
```

## Conventions

- **Probes**: `readinessProbe` gates traffic, `livenessProbe` restarts stuck
  containers. Keep them cheap and distinct — liveness hitting a DB-dependent
  route causes restart storms during database hiccups.
- **Secrets**: `Secret` resources at minimum; prefer the external-secrets
  operator or a secrets controller over plaintext `Secret` manifests in git.
  Never bake secrets into the image.
- **Resources**: always set requests; set limits when you know the profile.
  Missing requests = scheduler packs nodes blindly.
- **Migrations**: a Job or init container before rollout, never in the app's
  `CMD` — replicas would race.
- **Ingress/TLS**: cluster ingress controller or gateway; don't publish
  NodePorts to the internet.

## Operations

```bash
kubectl rollout status deployment/app
kubectl rollout undo deployment/app     # rollback to previous ReplicaSet
kubectl logs deploy/app --previous      # logs from the crashed container
kubectl describe pod <pod>              # events name the real failure
```

If a Helm chart exists in the repo, extend its values instead of adding raw
manifests alongside it.
