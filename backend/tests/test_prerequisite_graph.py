"""The prerequisite graph must actually work in every chapter, not just exist."""
import os
import re
import uuid
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_prerequisite_graph.db")

import pytest
from fastapi.testclient import TestClient

from app.catalog import CHAPTERS, MISCONCEPTIONS_DATABASE, PREREQUISITE_QUESTIONS, PREREQUISITE_SKILLS
from app.database import SessionLocal, engine
from app.engine import CHAPTER_CONCEPTS, CONCEPT_GRAPH, ancestors, prerequisite_checks, validate_graph
from app.main import app
from app.models import Question
from app.seed import main as seed

client = TestClient(app)
CHAPTER_IDS = [chapter["id"] for chapter in CHAPTERS]
LOCALIZATION = (Path(__file__).parents[2] / "frontend" / "src" / "localization.ts").read_text(encoding="utf-8")


def setup_module():
    seed()


def teardown_module():
    engine.dispose()


def new_student():
    data = client.post("/api/auth/register", json={"name": "Graph Learner", "email": f"{uuid.uuid4().hex}@x.io", "password": "Password123", "role": "student"}).json()
    return {"authorization": f"Bearer {data['access_token']}"}


def answer(headers, question_id, response, stage):
    result = client.post("/api/learning/attempts", json={"question_id": question_id, "response": response, "stage": stage, "submission_id": uuid.uuid4().hex}, headers=headers)
    assert result.status_code == 200, result.text
    return result.json()


def chapter_row(headers, unit_id):
    return next(row for row in client.get("/api/learning/my-progress", headers=headers).json() if row["unit_id"] == unit_id)


def test_graph_is_valid():
    assert validate_graph() is True


@pytest.mark.parametrize("chapter", CHAPTERS, ids=lambda c: c["id"])
def test_every_chapter_has_a_prerequisite_it_can_measure(chapter):
    concept = chapter["concept"]
    assert concept in CONCEPT_GRAPH
    assert ancestors(concept), f"{concept} has no prerequisites"
    assert prerequisite_checks(concept), f"{concept} has no prerequisite skill of its own"


def test_every_graph_node_has_questions():
    db = SessionLocal()
    with_questions = {q.concept_id for q in db.query(Question).all()}
    db.close()
    assert not set(CONCEPT_GRAPH) - with_questions


def test_every_skill_is_registered_and_owned_by_a_real_chapter():
    skills = set(CONCEPT_GRAPH) - CHAPTER_CONCEPTS
    assert skills == set(PREREQUISITE_SKILLS)
    for skill in PREREQUISITE_SKILLS.values():
        assert skill["chapter_id"] in CHAPTER_IDS


@pytest.mark.parametrize("question", PREREQUISITE_QUESTIONS, ids=lambda q: q[0])
def test_prerequisite_questions_are_well_formed(question):
    qid, concept, prompt, options, answer_text, explanation, tags = question
    assert concept in PREREQUISITE_SKILLS
    assert answer_text in options
    assert answer_text not in tags
    assert set(tags) <= set(options)
    assert set(tags.values()) <= {entry["id"] for entry in MISCONCEPTIONS_DATABASE}
    assert prompt and explanation


@pytest.mark.parametrize("chapter", CHAPTERS, ids=lambda c: c["id"])
def test_chapter_serves_its_checks_but_not_other_chapters(chapter):
    headers = new_student()
    served = client.get(f"/api/learning/units/{chapter['id']}/questions?stage=diagnostic", headers=headers).json()
    concepts = {q["concept_id"] for q in served}
    assert concepts & set(prerequisite_checks(chapter["concept"]))
    assert concepts & CHAPTER_CONCEPTS == {chapter["concept"]}
    # Chapter questions come first, so the prerequisite checks close the diagnostic.
    kinds = [q["id"].startswith("prereq-") or q["id"] == "diag-representation" for q in served if q["id"] != "diag-representation"]
    assert kinds == sorted(kinds)


def weak_setup():
    """(chapter id, its wrong prerequisite answers, one wrong and one right chapter answer)."""
    return [
        ("rational-numbers", [("prereq-simplify", "6/8")], [("diag-equivalent", "2/3", "diagnostic"), ("diag-magnitude", "1/3", "diagnostic")]),
        ("linear-equations", [("prereq-inverse", "16")], [("linear-equations-diagnostic-1", "3", "diagnostic"), ("linear-equations-diagnostic-4", "7", "diagnostic")]),
        ("quadrilaterals", [("prereq-triangle", "230°")], [("quadrilaterals-diagnostic-1", "180°", "diagnostic"), ("quadrilaterals-diagnostic-4", "5", "diagnostic")]),
        ("practical-geometry", [("prereq-ruler", "9 cm")], [("practical-geometry-diagnostic-1", "ruler", "diagnostic"), ("practical-geometry-diagnostic-4", "5 measurements (sides and angles)", "diagnostic")]),
        ("data-handling", [("prereq-data", "3")], [("data-handling-diagnostic-1", "1/4", "diagnostic"), ("data-handling-diagnostic-4", "90°", "diagnostic")]),
        ("squares-roots", [("prereq-factors", "4 × 9")], [("squares-roots-diagnostic-1", "18", "diagnostic"), ("squares-roots-diagnostic-4", "13", "diagnostic")]),
        ("cubes-roots", [("prereq-repeated", "9")], [("cubes-roots-diagnostic-1", "16", "diagnostic"), ("cubes-roots-diagnostic-4", "8", "diagnostic")]),
        ("comparing-quantities", [("prereq-percent", "50")], [("comparing-quantities-diagnostic-1", "1/5", "diagnostic"), ("comparing-quantities-diagnostic-4", "30%", "diagnostic")]),
    ]


@pytest.mark.parametrize("unit_id,prereq,chapter_answers", weak_setup(), ids=[row[0] for row in weak_setup()])
def test_weak_prerequisite_routes_to_foundation_in_every_chapter(unit_id, prereq, chapter_answers):
    headers = new_student()
    for question_id, response, stage in chapter_answers:
        answer(headers, question_id, response, stage)
    for question_id, response in prereq:  # answered last, as the learner meets them
        answer(headers, question_id, response, "diagnostic")
    row = chapter_row(headers, unit_id)
    assert row["prerequisite_status"] == "needs-check"
    assert row["recommendation"] == "foundation"
    assert row["prerequisite_gap"]["concept_id"] in PREREQUISITE_SKILLS
    assert row["prerequisite_gap"]["remedy"]


def test_answering_a_skill_check_reports_the_chapter_route_it_changed():
    headers = new_student()
    answer(headers, "squares-roots-diagnostic-1", "18", "diagnostic")
    answer(headers, "squares-roots-diagnostic-4", "13", "diagnostic")
    result = answer(headers, "prereq-factors", "4 × 9", "diagnostic")
    assert result["route"] == "foundation"
    assert "Prime factorisation" in result["reason"]


def test_a_strong_prerequisite_is_reported_as_secure():
    headers = new_student()
    answer(headers, "prereq-inverse", "4", "diagnostic")
    answer(headers, "linear-equations-diagnostic-1", "5", "diagnostic")
    row = chapter_row(headers, "linear-equations")
    assert row["prerequisite_status"] == "secure"
    assert row["prerequisite_gap"] is None


def test_weak_earlier_chapter_flows_into_later_chapter():
    headers = new_student()
    answer(headers, "comparing-quantities-diagnostic-1", "1/5", "diagnostic")
    answer(headers, "comparing-quantities-diagnostic-4", "30%", "diagnostic")
    assert chapter_row(headers, "comparing-quantities")["prerequisite_status"] == "unknown"
    # Now Chapter 1 evidence arrives, weak. Chapter 8 must update without a new answer there.
    answer(headers, "diag-equivalent", "2/3", "diagnostic")
    row = chapter_row(headers, "comparing-quantities")
    assert row["prerequisite_status"] == "needs-check"
    assert row["recommendation"] == "foundation"
    assert row["prerequisite_gap"]["title"] == "Rational Numbers"


def test_foundation_pod_names_the_gap_for_the_teacher():
    token = client.post("/api/auth/login", json={"email": "teacher@prism.demo", "password": "PrismDemo!2026"}).json()["access_token"]
    teacher = {"authorization": f"Bearer {token}"}
    headers = new_student()
    answer(headers, "squares-roots-diagnostic-1", "18", "diagnostic")
    answer(headers, "squares-roots-diagnostic-4", "13", "diagnostic")
    answer(headers, "prereq-factors", "4 × 9", "diagnostic")
    plans = client.post("/api/teacher/interventions/recompile", headers=teacher).json()
    pod = next(p for p in plans if p["unit_id"] == "squares-roots" and p["group_key"] == "foundation")
    assert pod["barrier"] == "Prerequisite gap: Prime factorisation"
    assert "factor tree" in pod["activity"]


def test_curriculum_publishes_the_graph_for_all_chapters():
    graph = client.get("/api/curriculum").json()["prerequisite_graph"]
    assert [row["unit_id"] for row in graph] == CHAPTER_IDS
    assert all(row["skills"] for row in graph)
    by_unit = {row["unit_id"]: row for row in graph}
    assert [c["id"] for c in by_unit["cubes-roots"]["chapters"]] == ["squares-roots"]


def test_every_served_question_has_a_translated_prompt():
    db = SessionLocal()
    ids = [q.id for q in db.query(Question).all()]
    db.close()
    missing = [qid for qid in ids if f"'{qid}': {{" not in LOCALIZATION]
    assert not missing, missing


def test_translated_prompts_include_hindi_and_telugu():
    for qid, *_ in PREREQUISITE_QUESTIONS:
        block = re.search(rf"'{qid}': \{{(.*?)\n  \}},", LOCALIZATION, re.S).group(1)
        assert re.search(r"[ऀ-ॿ]", block), qid
        assert re.search(r"[ఀ-౿]", block), qid
