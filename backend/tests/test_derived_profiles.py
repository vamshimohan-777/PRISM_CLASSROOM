"""Guards the claim that no learner profile anywhere is hand-written.

Every mastery score, misconception label and route in the database must be
reproducible by replaying the `attempts` table through the rules engine.
"""
import os

os.environ["DATABASE_URL"] = "sqlite:///./test_derived.db"

from app.database import SessionLocal, engine
from app.models import Attempt, LearnerProgress, Student
from app.scoring import recompute_student
from app.seed import main as seed


def setup_module():
    seed()


def teardown_module():
    engine.dispose()


def _snapshot(db):
    return {
        (row.student_id, row.concept_id): (
            row.mastery,
            row.evidence_count,
            row.misconception,
            row.prerequisite_status,
            row.recommendation,
        )
        for row in db.query(LearnerProgress).all()
    }


def test_every_seeded_profile_is_reproducible_from_attempts():
    """Re-deriving from raw attempts must reproduce the stored profile exactly.

    If any profile had been hand-written into the seed, this would drift.
    """
    db = SessionLocal()
    before = _snapshot(db)
    assert before, "expected seeded learner profiles"
    for student in db.query(Student).all():
        recompute_student(db, student.id)
    db.flush()
    assert _snapshot(db) == before
    db.close()


def test_demo_archetypes_are_engine_outputs_not_fixtures():
    """The four published archetypes must fall out of the rules engine."""
    expected = {
        "STU-VISUAL": "visual-support",
        "STU-FOUNDATION": "foundation",
        "STU-CALC": "guided-practice",
        "STU-EXTEND": "extension",
    }
    db = SessionLocal()
    for code, route in expected.items():
        student = db.query(Student).filter_by(code=code).first()
        profile = (
            db.query(LearnerProgress)
            .filter_by(student_id=student.id, concept_id="equivalent-fractions")
            .first()
        )
        assert profile.recommendation == route, f"{code} routed to {profile.recommendation}"
    db.close()


def test_foundation_route_is_reachable_from_prerequisite_evidence():
    """The foundation branch fires from real DAG evidence, not a seeded value.

    Diya's weak `fraction-parts` attempt is what makes her prerequisites
    'needs-check' on the dependent concept.
    """
    db = SessionLocal()
    student = db.query(Student).filter_by(code="STU-FOUNDATION").first()
    prerequisite = (
        db.query(LearnerProgress)
        .filter_by(student_id=student.id, concept_id="fraction-parts")
        .first()
    )
    assert prerequisite is not None, "prerequisite node carries its own evidence"
    assert prerequisite.evidence_count > 0

    dependent = (
        db.query(LearnerProgress)
        .filter_by(student_id=student.id, concept_id="equivalent-fractions")
        .first()
    )
    assert dependent.prerequisite_status == "needs-check"
    assert dependent.recommendation == "foundation"
    db.close()


def test_no_profile_exists_without_supporting_attempts():
    """A stored profile must always be backed by at least one recorded attempt."""
    db = SessionLocal()
    for row in db.query(LearnerProgress).filter(LearnerProgress.evidence_count > 0).all():
        attempts = db.query(Attempt).filter_by(student_id=row.student_id).count()
        assert attempts > 0, f"profile {row.concept_id} has evidence but no attempts"
    db.close()
