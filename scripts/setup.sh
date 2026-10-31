#!/usr/bin/env bash
# One-time setup for macOS/Linux: backend virtualenv, demo data, frontend deps.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv backend/.venv
backend/.venv/bin/pip install -q -r backend/requirements-dev.txt
(cd backend && .venv/bin/python -m app.seed)
(cd frontend && npm ci)
echo "Setup complete. Run scripts/dev.sh to start both servers."
