"""Reproducible synthetic demo data. Run with `python -m app.seed`."""

from .auth import hash_password
from .catalog import CHAPTERS, QUESTION_BANK
from .curriculum import CBSE_CURRICULUM
from .database import Base, SessionLocal, engine
from .engine import compile_groups, update_profile, validate_graph
from .models import Attempt, Classroom, Concept, Intervention, LearnerProgress, Question, Student, Teacher, User

CONCEPTS = [
    (
        "fraction-parts",
        "Fraction parts",
        "Identify numerator, denominator, sign, and equal parts of a rational number.",
        [],
    ),
    (
        "fraction-magnitude",
        "Rational-number comparison",
        "Compare rational numbers using equal-sized wholes and sign.",
        ["fraction-parts"],
    ),
    (
        "simplification",
        "Standard form",
        "Write a rational number in standard form by dividing both terms by a common factor.",
        ["fraction-parts"],
    ),
    (
        "equivalent-fractions",
        "Equivalent rational numbers",
        "Generate, recognise, simplify, and apply equivalent rational numbers.",
        ["fraction-magnitude", "simplification"],
    ),
]
QUESTIONS = [
    (
        "diag-equivalent",
        "diagnostic",
        1,
        "Which fraction is equivalent to 1/2?",
        ["2/3", "2/4", "3/4", "1/4"],
        "2/4",
        "Multiplying the numerator and denominator of 1/2 by 2 gives 2/4.",
        {},
    ),
    (
        "diag-magnitude",
        "diagnostic",
        1,
        "Which is greater?",
        ["1/8", "1/3", "They are equal"],
        "1/3",
        "With the same numerator, the fraction with fewer equal parts is greater.",
        {"1/8": "denominator-magnitude"},
    ),
    (
        "diag-simplify",
        "diagnostic",
        2,
        "Write -18/24 in standard form.",
        ["-3/4", "3/4", "-9/12", "-18/12"],
        "-3/4",
        "Divide numerator and denominator by 6 and keep the negative sign: -18/24 = -3/4.",
        {"3/4": "sign-error", "-9/12": "incomplete-simplification", "-18/12": "unequal-operations"},
    ),
    (
        "diag-representation",
        "diagnostic",
        2,
        "A strip is split into 6 equal parts and 3 are shaded. Which matching fraction names the same amount?",
        ["1/2", "1/3", "2/3", "3/3"],
        "1/2",
        "Three of six equal parts is one half.",
        {"1/3": "fraction-parts-gap"},
    ),
    (
        "practice-guided",
        "practice",
        2,
        "Complete: 3/5 = __/10",
        ["5", "6", "7", "8"],
        "6",
        "Multiply both numerator and denominator by 2: 3/5 = 6/10.",
        {"5": "unequal-operations", "8": "additive-equivalence"},
    ),
    (
        "practice-standard",
        "practice",
        3,
        "Which pair names the same rational number?",
        ["4/6 and 6/8", "-3/4 and 6/-8", "2/5 and 4/15", "5/6 and 10/15"],
        "-3/4 and 6/-8",
        "A negative sign in either the numerator or denominator makes the rational number negative: 6/-8 = -3/4.",
        {"4/6 and 6/8": "additive-equivalence"},
    ),
    (
        "test-transfer",
        "test",
        3,
        "A recipe uses 2/3 cup of milk. Which amount is the same quantity in sixth-cup measures?",
        ["3/6", "4/6", "5/6", "2/6"],
        "4/6",
        "Multiply 2/3 by 2/2 to write it in sixths: 4/6.",
        {"3/6": "denominator-magnitude", "5/6": "additive-equivalence"},
    ),
]

LEARNERS = [
    ("STU-VISUAL", "Aarav Sharma", "student@prism.demo", "visual-support"),
    ("STU-FOUNDATION", "Diya Patel", "diya@prism.demo", "foundation"),
    ("STU-CALC", "Kabir Verma", "kabir@prism.demo", "guided-practice"),
    ("STU-EXTEND", "Meera Iyer", "meera@prism.demo", "extension"),
]
PRIOR_MASTERY = 0.35


def main():
    validate_graph()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    room = db.query(Classroom).filter_by(code="8A-CBSE").first()
    if not room:
        room = Classroom(code="8A-CBSE", grade=CBSE_CURRICULUM["grade"], curriculum="CBSE-aligned · NCERT reference")
        db.add(room)
        db.flush()
    teacher = db.query(Teacher).filter_by(demo_identity="TEACHER-PRISM").first()
    if not teacher:
        teacher = Teacher(demo_identity="TEACHER-PRISM", name="Ms. Ananya (Demo)", classroom_id=room.id)
        db.add(teacher)
        db.flush()
    seen_concepts = set()
    for cid, name, obj, pre in CONCEPTS:
        seen_concepts.add(cid)
        if not db.get(Concept, cid):
            db.add(Concept(id=cid, name=name, objective=obj, grade=8, prerequisites=pre))
    for chapter in CHAPTERS:
        cid = chapter["concept"]
        if cid in seen_concepts:
            continue
        seen_concepts.add(cid)
        if not db.get(Concept, cid):
            db.add(Concept(id=cid, name=chapter["title"], objective=chapter["summary"], grade=8, prerequisites=[]))
        for index, (stage, prompt, options, answer, explanation) in enumerate(QUESTION_BANK[chapter["id"]], start=1):
            question_id = f"{chapter['id']}-{stage}-{index}"
            if not db.get(Question, question_id):
                db.add(
                    Question(
                        id=question_id,
                        concept_id=chapter["concept"],
                        stage=stage,
                        difficulty=index,
                        prompt=prompt,
                        question_type="choice",
                        options=options,
                        expected_answer=answer,
                        explanation=explanation,
                        misconception_map={},
                        is_transfer=stage == "test",
                    )
                )
    for qid, stage, difficulty, prompt, options, answer, explanation, mapping in QUESTIONS:
        if not db.get(Question, qid):
            db.add(
                Question(
                    id=qid,
                    concept_id="equivalent-fractions",
                    stage=stage,
                    difficulty=difficulty,
                    prompt=prompt,
                    question_type="choice",
                    options=options,
                    expected_answer=answer,
                    explanation=explanation,
                    misconception_map=mapping,
                    is_transfer=stage == "test",
                )
            )
    # Name, login and intended route for each simulated learner. The route is
    # documentation only: the stored profile is always derived by the rules
    # engine from the seeded attempts (see derive_profiles), and
    # tests/test_prototype_evaluation.py checks that the two agree.
    for code, *_ in LEARNERS:
        s = db.query(Student).filter_by(code=code).first()
        if not s:
            s = Student(code=code, grade=8, language="en", classroom_id=room.id)
            db.add(s)
            db.flush()
        if not db.query(LearnerProgress).filter_by(student_id=s.id, concept_id="equivalent-fractions").first():
            db.add(LearnerProgress(student_id=s.id, concept_id="equivalent-fractions"))

    db.flush()
    seed_attempts(db)
    db.flush()
    derive_profiles(db)

    def demo_user(email, name, role, student_code=None, teacher_id=None):
        u = db.query(User).filter_by(email=email).first()
        if u:
            return
        salt, password_hash = hash_password("PrismDemo!2026")
        db.add(
            User(
                email=email,
                name=name,
                role=role,
                password_salt=salt,
                password_hash=password_hash,
                student_code=student_code,
                teacher_id=teacher_id,
            )
        )

    demo_user("student@prism.demo", "Aarav Sharma", "student", "STU-VISUAL")
    demo_user("diya@prism.demo", "Diya Patel", "student", "STU-FOUNDATION")
    demo_user("kabir@prism.demo", "Kabir Verma", "student", "STU-CALC")
    demo_user("meera@prism.demo", "Meera Iyer", "student", "STU-EXTEND")
    demo_user("teacher@prism.demo", "Ms. Ananya", "teacher", teacher_id=teacher.id)

    # Ensure initial interventions exist
    compile_initial_interventions(db, room.id)

    db.commit()
    db.close()


def seed_attempts(db):
    attempts_data = [
        (
            "STU-VISUAL",
            [
                ("diag-equivalent", "2/4", True, "diagnostic", "seed-sub-aarav-1"),
                ("diag-magnitude", "1/8", False, "diagnostic", "seed-sub-aarav-2"),
                ("diag-simplify", "-3/4", True, "diagnostic", "seed-sub-aarav-3"),
                ("test-transfer", "3/6", False, "test", "seed-sub-aarav-4"),
            ],
        ),
        (
            "STU-FOUNDATION",
            [
                ("diag-representation", "1/3", False, "diagnostic", "seed-sub-diya-1"),
                ("diag-equivalent", "2/3", False, "diagnostic", "seed-sub-diya-2"),
                ("diag-magnitude", "1/3", True, "diagnostic", "seed-sub-diya-3"),
            ],
        ),
        (
            "STU-CALC",
            [
                ("diag-equivalent", "2/4", True, "diagnostic", "seed-sub-kabir-1"),
                ("diag-magnitude", "1/3", True, "diagnostic", "seed-sub-kabir-2"),
                ("diag-simplify", "-9/12", False, "diagnostic", "seed-sub-kabir-3"),
                ("practice-guided", "5", False, "practice", "seed-sub-kabir-4"),
            ],
        ),
        (
            "STU-EXTEND",
            [
                ("diag-equivalent", "2/4", True, "diagnostic", "seed-sub-meera-1"),
                ("diag-magnitude", "1/3", True, "diagnostic", "seed-sub-meera-2"),
                ("diag-simplify", "-3/4", True, "diagnostic", "seed-sub-meera-3"),
                ("practice-guided", "6", True, "practice", "seed-sub-meera-4"),
                ("test-transfer", "4/6", True, "test", "seed-sub-meera-5"),
            ],
        ),
    ]
    for code, atts in attempts_data:
        stu = db.query(Student).filter_by(code=code).first()
        if not stu:
            continue
        for qid, resp, corr, stg, sub_id in atts:
            if not db.query(Attempt).filter_by(student_id=stu.id, submission_id=sub_id).first():
                db.add(
                    Attempt(
                        student_id=stu.id, question_id=qid, submission_id=sub_id, response=resp, correct=corr, stage=stg
                    )
                )


def evidence_for(db, student_id):
    """Turn stored attempts into the evidence format the rules engine expects."""
    attempts = (
        db.query(Attempt)
        .join(Question)
        .filter(Attempt.student_id == student_id, Question.concept_id == "equivalent-fractions")
        .order_by(Attempt.id)
        .all()
    )
    rows = []
    for a in attempts:
        q = db.get(Question, a.question_id)
        rows.append(
            {
                "correct": a.correct,
                "stage": a.stage,
                "transfer": q.is_transfer,
                "misconception": q.misconception_map.get(a.response),
            }
        )
    return rows


def derive_profiles(db):
    """Recompute every seeded learner profile from their attempts via the engine."""
    for code, *_ in LEARNERS:
        s = db.query(Student).filter_by(code=code).first()
        if not s:
            continue
        prog = db.query(LearnerProgress).filter_by(student_id=s.id, concept_id="equivalent-fractions").first()
        evidence = evidence_for(db, s.id)
        result = update_profile(PRIOR_MASTERY, evidence)
        prog.mastery, prog.evidence_count = result.mastery, result.evidence_count
        prog.recent_correct = sum(e["correct"] for e in evidence)
        prog.misconception, prog.misconception_confidence = result.misconception, result.misconception_confidence
        prog.prerequisite_status, prog.recommendation = result.prerequisite_status, result.recommendation


def compile_initial_interventions(db, classroom_id):
    records = db.query(Intervention).filter_by(classroom_id=classroom_id).all()
    if not records:
        students = db.query(Student).filter_by(classroom_id=classroom_id).all()
        profiles = []
        for s in students:
            p = db.query(LearnerProgress).filter_by(student_id=s.id, concept_id="equivalent-fractions").first()
            if p:
                p.code = s.code
                profiles.append(p)
        for plan in compile_groups(profiles):
            ids = [db.query(Student).filter_by(code=c).first().id for c in plan.pop("students")]
            db.add(Intervention(classroom_id=classroom_id, concept_id="equivalent-fractions", student_ids=ids, **plan))


def reset_to_seed(db):
    db.query(Attempt).delete()
    db.query(Intervention).delete()
    seed_attempts(db)
    db.flush()
    derive_profiles(db)
    room = db.query(Classroom).filter_by(code="8A-CBSE").first()
    if room:
        compile_initial_interventions(db, room.id)
    db.commit()


if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
