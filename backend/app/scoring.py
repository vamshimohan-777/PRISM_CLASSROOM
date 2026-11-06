"""Single source of truth for turning stored attempts into a learner profile.

Both the live attempt endpoints and the demo seed call `recompute_concept`, so
there is exactly one code path that can produce a `LearnerProgress` row. No
profile anywhere in the system is hand-written: every mastery score, every
misconception label and every route is derived from the `attempts` table by
`engine.update_profile`.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .catalog import concept_remedy, concept_title
from .engine import CHAPTER_CONCEPTS, PREREQUISITE_SECURE_AT, ancestors, dependants, update_profile, weakest_prerequisite
from .models import Attempt, LearnerProgress, Question

INITIAL_MASTERY = 0.35


def evidence_for(db: Session, student_id: int, concept_id: str) -> list[dict]:
    """Observable attempt evidence for one concept, oldest first."""
    rows = db.execute(
        select(Attempt, Question)
        .join(Question, Question.id == Attempt.question_id)
        .where(Attempt.student_id == student_id, Question.concept_id == concept_id)
        .order_by(Attempt.created_at, Attempt.id)
    ).all()
    return [
        {
            "correct": attempt.correct,
            "stage": attempt.stage,
            "transfer": question.is_transfer,
            "misconception": (question.misconception_map or {}).get(attempt.response),
        }
        for attempt, question in rows
    ]


def progress_map(db: Session, student_id: int) -> dict[str, tuple[float, int]]:
    """concept_id -> (mastery, evidence_count) for every concept the learner has touched."""
    rows = db.scalars(
        select(LearnerProgress).where(LearnerProgress.student_id == student_id)
    ).all()
    return {row.concept_id: (row.mastery, row.evidence_count) for row in rows}


def progress_row(db: Session, student_id: int, concept_id: str) -> LearnerProgress:
    row = db.scalar(
        select(LearnerProgress).where(
            LearnerProgress.student_id == student_id,
            LearnerProgress.concept_id == concept_id,
        )
    )
    if row is None:
        row = LearnerProgress(
            student_id=student_id,
            concept_id=concept_id,
            mastery=INITIAL_MASTERY,
            evidence_count=0,
            recommendation="diagnostic",
        )
        db.add(row)
        db.flush()
    return row


def recompute_concept(db: Session, student_id: int, concept_id: str):
    """Re-derive one concept profile from the learner's full attempt history.

    Prerequisite strength is read from the concept DAG: the weakest prerequisite
    the learner has actually attempted. Prerequisites with no evidence are
    reported as unknown rather than assumed weak or assumed secure.
    """
    row = progress_row(db, student_id, concept_id)
    evidence = evidence_for(db, student_id, concept_id)
    weakest = weakest_prerequisite(progress_map(db, student_id), concept_id)
    result = update_profile(
        INITIAL_MASTERY,
        evidence,
        prerequisite_mastery=weakest[1] if weakest else None,
        prerequisite_name=concept_title(weakest[0]) if weakest else None,
    )
    row.mastery = result.mastery
    row.evidence_count = result.evidence_count
    row.recent_correct = sum(1 for item in evidence if item["correct"])
    row.misconception = result.misconception
    row.misconception_confidence = result.misconception_confidence
    row.prerequisite_status = result.prerequisite_status
    row.recommendation = result.recommendation
    db.flush()
    return result


def prerequisite_gap(progress_by_concept: dict[str, tuple[float, int]], concept_id: str) -> dict | None:
    """Name the weak prerequisite behind a concept, if there is one."""
    weakest = weakest_prerequisite(progress_by_concept, concept_id)
    if not weakest or weakest[1] >= PREREQUISITE_SECURE_AT:
        return None
    return {
        "concept_id": weakest[0],
        "title": concept_title(weakest[0]),
        "remedy": concept_remedy(weakest[0]),
        "mastery": weakest[1],
    }


def recompute_after_attempt(db: Session, student_id: int, concept_id: str):
    """Re-derive a concept, then any concept that depends on it.

    A new answer on a prerequisite changes what its dependants should conclude, so
    those profiles must not wait for the learner's next answer on them to catch up.
    """
    result = recompute_concept(db, student_id, concept_id)
    touched = progress_map(db, student_id)
    decisive = None
    for dependant in dependants(concept_id):
        if touched.get(dependant, (0, 0))[1] > 0:
            updated = recompute_concept(db, student_id, dependant)
            # A skill check has no route of its own to act on: what the learner should
            # hear about is the nearest chapter that the answer just changed.
            if decisive is None and dependant in CHAPTER_CONCEPTS:
                decisive = updated
    return decisive if decisive is not None and concept_id not in CHAPTER_CONCEPTS else result


def recompute_student(db: Session, student_id: int) -> None:
    """Re-derive every concept the learner has evidence for, prerequisites first.

    Prerequisite nodes are recomputed before dependants so that a dependant sees
    up-to-date prerequisite mastery in the same pass.
    """
    concept_ids = list(
        db.scalars(
            select(Question.concept_id)
            .join(Attempt, Attempt.question_id == Question.id)
            .where(Attempt.student_id == student_id)
            .distinct()
        ).all()
    )
    # A concept's ancestors are a strict subset of its dependant's, so sorting by
    # ancestor count is a valid topological order.
    for concept_id in sorted(concept_ids, key=lambda c: len(ancestors(c))):
        recompute_concept(db, student_id, concept_id)
