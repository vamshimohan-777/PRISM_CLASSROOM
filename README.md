# PRISM Classroom

PRISM is a working vertical-slice prototype for Class 8 Mathematics — Equivalent Fractions. It supports an evidence-led student learning loop and a teacher-controlled **Intervention Compiler**. All included people and learning data are synthetic.

## Highlights

- Student workflow: diagnostic → adaptive learn → guided/independent solve → transfer verification.
- Deterministic, explainable rules for prerequisite gaps, possible misconceptions, mastery, uncertainty, and extension routes.
- Teacher workspace that groups similar needs, shows the supporting evidence, and lets a teacher edit, approve, or reject a plan.
- FastAPI + SQLAlchemy + SQLite persistence; React + TypeScript UI.
- Pseudonymous demo identities; no real child data.

## Architecture

```mermaid
flowchart LR
  UI[React student & teacher UI] --> API[FastAPI REST API]
  API --> Engine[Rules engine]
  Engine --> DB[(SQLite)]
  DB --> Compiler[Intervention Compiler]
  Compiler --> API
```

## Run locally

Requirements: Node 20+ and Python 3.11+.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The app is pre-populated with synthetic data; choose **Student demo** or **Teacher dashboard** on the entry screen.

## Tests

```powershell
cd backend
pytest -q
cd ..\frontend
npm run test
npm run build
```

## Core data model

`Student`, `Teacher`, `Classroom`, `Concept`, `Question`, `Attempt`, `LearnerProgress`, and `Intervention` are persisted with relational foreign keys. Attempt submissions are idempotent via a client submission ID.

## Design decisions

Recommendations are provisional rule outputs, not diagnoses or calibrated probabilities. A single wrong answer cannot create a misconception label. Contradictory or low-volume evidence creates a review/follow-up recommendation. Teacher decisions override and are retained.

## Privacy and limitations

- Seed records are fictional and intentionally pseudonymous.
- Demo identity headers are not production authentication. A deployment must replace them with a vetted identity provider, HTTPS, rate limiting, and role audits.
- English content is reviewed for this prototype. Telugu is represented as a language preference only; a reviewed Telugu pack is not included.
- Offline response queuing and production deployment/video capture are not included.
- This prototype has not been evaluated for learning outcomes.

## Deployment

Deploy the API with a persistent volume for `prism.db` (or migrate `DATABASE_URL` to PostgreSQL), set `CORS_ORIGINS` to the frontend URL, and set `VITE_API_URL` when building the frontend. Do not use ephemeral SQLite storage in production.
