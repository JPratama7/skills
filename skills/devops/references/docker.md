# Docker: images and local compose

Starting points, not gospel. Read the manifest and lock file before adapting any
pattern. Every pattern assumes a matching `.dockerignore` exists.

## Dockerfile patterns by stack

### Node.js (server)

```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build   # omit if nothing to compile

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -S app && adduser -S app -G app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist   # or COPY . . for uncompiled apps
USER app
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

- Use the repo's package manager: `npm ci`, `pnpm install --frozen-lockfile`,
  `yarn install --frozen-lockfile`. The lock file must be in the build context.
- Next.js: enable `output: "standalone"` in `next.config.*`, then copy
  `.next/standalone` and `.next/static` into the runtime stage — drops the image
  from ~1 GB to ~150 MB.
- Prisma: run `prisma generate` in the build stage and `prisma migrate deploy`
  as a release command, not in `CMD` alongside the server.

### Python

```dockerfile
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN useradd -r -u 1000 app
COPY --from=build /install /usr/local
COPY . .
USER app
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
```

- uv/poetry: install deps into a venv in the build stage, copy the venv.
- Need gcc/libpq/etc.? Install them only in the build stage; the runtime stage
  gets just the shared libs (`libpq5`, not `libpq-dev`).
- Django: run `collectstatic` in the build stage; run migrations as a release
  step, not in `CMD`.

### Go

```dockerfile
FROM golang:1.23-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /server ./cmd/server

FROM alpine:3.20
RUN adduser -D app
COPY --from=build /server /server
USER app
EXPOSE 8080
ENTRYPOINT ["/server"]
```

- `CGO_ENABLED=0` produces a static binary — then `scratch` or
  `gcr.io/distroless/static` work as the final stage if you want minimal.
- If the app needs CA certs or tzdata, copy them from the build stage or
  install them in the final image.

### Rust

```dockerfile
FROM rust:1.80-slim AS build
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
RUN useradd -r app
COPY --from=build /app/target/release/myapp /usr/local/bin/myapp
USER app
EXPOSE 8080
ENTRYPOINT ["myapp"]
```

- Cache dependencies between builds with a dummy `cargo build` of just the
  manifests, or use `cargo-chef`.
- Full static binary: build with `--target x86_64-unknown-linux-musl`, then use
  `scratch`/`alpine` as the final stage.

### Java (Maven)

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn -q dependency:go-offline
COPY src ./src
RUN mvn -q package -DskipTests

FROM eclipse-temurin:21-jre-alpine
RUN adduser -D app
COPY --from=build /app/target/*.jar /app/app.jar
USER app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

### Ruby / Rails

```dockerfile
FROM ruby:3.3-slim AS build
WORKDIR /app
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev
COPY Gemfile Gemfile.lock ./
RUN bundle config set --local deployment true && \
    bundle config set --local without "development test" && \
    bundle install
COPY . .
RUN SECRET_KEY_BASE=dummy bundle exec rails assets:precompile

FROM ruby:3.3-slim
WORKDIR /app
RUN apt-get update -qq && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/* && \
    useradd -r app
COPY --from=build /app /app
COPY --from=build /usr/local/bundle /usr/local/bundle
USER app
EXPOSE 3000
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]
```

### Static frontend (build → nginx)

```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

- If the site is purely static, ask whether it should deploy to a CDN/static
  host instead — Docker may be the wrong tool.
- SPA routing needs `try_files $uri /index.html` in the nginx config.

## .dockerignore template

```
.git
.gitignore
node_modules
dist
build
.env
.env.*
*.log
coverage
tests
docs
*.md
.dockerignore
Dockerfile
compose.yml
docker-compose.yml
```

Keep `dist`/`build` excluded only when the Dockerfile rebuilds them; if the
build happens on CI before `docker build`, the artifact must stay in the
context — decide deliberately.

## Cross-cutting decisions

- **Alpine vs. debian-slim**: alpine is smaller but uses musl — Python wheels
  with C extensions and some Node native modules can fail. When `pip install`
  or `npm ci` compiles native code and errors out, switch to `-slim`.
- **PORT env var**: platforms like Cloud Run and Fly inject `PORT`. Make the
  app read `process.env.PORT` / `os.environ["PORT"]` with a sane default, and
  note it in the Dockerfile's `EXPOSE` comment.
- **Migrations**: never run migrations in `CMD` next to the server — race
  conditions on rolling deploys. Use a release-phase command or a one-off job.
- **Health checks**: `HEALTHCHECK CMD curl -f http://localhost:PORT/health || exit 1`
  requires curl/wget in the final image; slim images may not ship it — use a
  tiny `wget` or the runtime's own HTTP client. Skip `HEALTHCHECK` entirely on
  platforms with their own probe system (k8s, Fly, Railway) — they ignore it.

## Compose for local dev

`compose.yml` runs the app plus its dependencies locally. It is not the
production deploy mechanism unless the target is a plain VPS you control.

### When to write one

- The app needs a database, cache, queue, or other sibling service to run.
- The user asks for `docker compose up` to work.
- The repo already has one — extend it.

Skip it when the service is standalone, or when dependencies are managed
externally (hosted Postgres, etc.) — a compose file that only wraps `docker
run` adds indirection without value.

### Shape

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    env_file: .env          # local only; never commit real values
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app              # optional: live-reload dev mount
      - /app/node_modules   # keep container's node_modules, don't overwrite
    command: npm run dev    # override the production CMD for dev

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: localdev
      POSTGRES_DB: app
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 3s
      retries: 10

volumes:
  db-data:
```

### Conventions

- **Health-gate dependencies.** `depends_on` alone only waits for container
  start, not readiness. Pair it with a `healthcheck` + `service_healthy` so the
  app doesn't crash-loop waiting for Postgres to accept connections.
- **Use `env_file: .env` for dev secrets**, and ship `.env.example` with
  placeholders. The app reads the same var names locally and in production.
- **Bind-mount source for dev, not prod.** The `volumes` mount makes code
  changes visible without rebuilds. If the production image bakes the source,
  keep a separate `compose.yml` (dev) vs. relying on the Dockerfile (prod), or
  use a `command` override + mount as above.
- **Name services by role** (`db`, `cache`, `app`), not by image
  (`postgres`, `redis`). Compose DNS resolves service names — the app's
  `DATABASE_URL` becomes `postgres://app:localdev@db:5432/app`.
- **Pin dependency images** (`postgres:16-alpine`, not `postgres:latest`).
- **Named volumes for stateful data.** Bind-mounting a host dir into Postgres
  causes permission problems on Linux; named volumes just work.
- **Ports**: publish only what a developer needs (`"3000:3000"`). Internal
  services don't need host ports — the compose network handles it.

### Verify

```bash
docker compose up --build
# in another shell:
docker compose ps        # all services healthy/running
curl localhost:3000/health
docker compose down -v   # clean teardown check
```

`down -v` deletes the named volume — warn the user before suggesting it if the
dev database has data worth keeping.
