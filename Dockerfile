# ============================================================
# PRISM CLASSROOM — Production Dockerfile
# Packages React Frontend + FastAPI Backend in one container
# Served by a single Uvicorn process on $PORT (default 8000)
# ============================================================

# ── Stage 1: Build React/TypeScript frontend ──────────────────
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Cache npm install layer separately
COPY frontend/package*.json ./
RUN npm ci --prefer-offline

# Build production bundle
COPY frontend/ ./
RUN npm run build


# ── Stage 2: Python + serve static assets ────────────────────
FROM python:3.11-slim AS runtime
WORKDIR /app

# System deps (needed by some Python wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies. requirements.txt is the single source of truth:
# this previously copied the file and then ignored it in favour of a duplicated
# inline list, so the two could drift apart unnoticed.
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/app ./app
COPY backend/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Copy built React bundle → served as static files by FastAPI
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Default the database onto /data so a mounted disk survives redeploys.
# Seeding happens on first start (see entrypoint.sh), not at build time:
# baking prism.db into an image layer discarded all learner data on every
# redeploy.
RUN mkdir -p /data
ENV DATABASE_URL=sqlite:////data/prism.db

# Render injects $PORT at runtime; default to 8000
ENV PORT=8000

EXPOSE 8000

# --workers 1 keeps SQLite writes safe on the free tier
CMD ["./entrypoint.sh"]
