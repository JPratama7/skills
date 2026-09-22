# CI/CD

The pipeline spine: install → lint → test → build → deploy, each stage gating
the next. Deploy only from green builds on the main branch.

## Shape (GitHub Actions)

```yaml
name: ci
on:
  push: { branches: [main] }
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint --if-present
      - run: npm test -- --watchAll=false

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production        # gates on environment protection rules
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh ${{ github.sha }}
```

## Conventions

- **Deploy from CI, not laptops.** The pipeline is the only path to production;
  it's auditable and repeatable.
- **Tag artifacts with the git SHA** (`git rev-parse --short HEAD`), never
  `latest` — rollbacks need to know what they're rolling back to.
- **Gate deploys on environments.** GitHub `environment: production` with
  required reviewers gives you an approval step for free.
- **Authenticate with OIDC, not long-lived keys.** AWS/GCP support federated
  tokens from Actions (`aws-actions/configure-aws-credentials` with
  `role-to-assume`); no static cloud keys in secrets.
- **Cache dependencies** (`actions/setup-*` with `cache:`) — CI minutes are
  mostly dependency installs.
- **Fail fast**: lint and unit tests before build; build before deploy. Don't
  pay for a Docker build when tests already failed.
- **Keep workflows boring.** No curl-piping scripts from the internet into
  steps; pin third-party actions to a full SHA.

## Other systems

The spine translates directly: GitLab CI (`stages:`), CircleCI (orbs/jobs),
Jenkins (declarative pipeline). Same order, same gating, same SHA tags.
