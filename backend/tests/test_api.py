import os
os.environ["DATABASE_URL"]="sqlite:///./test.db"
from app.database import SessionLocal, engine
from app.main import submit_attempt, interventions, decide_intervention
from app.schemas import AttemptIn, InterventionDecision
from app.seed import main as seed

def setup_module(): seed()
def teardown_module():
    # Windows may retain SQLite handles briefly; the test database is git-ignored.
    engine.dispose()

def test_student_attempt_and_idempotency():
    db=SessionLocal()
    payload=AttemptIn(question_id="diag-equivalent",response="2/4",stage="diagnostic",submission_id="test-submission-0001")
    response=submit_attempt("STU-CALC",payload,db)
    assert response["correct"]
    duplicate=submit_attempt("STU-CALC",payload,db)
    assert duplicate["duplicate"] is True
    db.close()

def test_teacher_can_view_and_decide_intervention():
    db=SessionLocal()
    plans=interventions("TEACHER-PRISM",db)
    assert len(plans)>0
    update=decide_intervention(plans[0]["id"],InterventionDecision(status="approved",teacher_notes="Use fraction strips first."),"TEACHER-PRISM",db)
    assert update["status"]=="approved"
    db.close()
