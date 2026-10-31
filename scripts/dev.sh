#!/usr/bin/env bash
# Start the API (port 8000) and the web app (port 5173). Ctrl+C stops both.
set -euo pipefail
cd "$(dirname "$0")/.."

(cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000) &
API_PID=$!
trap 'kill $API_PID 2>/dev/null' EXIT
(cd frontend && npm run dev)
