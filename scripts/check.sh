#!/usr/bin/env bash
# Everything CI runs, locally.
set -euo pipefail
cd "$(dirname "$0")/.."

(cd backend && .venv/bin/ruff check . && .venv/bin/ruff format --check . && .venv/bin/pytest -q)
(cd frontend && npm test && npm run build)
