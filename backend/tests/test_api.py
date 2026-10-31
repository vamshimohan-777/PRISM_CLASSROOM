import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
from app.database import SessionLocal, engine
from app.main import (
    curriculum,
    decide_intervention,
    demo_personas,
    interventions,
    learning_units,
    login,
    my_progress,
    reset_demo,
    submit_attempt,
    teacher_student_detail,
    teacher_workspace,
)
from app.models import User
from app.schemas import AttemptIn, InterventionDecision, LoginIn
from app.seed import main as seed


def setup_module():
    seed()


def teardown_module():
    # Windows may retain SQLite handles briefly; the test database is git-ignored.
    engine.dispose()


def test_student_attempt_and_idempotency():
    db = SessionLocal()
    payload = AttemptIn(
        question_id="diag-equivalent", response="2/4", stage="diagnostic", submission_id="test-submission-0001"
    )
    response = submit_attempt("STU-CALC", payload, db)
    assert response["correct"]
    duplicate = submit_attempt("STU-CALC", payload, db)
    assert duplicate["duplicate"] is True
    db.close()


def test_teacher_can_view_and_decide_intervention():
    db = SessionLocal()
    plans = interventions("TEACHER-PRISM", db, authorization=None)
    assert len(plans) > 0
    update = decide_intervention(
        plans[0]["id"],
        InterventionDecision(
            status="approved",
            teacher_notes="Use fraction strips first.",
            activity="Review fraction strips with peers.",
            duration="15 min",
            outcome="Student connects parts to whole.",
        ),
        "TEACHER-PRISM",
        db,
        authorization=None,
    )
    assert update["status"] == "approved"
    assert update["duration"] == "15 min"
    db.close()


def test_project_declares_a_single_cbse_curriculum():
    details = curriculum()
    assert details["board_code"] == "CBSE"
    assert details["grade"] == 8
    assert "Rational Numbers" in details["module_title"]


def test_authentication_exposes_a_multi_chapter_student_catalogue():
    db = SessionLocal()
    auth = login(LoginIn(email="student@prism.demo", password="PrismDemo!2026"), db)
    assert auth["token_type"] == "bearer"
    assert auth["user"]["role"] == "student"
    units = learning_units()
    assert len(units) == 8
    user = db.query(User).filter_by(email="student@prism.demo").first()
    progress = my_progress(user=user, db=db)
    assert len(progress) == 8
    db.close()


def test_teacher_workspace_contains_rich_learner_profiles():
    db = SessionLocal()
    workspace = teacher_workspace(authorization=None, x_demo_teacher="TEACHER-PRISM", db=db)
    assert workspace["class_code"] == "8A-CBSE"
    assert len(workspace["learners"]) >= 4
    aarav = next(row for row in workspace["learners"] if row["code"] == "STU-VISUAL")
    assert aarav["name"] == "Aarav Sharma"
    assert aarav["recommendation"] == "visual-support"
    assert aarav["misconception"] == "denominator-magnitude"
    db.close()


def test_student_detail_and_attempt_history():
    db = SessionLocal()
    detail = teacher_student_detail("STU-VISUAL", authorization=None, x_demo_teacher="TEACHER-PRISM", db=db)
    assert detail["name"] == "Aarav Sharma"
    assert detail["recommendation"] == "visual-support"
    assert len(detail["attempts"]) >= 3
    db.close()


def test_demo_personas_and_reset():
    db = SessionLocal()
    personas = demo_personas(db)
    assert len(personas) == 5
    assert any(p["id"] == "aarav" for p in personas)
    assert any(p["id"] == "teacher" for p in personas)

    reset_res = reset_demo(db)
    assert reset_res["status"] == "ok"
    db.close()
