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

# Install Python dependencies (production only — no pytest/httpx)
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir \
        fastapi==0.115.6 \
        uvicorn[standard]==0.34.0 \
        sqlalchemy==2.0.36 \
        pydantic==2.10.3 \
        httpx==0.28.1

# Copy backend source
COPY backend/app ./app

# Copy built React bundle → served as static files by FastAPI
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Seed the demo database at image build time so the container
# starts immediately without a migration step.
RUN python -m app.seed

# Render injects $PORT at runtime; default to 8000
ENV PORT=8000

EXPOSE 8000

# --workers 1 keeps SQLite writes safe on the free tier
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 1"]
