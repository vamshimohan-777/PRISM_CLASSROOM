# Deploying PRISM Classroom on Render

Frontend and backend deploy together as **one** Render web service. The
Dockerfile builds the React bundle, then FastAPI serves that bundle alongside
`/api/*` from the same port — so there is no second service to create, no
cross-origin configuration, and no separate frontend URL to keep in sync.

```
┌──────────── one Render web service, one port ────────────┐
│  FastAPI (uvicorn)                                       │
│    /api/*                → JSON API                      │
│    /assets/*             → hashed JS + CSS bundles       │
│    /robots.txt, /sitemap.xml, /llms.txt, og image        │
│    everything else       → index.html (SPA fallback)     │
└──────────────────────────────────────────────────────────┘
```

---

## 1. Deploy (about five minutes)

1. **Push the branch to GitHub.**
   ```bash
   git push -u origin minor-fixes
   ```
   Merge into your default branch if you want `autoDeploy` to track it.

2. **Create the service.** Go to [dashboard.render.com](https://dashboard.render.com)
   → **New** → **Blueprint** → connect this repository.

3. **Apply.** Render reads `render.yaml` and configures everything —
   runtime, Dockerfile path, health check, and all environment variables.
   You should not need to type any settings by hand.

4. **Wait for the first build.** Roughly 4–8 minutes: it installs npm
   dependencies, builds the SPA with Vite, installs the Python
   dependencies, then starts uvicorn.

5. **Verify.** Render reports the service healthy once
   `GET /api/health` returns `{"status":"ok"}`. Then check:

   | URL | Expect |
   | :--- | :--- |
   | `/` | Landing page |
   | `/app` | Sign-in screen |
   | `/curriculum`, `/engines`, `/flowchart`, `/faq` | Each loads directly (deep links work) |
   | `/api/health` | `{"status":"ok"}` |
   | `/api/docs` | Interactive OpenAPI docs |
   | `/sitemap.xml`, `/robots.txt`, `/llms.txt` | Served as files |

Demo accounts are seeded automatically on first boot. All five share the
password `PrismDemo!2026` — see `DEMO_LOGINS.md`.

---

## 2. What `render.yaml` sets for you

| Variable | Value | Why |
| :--- | :--- | :--- |
| `PORT` | `8000` | Render injects this; uvicorn binds to it. |
| `DATABASE_URL` | `sqlite:////data/prism.db` | See persistence below. |
| `PRISM_AUTH_SECRET` | generated | Render creates a random secret on first deploy, so tokens are never signed with the development fallback committed in this repo. |
| `PRISM_DEMO_MODE` | `1` | Keeps the persona endpoints and `POST /api/demo/reset` available for judging. Set to `0` for real learner data. |
| `CORS_ORIGINS` | empty | Not needed — the SPA is same-origin. |
| `GEMINI_API_KEY` | empty | Optional Answer Engine fallback; never affects learner routing. |

---

## 3. Persistence — read this before judging

**Render free instances have an ephemeral filesystem and cannot mount a
persistent disk.** On the free plan the SQLite file is therefore recreated
whenever the instance restarts, redeploys, or wakes from idle, and
`entrypoint.sh` reseeds the demo classroom.

For a judged demo that is usually fine: the four archetypes are always
present and reproducible. But anything a judge enters themselves — a new
account, new attempts — can disappear when the free instance spins down
after inactivity. If a judge will return to the site later, pick one of these.

### Option A — free managed Postgres (recommended)

Survives redeploys and costs nothing, though a free Render Postgres instance
expires 30 days after creation.

In `render.yaml`, uncomment the `databases:` block at the bottom and replace
the `DATABASE_URL` entry with:

```yaml
      - key: DATABASE_URL
        fromDatabase:
          name: prism-db
          property: connectionString
```

No code change is needed. The driver (`psycopg`) is already in
`requirements.txt`, and `app/database.py` rewrites Render's legacy
`postgres://` scheme to the `postgresql+psycopg://` form SQLAlchemy 2
requires — a step that is easy to miss and fails at boot without it.

### Option B — persistent disk (paid instance)

Disks require a paid instance type. Set `plan: starter` and add:

```yaml
    disk:
      name: prism-data
      mountPath: /data
      sizeGB: 1
```

`DATABASE_URL` already points at `/data/prism.db`, so nothing else changes.

Either way, `entrypoint.sh` seeds **only when the database is empty**, so real
learner data is never overwritten by a redeploy.

---

## 4. Running the same image locally

```bash
docker build -t prism-classroom .
docker run --rm -p 8000:8000 prism-classroom
# open http://localhost:8000
```

To rehearse a production configuration:

```bash
docker run --rm -p 8000:8000 \
  -e PRISM_DEMO_MODE=0 \
  -e PRISM_AUTH_SECRET="$(python -c 'import secrets;print(secrets.token_urlsafe(48))')" \
  prism-classroom
```

With `PRISM_DEMO_MODE=0` the persona endpoints and `/api/demo/reset` return
404, and the app refuses to start without `PRISM_AUTH_SECRET`.

---

## 5. Troubleshooting

| Symptom | Cause |
| :--- | :--- |
| Build fails in the npm stage | `package-lock.json` out of sync with `package.json`. Run `npm install` in `frontend/` and commit the lockfile. |
| Service starts but pages are blank | The SPA bundle was not copied. Confirm the Docker build reached `COPY --from=frontend-builder`. `backend/tests/test_unified_serving.py` covers this locally. |
| Deep links 404 | Something is serving the API without the SPA fallback; check the catch-all route at the end of `app/main.py`. |
| Boot fails with `PRISM_AUTH_SECRET must be set` | `PRISM_DEMO_MODE=0` without a secret. Add one, or set demo mode back to `1`. |
| `NoSuchModuleError: postgres` | A `DATABASE_URL` bypassing `normalise_database_url`. Use the `fromDatabase` form above. |
| Data disappeared after a redeploy | Expected on the free plan. See Persistence. |

---

## Notes on the Netlify config

`netlify.toml` remains for a **frontend-only** deployment, which needs a
separately hosted backend and `VITE_API_URL` pointing at it, plus that origin
added to `CORS_ORIGINS`. The Render blueprint above is the simpler path and
the one these docs assume.
