"""Teacher Intervention Compiler: turns a classroom's learner profiles into pods.

`engine.compile_groups` decides who belongs together. This module applies it per
chapter, gives each pod text that fits that chapter, and reconciles the engine's
latest view with decisions the teacher has already made. The teacher's decision
always wins: fresh evidence becomes a visible suggestion, never a silent overwrite.
"""
from __future__ import annotations

from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from .catalog import CHAPTERS, PREREQUISITE_SKILLS, concept_title, misconception_entry
from .engine import INTERVENTION_LIBRARY, compile_groups
from .models import Intervention, LearnerProgress, Student
from .scoring import prerequisite_gap

CHAPTER_BY_CONCEPT = {chapter["concept"]: chapter for chapter in CHAPTERS}
ROUTE_ORDER = ["foundation", "visual-support", "guided-practice", "follow-up", "test", "extension"]

# INTERVENTION_LIBRARY speaks about fractions, so it only fits Chapter 1. Other
# chapters use their misconception's remedy, or this text when no label exists yet.
GENERIC_ROUTE_TEXT = {
    "foundation": ("Revisit the basics of {chapter}", "Work through one simple example together, naming each step before the learner tries another.", "Learner can state the key idea of the chapter in their own words."),
    "visual-support": ("See it differently: {chapter}", "Draw or model the problem so the relationship is visible, then ask the learner to justify the answer.", "Learner connects the picture to the written method."),
    "guided-practice": ("Guided practice: {chapter}", "Pairs solve two structured problems, explaining each step to each other.", "Learner completes the method accurately with prompts removed."),
    "extension": ("Extension challenge: {chapter}", "Pose a harder problem in a real-life context and ask learners to justify their method.", "Learner applies the concept in a new context."),
    "test": ("Ready for a transfer check: {chapter}", "Give one unscaffolded problem in a new context and ask the learner to explain the method.", "Learner applies the concept independently in an unfamiliar setting."),
    "follow-up": ("Teacher conference: {chapter}", "Ask one contrast question and listen to the explanation before selecting a route.", "Teacher gathers enough evidence to choose an appropriate next step."),
}


def _dominant_tag(members) -> str | None:
    """The pod's most common label. Ties resolve alphabetically, so output is stable."""
    counts = Counter(m.misconception for m in members if m.misconception)
    if not counts:
        return None
    return min(counts, key=lambda tag: (-counts[tag], tag))


def _dominant_gap(members, gaps: dict) -> dict | None:
    """The prerequisite most members of a foundation pod are weak in."""
    found = [gaps[m.student_id] for m in members if gaps.get(m.student_id)]
    if not found:
        return None
    counts = Counter(gap["concept_id"] for gap in found)
    leader = min(counts, key=lambda concept: (-counts[concept], concept))
    return next(gap for gap in found if gap["concept_id"] == leader)


def _localise_plan(plan: dict, concept_id: str, members, gaps: dict | None = None) -> dict:
    gap = _dominant_gap(members, gaps or {}) if plan["group_key"] == "foundation" else None
    # The library's Chapter 1 foundation activity already covers fraction parts.
    if gap and not (concept_id == "equivalent-fractions" and gap["concept_id"] == "fraction-parts"):
        skill = PREREQUISITE_SKILLS.get(gap["concept_id"])
        plan.update(
            barrier=f"Prerequisite gap: {gap['title']}",
            activity=gap["remedy"],
            outcome=skill["objective"] if skill else f"Learner is ready to return to {concept_title(concept_id)}.",
        )
        return plan
    if concept_id == "equivalent-fractions":
        return plan
    chapter_title = CHAPTER_BY_CONCEPT[concept_id]["title"]
    entry = misconception_entry(_dominant_tag(members))
    if entry:
        plan.update(
            barrier=entry["title"],
            activity=entry["remedy"],
            outcome=f"Learner can explain and correct this error: {entry['title']}.",
        )
    else:
        barrier, activity, outcome = GENERIC_ROUTE_TEXT[plan["group_key"]]
        plan.update(barrier=barrier.format(chapter=chapter_title), activity=activity, outcome=outcome)
    return plan


def compile_classroom(db: Session, classroom_id: int) -> list[dict]:
    """The engine's current pods for every chapter with evidence, as Intervention fields."""
    students = db.scalars(select(Student).where(Student.classroom_id == classroom_id)).all()
    code_by_id = {student.id: student.code for student in students}
    if not code_by_id:
        return []
    rows = db.scalars(
        select(LearnerProgress).where(
            LearnerProgress.student_id.in_(code_by_id),
            LearnerProgress.evidence_count > 0,
        )
    ).all()

    by_student: dict[int, dict] = {}
    for row in rows:
        by_student.setdefault(row.student_id, {})[row.concept_id] = (row.mastery, row.evidence_count)

    plans: list[dict] = []
    for chapter in CHAPTERS:
        concept_id = chapter["concept"]
        profiles = [row for row in rows if row.concept_id == concept_id]
        for profile in profiles:
            profile.code = code_by_id[profile.student_id]
        id_by_code = {profile.code: profile.student_id for profile in profiles}
        for plan in compile_groups(profiles):
            members = [p for p in profiles if p.recommendation == plan["group_key"]]
            codes = plan.pop("students")
            gaps = {
                m.student_id: prerequisite_gap(by_student[m.student_id], concept_id)
                for m in members
                if m.prerequisite_status == "needs-check"
            }
            plan = _localise_plan(plan, concept_id, members, gaps)
            plans.append({**plan, "concept_id": concept_id, "student_ids": [id_by_code[c] for c in codes]})
    plans.sort(key=lambda p: (_chapter_number(p["concept_id"]), _route_rank(p["group_key"])))
    return plans


def recompile_classroom(db: Session, classroom_id: int) -> None:
    """Refresh pods from evidence without discarding any teacher decision.

    Only plans still `proposed` are replaced. An approved, modified or rejected plan
    is the teacher's work and stays exactly as they left it; `plan_out` shows how the
    engine's view has since diverged so they can choose to act on it.
    """
    existing = db.scalars(select(Intervention).where(Intervention.classroom_id == classroom_id)).all()
    decided = set()
    for record in existing:
        if record.status == "proposed":
            db.delete(record)
        else:
            decided.add((record.concept_id, record.group_key))
    db.flush()
    for plan in compile_classroom(db, classroom_id):
        if (plan["concept_id"], plan["group_key"]) not in decided:
            db.add(Intervention(classroom_id=classroom_id, **plan))
    db.flush()


def classroom_plans(db: Session, classroom_id: int) -> list[dict]:
    """Stored plans for the teacher's view, each carrying the engine's suggested changes."""
    records = db.scalars(select(Intervention).where(Intervention.classroom_id == classroom_id)).all()
    if not records:
        for plan in compile_classroom(db, classroom_id):
            db.add(Intervention(classroom_id=classroom_id, **plan))
        db.commit()
        records = db.scalars(select(Intervention).where(Intervention.classroom_id == classroom_id)).all()

    fresh = {(p["concept_id"], p["group_key"]): set(p["student_ids"]) for p in compile_classroom(db, classroom_id)}
    students = db.scalars(select(Student).where(Student.classroom_id == classroom_id)).all()
    code_by_id = {student.id: student.code for student in students}

    def codes(ids) -> list[str]:
        return sorted(code_by_id[i] for i in ids if i in code_by_id)

    output = []
    for record in sorted(records, key=lambda r: (_chapter_number(r.concept_id), _route_rank(r.group_key))):
        current = set(record.student_ids)
        latest = fresh.get((record.concept_id, record.group_key), set())
        chapter = CHAPTER_BY_CONCEPT.get(record.concept_id)
        output.append({
            "id": record.id,
            "group_key": record.group_key,
            "concept_id": record.concept_id,
            "unit_id": chapter["id"] if chapter else None,
            "chapter_number": chapter["number"] if chapter else None,
            "chapter_title": chapter["title"] if chapter else record.concept_id,
            "student_codes": [code_by_id[i] for i in record.student_ids if i in code_by_id],
            "suggested_add": codes(latest - current),
            "suggested_remove": codes(current - latest),
            "barrier": record.barrier,
            "evidence": record.evidence,
            "confidence": record.confidence,
            "activity": record.activity,
            "duration": record.duration,
            "outcome": record.outcome,
            "follow_up": record.follow_up,
            "status": record.status,
            "teacher_notes": record.teacher_notes,
        })
    return output


def _chapter_number(concept_id: str) -> int:
    chapter = CHAPTER_BY_CONCEPT.get(concept_id)
    return chapter["number"] if chapter else 99


def _route_rank(group_key: str) -> int:
    return ROUTE_ORDER.index(group_key) if group_key in ROUTE_ORDER else len(ROUTE_ORDER)


__all__ = ["INTERVENTION_LIBRARY", "classroom_plans", "compile_classroom", "recompile_classroom"]
