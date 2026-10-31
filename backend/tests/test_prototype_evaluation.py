"""Checks for the five measures in section 07 of the Decode submission.

Each test class corresponds to one row of "How We Will Prove the Prototype".
They validate software behaviour on simulated learners only; they say nothing
about learning gains with real students.
"""

import pytest
from fastapi.testclient import TestClient

from app.engine import update_profile
from app.main import app
from app.seed import LEARNERS, QUESTIONS
from app.seed import main as seed

PASSWORD = "PrismDemo!2026"
QUESTION_BY_ID = {q[0]: q for q in QUESTIONS}


@pytest.fixture(scope="module")
def client():
    seed()
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def fresh_demo(client):
    client.post("/api/demo/reset")
    yield


def auth(client, email):
    token = client.post("/api/auth/login", json={"email": email, "password": PASSWORD}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def workspace_learners(client):
    data = client.get("/api/teacher/workspace", headers=auth(client, "teacher@prism.demo")).json()
    return {row["code"]: row for row in data["learners"]}


def evidence(*answers):
    rows = []
    for qid, response in answers:
        _, stage, _, _, _, expected, _, mapping = QUESTION_BY_ID[qid]
        rows.append(
            {
                "correct": response == expected,
                "stage": stage,
                "transfer": stage == "test",
                "misconception": mapping.get(response),
            }
        )
    return rows


class TestDiagnosticConsistency:
    """Does the rule engine match predefined cases and flag ambiguous evidence?"""

    @pytest.mark.parametrize(("code", "intended_route"), [(c, r) for c, _, _, r in LEARNERS])
    def test_seeded_profiles_are_derived_by_the_engine(self, client, code, intended_route):
        assert workspace_learners(client)[code]["recommendation"] == intended_route

    def test_conflicting_conceptual_errors_are_flagged_for_follow_up(self):
        result = update_profile(
            0.35,
            evidence(("diag-magnitude", "1/8"), ("practice-guided", "8"), ("diag-equivalent", "2/4")),
        )
        assert result.recommendation == "follow-up"
        assert result.misconception is None

    def test_one_wrong_answer_does_not_label_a_learner(self):
        result = update_profile(0.35, evidence(("diag-magnitude", "1/8")))
        assert result.misconception is None


class TestRouteAppropriateness:
    """Does each profile receive the intended visual, guided, foundation or extension route?"""

    def test_each_archetype_gets_a_distinct_route(self, client):
        routes = {row["recommendation"] for row in workspace_learners(client).values()}
        assert routes == {"visual-support", "foundation", "guided-practice", "extension"}

    def test_procedural_slips_are_not_reported_as_a_misconception(self, client):
        kabir = workspace_learners(client)["STU-CALC"]
        assert kabir["recommendation"] == "guided-practice"
        assert kabir["misconception"] is None


class TestTransferCheck:
    """Does the system update its estimate using a new problem?"""

    def test_correct_transfer_answer_raises_the_estimate(self, client):
        before = workspace_learners(client)["STU-CALC"]
        reply = client.post(
            "/api/learning/attempts",
            headers=auth(client, "kabir@prism.demo"),
            json={
                "question_id": "test-transfer",
                "response": "4/6",
                "stage": "test",
                "submission_id": "eval-transfer-001",
            },
        ).json()
        assert reply["correct"] is True
        assert reply["profile"]["evidence_count"] == before["evidence_count"] + 1
        assert reply["profile"]["mastery"] > before["mastery"]


class TestTeacherControl:
    """Can the teacher inspect, edit and reject recommendations and see the plan update?"""

    def test_teacher_can_edit_then_reject_a_plan(self, client):
        headers = auth(client, "teacher@prism.demo")
        plans = client.get("/api/teacher/interventions", headers=headers).json()
        assert plans and all(p["status"] == "proposed" for p in plans)

        target = plans[0]
        edited = client.put(
            f"/api/teacher/interventions/{target['id']}",
            headers=headers,
            json={"status": "modified", "duration": "20 min", "teacher_notes": "Start with strips."},
        ).json()
        assert edited["status"] == "modified" and edited["duration"] == "20 min"

        client.put(f"/api/teacher/interventions/{target['id']}", headers=headers, json={"status": "rejected"})
        after = {p["id"]: p for p in client.get("/api/teacher/interventions", headers=headers).json()}
        assert after[target["id"]]["status"] == "rejected"

    def test_teacher_can_reassign_students_between_groups(self, client):
        headers = auth(client, "teacher@prism.demo")
        plan = client.get("/api/teacher/interventions", headers=headers).json()[0]
        updated = client.put(
            f"/api/teacher/interventions/{plan['id']}",
            headers=headers,
            json={"status": "modified", "student_codes": ["STU-VISUAL", "STU-CALC"]},
        ).json()
        assert sorted(updated["student_codes"]) == ["STU-CALC", "STU-VISUAL"]

    def test_students_cannot_change_teacher_plans(self, client):
        plan_id = client.get("/api/teacher/interventions", headers=auth(client, "teacher@prism.demo")).json()[0]["id"]
        response = client.put(
            f"/api/teacher/interventions/{plan_id}",
            headers=auth(client, "student@prism.demo"),
            json={"status": "rejected"},
        )
        assert response.status_code in (401, 403)


class TestPracticality:
    """Can the flow survive the offline path (queued answers replayed on reconnect)?"""

    def test_replaying_a_queued_answer_is_idempotent(self, client):
        headers = auth(client, "meera@prism.demo")
        body = {
            "question_id": "practice-standard",
            "response": "-3/4 and 6/-8",
            "stage": "practice",
            "submission_id": "offline-q-0001",
        }
        first = client.post("/api/learning/attempts", headers=headers, json=body).json()
        replay = client.post("/api/learning/attempts", headers=headers, json=body).json()
        assert first["duplicate"] is False
        assert replay["duplicate"] is True
        assert workspace_learners(client)["STU-EXTEND"]["evidence_count"] == first["profile"]["evidence_count"]
