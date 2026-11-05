"""Unit and integration tests for PRISM Search, Answer, and Generative Engines."""
import pytest
from app.main import (
    search_post,
    search_get,
    search_suggestions,
    answer_post,
    answer_get,
    generate_question_endpoint,
    generate_remediation_endpoint,
    generate_lesson_plan_endpoint,
    generate_transfer_task_endpoint,
)
from app.schemas import (
    SearchQueryIn,
    AnswerQueryIn,
    GenerateQuestionIn,
    GenerateRemediationIn,
    GenerateLessonPlanIn,
    GenerateTransferIn,
)
from app.search_engine import search_engine
from app.answer_engine import answer_engine
from app.generative_engine import generative_engine

# =============================================================================
# 1. SEARCH ENGINE TESTS
# =============================================================================

def test_search_engine_basic_query():
    results = search_engine.search("fraction")
    assert len(results) > 0
    # Should find chapters, questions, and concepts related to fractions
    types = {r.type for r in results}
    assert "chapter" in types or "concept" in types or "question" in types

def test_search_engine_misconception_lookup():
    results = search_engine.search("denominator magnitude", entity_type="misconception")
    assert len(results) >= 1
    top = results[0]
    assert top.type == "misconception"
    assert "denominator" in top.title.lower() or "denominator" in top.snippet.lower()
    assert top.relevance_score > 0

def test_search_engine_filtering_by_type():
    results = search_engine.search("linear", entity_type="chapter")
    for r in results:
        assert r.type == "chapter"

def test_search_engine_filtering_by_chapter():
    results = search_engine.search("angle", chapter_id="quadrilaterals")
    for r in results:
        assert r.chapter_id == "quadrilaterals"

def test_search_engine_suggestions():
    suggs = search_engine.get_suggestions("linear")
    assert len(suggs) > 0
    assert any("linear" in s.lower() for s in suggs)


# =============================================================================
# 2. ANSWER ENGINE TESTS
# =============================================================================

def test_answer_engine_linear_equation():
    res = answer_engine.solve("Solve: 3x + 5 = 20")
    assert res.direct_answer == "x = 5"
    assert len(res.steps) >= 2
    assert "LHS" in res.verification or "5" in res.verification
    assert "Trap Alert" in res.misconception_warning
    assert res.practice_challenge["correct_answer"] == "4"

def test_answer_engine_linear_equation_subtraction():
    res = answer_engine.solve("Solve 2x - 7 = 15")
    assert res.direct_answer == "x = 11"
    assert any("Add 7" in s["title"] for s in res.steps)

def test_answer_engine_fraction_comparison():
    res = answer_engine.solve("Compare 1/3 and 1/8")
    assert "1/3 > 1/8" in res.direct_answer
    assert "Denominator-Magnitude" in res.misconception_warning
    assert len(res.steps) >= 2

def test_answer_engine_fraction_simplification():
    res = answer_engine.solve("Simplify 18/24")
    assert res.direct_answer == "3/4"
    assert "HCF" in res.steps[0]["title"] or "Common Factor" in res.steps[0]["title"]

def test_answer_engine_square_roots():
    res = answer_engine.solve("What is the square root of 144?")
    assert res.direct_answer == "√144 = 12"
    assert "Halving Fallacy" in res.misconception_warning

def test_answer_engine_percentages():
    res = answer_engine.solve("Find 10% discount on ₹500")
    assert "Discount = ₹50" in res.direct_answer
    assert "Sale Price = ₹450" in res.direct_answer

def test_answer_engine_quadrilaterals():
    res = answer_engine.solve("Three angles of a quadrilateral are 90°, 85°, and 110°. What is the fourth?")
    assert res.direct_answer == "75°"
    assert "360°" in res.verification

def test_answer_engine_mean():
    res = answer_engine.solve("Find the mean of 4, 6, and 8")
    assert res.direct_answer == "Mean = 6"


# =============================================================================
# 3. GENERATIVE ENGINE TESTS
# =============================================================================

def test_generative_question_fractions():
    q = generative_engine.generate_question("equivalent-fractions", stage="practice", difficulty="standard")
    assert len(q["options"]) == 4
    assert q["expected_answer"] in q["options"]
    assert len(q["explanation"]) > 10
    assert len(q["misconception_map"]) > 0

def test_generative_question_linear():
    q = generative_engine.generate_question("linear-equations", stage="practice", difficulty="standard")
    assert "Solve for x" in q["prompt"]
    assert q["expected_answer"] in q["options"]
    assert "sign-inversion-slip" in q["misconception_map"].values() or "forgot-division-slip" in q["misconception_map"].values()

def test_generative_question_squares():
    q = generative_engine.generate_question("squares-roots", stage="practice", difficulty="standard")
    assert "square root" in q["prompt"].lower() or "√" in q["prompt"]
    assert q["expected_answer"] in q["options"]

def test_generative_remediation_guide():
    guide = generative_engine.generate_remediation("denominator-magnitude", student_name="Aarav")
    assert guide["student_name"] == "Aarav"
    assert "Roti" in guide["concrete_analogy"] or "Cake" in guide["concrete_analogy"]
    assert len(guide["guided_steps"]) == 3
    assert guide["diagnostic_probe"]["correct_answer"] == "1/2"

def test_generative_lesson_plan():
    plan = generative_engine.generate_lesson_plan("equivalent-fractions", "8A-CBSE")
    assert plan["duration_minutes"] == 45
    assert len(plan["timeline"]) >= 4
    assert "Visual Support Pod" in str(plan["timeline"])

def test_generative_transfer_task():
    task = generative_engine.generate_transfer_task("equivalent-fractions", theme="recipes")
    assert "Diwali" in task["title"]
    assert len(task["ingredients"]) > 0
    assert len(task["solution_steps"]) > 0


# =============================================================================
# 4. API ENDPOINTS INTEGRATION TESTS
# =============================================================================

def test_api_search_endpoint():
    res = search_post(SearchQueryIn(query="fraction", limit=5))
    assert res["total_results"] > 0
    assert "results" in res

def test_api_search_suggestions_endpoint():
    res = search_suggestions("linear")
    assert "suggestions" in res

def test_api_answer_endpoint():
    res = answer_post(AnswerQueryIn(query="Solve 3x + 5 = 20"))
    assert res["direct_answer"] == "x = 5"
    assert len(res["steps"]) >= 2
    assert "verification" in res

def test_api_generate_question_endpoint():
    res = generate_question_endpoint(
        GenerateQuestionIn(
            concept_id="linear-equations",
            stage="practice",
            difficulty="standard"
        )
    )
    assert len(res["options"]) == 4
    assert res["expected_answer"] in res["options"]

def test_api_generate_remediation_endpoint():
    res = generate_remediation_endpoint(
        GenerateRemediationIn(
            misconception_id="denominator-magnitude",
            student_name="Aarav Sharma"
        )
    )
    assert res["student_name"] == "Aarav Sharma"
    assert "concrete_analogy" in res

def test_api_generate_lesson_plan_endpoint():
    res = generate_lesson_plan_endpoint(
        GenerateLessonPlanIn(
            concept_id="equivalent-fractions",
            classroom_code="8A-CBSE"
        )
    )
    assert res["duration_minutes"] == 45
    assert len(res["timeline"]) > 0

def test_api_generate_transfer_task_endpoint():
    res = generate_transfer_task_endpoint(
        GenerateTransferIn(
            concept_id="equivalent-fractions",
            theme="recipes"
        )
    )
    assert "Diwali" in res["title"]
    assert len(res["ingredients"]) > 0
    assert len(res["solution_steps"]) > 0
