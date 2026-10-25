import os
os.environ["DATABASE_URL"]="sqlite:///./test.db"
from fastapi.testclient import TestClient
from app.main import app
from app.seed import main as seed

def setup_module(): seed()
def teardown_module():
    if os.path.exists("test.db"): os.remove("test.db")

def test_student_attempt_and_idempotency():
    c=TestClient(app)
    response=c.post("/api/students/STU-CALC/attempts",json={"question_id":"diag-equivalent","response":"2/4","stage":"diagnostic","submission_id":"test-submission-0001"})
    assert response.status_code==200 and response.json()["correct"]
    duplicate=c.post("/api/students/STU-CALC/attempts",json={"question_id":"diag-equivalent","response":"2/4","stage":"diagnostic","submission_id":"test-submission-0001"})
    assert duplicate.json()["duplicate"] is True

def test_teacher_can_view_and_decide_intervention():
    c=TestClient(app,headers={"X-Demo-Teacher":"TEACHER-PRISM"})
    plans=c.get("/api/teacher/interventions")
    assert plans.status_code==200 and len(plans.json()) > 0
    update=c.put(f"/api/teacher/interventions/{plans.json()[0]['id']}",json={"status":"approved","teacher_notes":"Use fraction strips first."})
    assert update.status_code==200 and update.json()["status"]=="approved"
