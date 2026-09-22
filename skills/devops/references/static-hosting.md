# Static sites and framework-native hosting

When the app has no server-side runtime, containers are usually the wrong tool.
Say so plainly — a static site on Docker is a server nobody needs.

## When not to containerize

- **Pure static sites** (HTML/CSS/JS, no build or a client-only build) →
  CDN/static hosts: Cloudflare Pages, Netlify, Vercel, GitHub Pages, S3+CDN.
- **Framework-native apps** (Next.js, Nuxt, SvelteKit, Astro) → their native
  platforms build and deploy the repo directly; a Dockerfile opts you out of
  edge/ISR features and adds a server to pay for.
- **Cron jobs and one-off scripts** → platform schedulers, GitHub Actions on a
  schedule, or a serverless function — not a always-on container.
- **Libraries/packages** → the registry (npm/PyPI/crates.io); there is nothing
  to deploy.

## Deploying static

- Output dir is whatever the build produces (`dist/`, `build/`, `.output/`,
  `_site`). If there's no build step, deploy the directory as-is.
- **SPA routing**: configure `try_files $uri /index.html` (nginx) or the
  platform's rewrite setting, or deep links 404.
- Headers and redirects belong in platform config (`_headers`/`_redirects` on
  Cloudflare Pages/Netlify), not in a custom server.
- Cache aggressively: hashed assets get long max-age; `index.html` gets
  `no-cache` so deploys are picked up.

## If the user insists on a container

Serve with nginx/caddy, not a Node server:

```dockerfile
FROM nginx:1.27-alpine
COPY dist/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

No compose file for a single static service — it's indirection without value.
