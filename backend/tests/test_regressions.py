"""Regression tests for behaviour a judge or teacher could hit directly."""
import os
import subprocess
import sys
import uuid

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_regressions.db")

import pytest
from fastapi.testclient import TestClient

from app.answer_engine import answer_engine
from app.auth import PBKDF2_ITERATIONS, _digest, hash_password, verify_and_upgrade
from app.catalog import CHAPTERS, MISCONCEPTIONS_DATABASE
from app.database import engine
from app.engine import dependants, update_profile
from app.generative_engine import generative_engine
from app.main import app
from app.seed import main as seed

client = TestClient(app)


def setup_module():
    seed()
    client.post("/api/demo/reset")


def teardown_module():
    engine.dispose()


def teacher():
    token = client.post("/api/auth/login", json={"email": "teacher@prism.demo", "password": "PrismDemo!2026"}).json()["access_token"]
    return {"authorization": f"Bearer {token}"}


def new_student(**extra):
    body = client.post("/api/auth/register", json={"name": "Test Learner", "email": f"{uuid.uuid4().hex}@x.io", "password": "Password123", "role": "student", **extra})
    assert body.status_code == 201, body.text
    data = body.json()
    return {"authorization": f"Bearer {data['access_token']}"}, data["user"]["student_code"]


def answer(headers, question_id, response, stage):
    result = client.post("/api/learning/attempts", json={"question_id": question_id, "response": response, "stage": stage, "submission_id": uuid.uuid4().hex}, headers=headers)
    assert result.status_code == 200, result.text
    return result.json()


# ---------------------------------------------------------------------------
# Answer Engine: never a wrong result marked verified, never a crash
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query,expected", [
    ("3x + 5 = 20", "x = 5"),
    ("2x + 3 = x + 5", "x = 2"),
    ("2(x + 3) = 10", "x = 2"),
    ("solve x + 5 = -2", "x = -7"),
    ("Find x if 2x + 3 = 7?", "x = 2"),
    ("x/10 = 3/5", "x = 6"),
    ("3x + 1 = 2", "x = 1/3"),
    ("5n = 75", "n = 15"),
    ("0x + 5 = 20", "No solution"),
    ("2x + 2 = 2x + 2", "Every value of x is a solution"),
])
def test_linear_equations_are_solved_exactly(query, expected):
    assert answer_engine.solve(query).direct_answer == expected


def test_non_perfect_cube_is_not_reported_as_exact():
    result = answer_engine.solve("cube root of 100")
    assert "Not a perfect cube" in result.direct_answer
    assert "4.642" in result.direct_answer


def test_equal_fractions_compare_as_equal():
    assert answer_engine.solve("compare 1/2 and 2/4").direct_answer.startswith("1/2 = 2/4")


def test_negative_fractions_compare_correctly():
    assert "-1/2 < -1/3" in answer_engine.solve("compare -1/2 and -1/3").direct_answer


@pytest.mark.parametrize("query", ["compare 1/0 and 1/2", "simplify 5/0", "1/0 = ?/4"])
def test_zero_denominators_are_undefined_not_a_crash(query):
    assert answer_engine.solve(query).direct_answer.startswith("Undefined")


def test_blank_in_equivalent_fraction_is_recognised():
    assert answer_engine.solve("3/5 = ?/10").direct_answer.startswith("6 ")


def test_unrecognised_question_is_not_presented_as_confident():
    result = answer_engine.solve("who is the prime minister")
    assert result.confidence == 0.0
    assert "could not solve" in result.direct_answer


def test_trap_warning_uses_the_actual_numbers():
    assert "5" not in answer_engine.solve("x + 7 = 19").misconception_warning


def test_impossible_quadrilateral_is_rejected():
    assert answer_engine.solve("Three angles of a quadrilateral are 200, 100, and 110").direct_answer.startswith("Impossible")


# ---------------------------------------------------------------------------
# Generative Engine
# ---------------------------------------------------------------------------

ALL_CONCEPTS = [chapter["concept"] for chapter in CHAPTERS]
KNOWN_TAGS = {entry["id"] for entry in MISCONCEPTIONS_DATABASE}


@pytest.mark.parametrize("concept", ALL_CONCEPTS)
def test_generated_questions_hold_their_invariants(concept):
    for stage in ("diagnostic", "practice", "test"):
        for difficulty in ("foundation", "standard", "challenge"):
            for _ in range(60):
                q = generative_engine.generate_question(concept, stage, difficulty)
                assert q["concept_id"] == concept
                assert len(set(q["options"])) == 4, q
                assert q["expected_answer"] in q["options"]
                assert q["expected_answer"] not in q["misconception_map"], q
                assert set(q["misconception_map"]) <= set(q["options"]), q
                assert set(q["misconception_map"].values()) <= KNOWN_TAGS, q


def test_generated_mean_questions_have_a_correct_answer():
    for _ in range(200):
        q = generative_engine.generate_question("data-handling", "practice", "standard")
        values = [int(v) for v in q["prompt"].removeprefix("Find the mean of ").rstrip(".").split(", ")]
        assert sum(values) / len(values) == int(q["expected_answer"])


@pytest.mark.parametrize("entry", MISCONCEPTIONS_DATABASE, ids=lambda e: e["id"])
def test_every_misconception_has_its_own_remediation(entry):
    guide = generative_engine.generate_remediation(entry["id"], "Asha")
    assert guide["misconception_id"] == entry["id"]
    assert guide["diagnostic_probe"]["correct_answer"] in guide["diagnostic_probe"]["options"]
    if entry["id"] != "denominator-magnitude":
        assert "Roti" not in guide["concrete_analogy"]


def test_unknown_misconception_is_a_404_not_the_fraction_guide():
    assert client.post("/api/generate/remediation", json={"misconception_id": "made-up"}).status_code == 404


@pytest.mark.parametrize("concept", [c for c in ALL_CONCEPTS if c != "equivalent-fractions"])
def test_lesson_plans_are_about_their_own_chapter(concept):
    text = str(generative_engine.generate_lesson_plan(concept, "8A-CBSE"))
    assert "1/3" not in text and "Fraction Bar" not in text


# ---------------------------------------------------------------------------
# Rules engine
# ---------------------------------------------------------------------------

def _tagged(*tags):
    return [{"correct": False, "misconception": tag, "stage": "diagnostic", "transfer": False} for tag in tags]


def test_tie_between_error_patterns_routes_to_the_teacher():
    result = update_profile(0.35, _tagged("additive-bias", "additive-bias", "unequal-operations", "unequal-operations"))
    assert result.misconception is None
    assert result.recommendation == "follow-up"


def test_routing_does_not_depend_on_the_hash_seed():
    script = (
        "from app.engine import update_profile;"
        "t=[{'correct':False,'misconception':m,'stage':'diagnostic'} for m in ('a-tag','a-tag','b-tag','b-tag')];"
        "r=update_profile(.35,t);print(r.misconception,r.recommendation)"
    )
    seen = set()
    for seed_value in range(6):
        env = {**os.environ, "PYTHONHASHSEED": str(seed_value)}
        seen.add(subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, env=env, check=True).stdout)
    assert len(seen) == 1


@pytest.mark.parametrize("tag,route", [
    ("unequal-operations", "guided-practice"),
    ("denominator-magnitude", "visual-support"),
    ("perfect-square-recognition", "foundation"),
    ("equation-setup-slip", "follow-up"),
])
def test_a_misconception_routes_to_its_own_remedy(tag, route):
    result = update_profile(0.35, _tagged(tag, tag))
    assert result.misconception == tag
    assert result.recommendation == route


def test_mastery_is_a_pure_function_of_the_attempt_log():
    items = _tagged("x") + [{"correct": True, "stage": "test", "transfer": True}]
    assert update_profile(0.35, items).mastery == update_profile(0.35, items).mastery == round(0.0875 + 0.75 * 1.4 / 2.4, 2)


def test_dependants_are_transitive():
    following = dependants("fraction-parts")
    assert following[:3] == ["fraction-magnitude", "simplification", "equivalent-fractions"]
    assert {"data-handling", "comparing-quantities"} <= set(following)


# ---------------------------------------------------------------------------
# Live learner journeys through the API
# ---------------------------------------------------------------------------

def test_foundation_route_is_reachable_by_a_new_learner():
    headers, _ = new_student()
    served = [q["id"] for q in client.get("/api/learning/units/rational-numbers/questions?stage=diagnostic", headers=headers).json()]
    assert "diag-representation" in served
    answer(headers, "diag-equivalent", "2/3", "diagnostic")
    answer(headers, "diag-magnitude", "1/3", "diagnostic")
    answer(headers, "diag-representation", "1/3", "diagnostic")  # prerequisite answered last
    rows = client.get("/api/learning/my-progress", headers=headers).json()
    chapter_one = next(r for r in rows if r["unit_id"] == "rational-numbers")
    assert chapter_one["prerequisite_status"] == "needs-check"
    assert chapter_one["recommendation"] == "foundation"


def test_explanations_are_not_sent_before_answering():
    headers, _ = new_student()
    question = client.get("/api/learning/units/linear-equations/questions?stage=diagnostic", headers=headers).json()[0]
    assert "explanation" not in question


def test_retrying_a_submission_never_scores_twice():
    headers, _ = new_student()
    body = {"question_id": "diag-magnitude", "response": "1/8", "stage": "diagnostic", "submission_id": uuid.uuid4().hex}
    first = client.post("/api/learning/attempts", json=body, headers=headers).json()
    second = client.post("/api/learning/attempts", json=body, headers=headers).json()
    assert first["duplicate"] is False and second["duplicate"] is True
    assert first["profile"]["evidence_count"] == 1
    rows = client.get("/api/learning/my-progress", headers=headers).json()
    assert next(r for r in rows if r["unit_id"] == "rational-numbers")["evidence_count"] == 1


def test_unknown_class_code_is_rejected_rather_than_created():
    response = client.post("/api/auth/register", json={"name": "Typo", "email": f"{uuid.uuid4().hex}@x.io", "password": "Password123", "role": "student", "classroom_code": "NOPE-123"})
    assert response.status_code == 404


def test_other_chapters_reach_the_teacher():
    headers, code = new_student(classroom_code="8A-CBSE")
    answer(headers, "linear-equations-diagnostic-1", "25", "diagnostic")
    answer(headers, "linear-equations-practice-2", "26", "practice")
    workspace = client.get("/api/teacher/workspace", headers=teacher()).json()
    learner = next(l for l in workspace["learners"] if l["code"] == code)
    assert learner["focus_unit"] == "linear-equations"
    assert learner["misconception"] == "sign-inversion-slip"
    assert learner["recommendation"] == "guided-practice"
    assert learner["mastery"] > 0

    plans = client.post("/api/teacher/interventions/recompile", headers=teacher()).json()
    pod = next(p for p in plans if code in p["student_codes"])
    assert pod["unit_id"] == "linear-equations"
    assert pod["barrier"] == "Sign Inversion & Balancing Error"
    assert "fraction" not in pod["activity"].lower()


def test_recompile_keeps_teacher_decisions_and_suggests_changes():
    t = teacher()
    client.post("/api/demo/reset")
    plans = client.get("/api/teacher/workspace", headers=t).json()["interventions"]
    visual = next(p for p in plans if p["group_key"] == "visual-support")
    client.put(f"/api/teacher/interventions/{visual['id']}", json={"status": "approved", "teacher_notes": "Seat near the board"}, headers=t)

    headers, code = new_student(classroom_code="8A-CBSE")
    answer(headers, "diag-magnitude", "1/8", "diagnostic")
    answer(headers, "test-transfer", "3/6", "test")

    after = client.post("/api/teacher/interventions/recompile", headers=t).json()
    kept = next(p for p in after if p["id"] == visual["id"])
    assert kept["status"] == "approved"
    assert kept["teacher_notes"] == "Seat near the board"
    assert code not in kept["student_codes"]
    assert code in kept["suggested_add"]


def test_one_click_approve_keeps_existing_notes():
    t = teacher()
    plan = client.get("/api/teacher/workspace", headers=t).json()["interventions"][0]
    client.put(f"/api/teacher/interventions/{plan['id']}", json={"status": "modified", "teacher_notes": "Keep me"}, headers=t)
    approved = client.put(f"/api/teacher/interventions/{plan['id']}", json={"status": "approved"}, headers=t).json()
    assert approved["teacher_notes"] == "Keep me"


def test_pod_confidence_reflects_evidence_not_group_size():
    plans = client.get("/api/teacher/workspace", headers=teacher()).json()["interventions"]
    assert next(p for p in plans if p["group_key"] == "extension")["confidence"] == "high"


# ---------------------------------------------------------------------------
# Access control
# ---------------------------------------------------------------------------

def other_teacher():
    data = client.post("/api/auth/register", json={"name": "Other Teacher", "email": f"{uuid.uuid4().hex}@x.io", "password": "Password123", "role": "teacher"}).json()
    return {"authorization": f"Bearer {data['access_token']}"}


def test_teacher_cannot_read_another_classrooms_student():
    assert client.get("/api/teacher/students/STU-VISUAL/detail", headers=other_teacher()).status_code == 404
    assert client.get("/api/teacher/students/STU-VISUAL/detail", headers=teacher()).status_code == 200


def test_teacher_cannot_assign_another_classrooms_student():
    t = other_teacher()
    headers, code = new_student(classroom_code=client.get("/api/teacher/workspace", headers=t).json()["class_code"])
    answer(headers, "diag-magnitude", "1/8", "diagnostic")
    plans = client.post("/api/teacher/interventions/recompile", headers=t).json()
    response = client.put(f"/api/teacher/interventions/{plans[0]['id']}", json={"status": "modified", "student_codes": ["STU-VISUAL"]}, headers=t)
    assert response.status_code == 404


@pytest.mark.parametrize("path", ["/api/demo", "/api/demo/personas"])
def test_demo_listings_are_closed_outside_demo_mode(monkeypatch, path):
    assert client.get(path).status_code == 200
    monkeypatch.setenv("PRISM_DEMO_MODE", "0")
    assert client.get(path).status_code == 404


def test_tampered_tokens_are_rejected_without_a_server_error():
    assert client.get("/api/auth/me", headers={"authorization": "Bearer abc.def"}).status_code == 401


def test_password_hash_uses_the_current_cost():
    assert PBKDF2_ITERATIONS == 600_000
    salt, stored = hash_password("Password123")
    assert verify_and_upgrade("Password123", salt, stored) == (True, None)
    assert verify_and_upgrade("wrong", salt, stored) == (False, None)


def test_old_password_hashes_still_work_and_upgrade():
    salt = "legacy-salt"
    old = _digest("Password123", salt, 210_000)
    matched, upgraded = verify_and_upgrade("Password123", salt, old)
    assert matched and upgraded == _digest("Password123", salt, PBKDF2_ITERATIONS)


def test_hindi_and_telugu_topic_names_find_results():
    from app.search_engine import search_engine

    for query in ("तुल्य भिन्न", "సమాన భిన్నాలు"):
        assert search_engine.search(query), query
