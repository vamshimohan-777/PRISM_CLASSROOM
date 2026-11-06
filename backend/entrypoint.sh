#!/bin/sh
# Seed the database on first start rather than at image build time.
#
# Seeding during `docker build` bakes prism.db into an image layer, so every
# redeploy or container restart silently discards whatever learners did. With
# the database on a mounted disk this seeds once, then leaves real data alone
# on subsequent boots. `app.seed` is itself idempotent, but checking first
# keeps the common path quiet.
set -e

python - <<'PY'
import os
from app.database import Base, engine, SessionLocal
from app.models import Classroom

Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    if db.query(Classroom).count() == 0:
        print("No classroom found; seeding demo data.", flush=True)
        from app.seed import main as seed
        seed()
    else:
        print("Existing database detected; leaving it untouched.", flush=True)
finally:
    db.close()
PY

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 1
