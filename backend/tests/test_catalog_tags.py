"""Structural guards for the chapter question bank's misconception tags.

A tag that names an option which does not exist, or which names the correct
answer, would silently never fire (or would label a correct learner). These
tests make such a mistake a build failure rather than a dead diagnosis.
"""
import pytest

from app.catalog import CHAPTERS, MISCONCEPTION_TAGS, QUESTION_BANK


def generated_questions():
    """Mirror the id scheme and payload that seed.py writes to the database."""
    for chapter in CHAPTERS:
        for position, (stage, prompt, options, answer, _explanation) in enumerate(
            QUESTION_BANK[chapter["id"]], start=1
        ):
            yield f'{chapter["id"]}-{stage}-{position}', options, answer, prompt


QUESTIONS = list(generated_questions())
QUESTION_IDS = {qid for qid, _, _, _ in QUESTIONS}


def test_every_chapter_has_a_question_bank():
    for chapter in CHAPTERS:
        assert QUESTION_BANK.get(chapter["id"]), f'{chapter["id"]} has no questions'


def test_tag_keys_all_reference_a_real_question():
    unknown = set(MISCONCEPTION_TAGS) - QUESTION_IDS
    assert not unknown, f"tags reference non-existent question ids: {sorted(unknown)}"


@pytest.mark.parametrize("qid,options,answer,prompt", QUESTIONS, ids=[q[0] for q in QUESTIONS])
def test_tagged_options_exist_and_are_wrong(qid, options, answer, prompt):
    tags = MISCONCEPTION_TAGS.get(qid, {})
    for option, label in tags.items():
        assert option in options, f"{qid}: tagged option {option!r} is not one of {options}"
        assert option != answer, f"{qid}: tagged option {option!r} is the correct answer"
        assert label and label.strip() == label, f"{qid}: malformed misconception id {label!r}"


@pytest.mark.parametrize("qid,options,answer,prompt", QUESTIONS, ids=[q[0] for q in QUESTIONS])
def test_expected_answer_is_one_of_the_options(qid, options, answer, prompt):
    assert answer in options, f"{qid}: expected answer {answer!r} missing from {options}"


def test_every_chapter_can_diagnose_at_least_one_misconception():
    """Diagnosis must not be Chapter-1-only."""
    for chapter in CHAPTERS:
        tagged = sum(
            len(MISCONCEPTION_TAGS.get(qid, {}))
            for qid, _, _, _ in QUESTIONS
            if qid.startswith(chapter["id"] + "-")
        )
        assert tagged > 0, f'{chapter["id"]} cannot diagnose any misconception'


def test_tag_vocabulary_is_registered_in_the_misconception_database():
    """Every tag the engine can emit must be explainable to a teacher."""
    from app.search_engine import MISCONCEPTIONS_DATABASE

    known = {entry["id"] for entry in MISCONCEPTIONS_DATABASE}
    used = {label for tags in MISCONCEPTION_TAGS.values() for label in tags.values()}
    missing = used - known
    assert not missing, f"misconception ids with no database entry: {sorted(missing)}"
