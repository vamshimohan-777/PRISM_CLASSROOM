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

from .engine import prerequisite_mastery_from, update_profile
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
    prerequisite = prerequisite_mastery_from(progress_map(db, student_id), concept_id)
    result = update_profile(INITIAL_MASTERY, evidence, prerequisite_mastery=prerequisite)
    row.mastery = result.mastery
    row.evidence_count = result.evidence_count
    row.recent_correct = sum(1 for item in evidence if item["correct"])
    row.misconception = result.misconception
    row.misconception_confidence = result.misconception_confidence
    row.prerequisite_status = result.prerequisite_status
    row.recommendation = result.recommendation
    db.flush()
    return result


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
    from .engine import ancestors

    # Topological-ish ordering: fewer prerequisites first.
    for concept_id in sorted(concept_ids, key=lambda c: len(ancestors(c))):
        recompute_concept(db, student_id, concept_id)
