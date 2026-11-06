import secrets
import os
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from .database import Base, engine, get_db
from .models import Student, Teacher, User, Question, Attempt, LearnerProgress, Classroom, Intervention
from .schemas import (
    AttemptIn,
    InterventionDecision,
    LoginIn,
    RegisterIn,
    JoinClassroomIn,
    SearchQueryIn,
    AnswerQueryIn,
    GenerateQuestionIn,
    GenerateRemediationIn,
    GenerateLessonPlanIn,
    GenerateTransferIn,
)
from .engine import CHAPTER_CONCEPTS, CONCEPT_GRAPH, prerequisite_checks, validate_graph
from .scoring import prerequisite_gap, progress_map, recompute_after_attempt
from .compiler import CHAPTER_BY_CONCEPT, classroom_plans, recompile_classroom
from .search_engine import search_engine
from .answer_engine import answer_engine
from .generative_engine import generative_engine
from .curriculum import CBSE_CURRICULUM
from .catalog import CHAPTERS, chapter_for, concept_title, misconception_entry
from .auth import create_token, hash_password, read_token, verify_and_upgrade
from .config import demo_mode

validate_graph()
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="PRISM Classroom API",
    version="1.0.0",
    description=(
        "**PRISM Classroom** — Misconception-aware adaptive learning API for Indian schools.\n\n"
        "Backed by a deterministic rules engine + validated prerequisite DAG. "
        "Learner routing is 100% reproducible and model-free. The optional Gemini fallback in the "
        "Answer Engine is disabled unless GEMINI_API_KEY is set, and never affects routing.\n\n"
        "**Track:** EdTech / Adaptive Learning · Code Kernel '26 · Decode Round\n\n"
        "**Demo credentials (all):** `PrismDemo!2026`\n\n"
        "| Persona | Email | Role |\n"
        "|---|---|---|\n"
        "| Aarav Sharma (Misconception) | student@prism.demo | student |\n"
        "| Diya Patel (Foundation Gap) | diya@prism.demo | student |\n"
        "| Kabir Verma (Calc Slips) | kabir@prism.demo | student |\n"
        "| Meera Iyer (High Mastery) | meera@prism.demo | student |\n"
        "| Ms. Ananya (Teacher) | teacher@prism.demo | teacher |\n"
    ),
)
origins_env = os.getenv("CORS_ORIGINS", "")
allowed_origins = [o.strip() for o in origins_env.split(",") if o.strip()] or [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# The previous default trusted every host on netlify.app and onrender.com --
# shared domains anyone can deploy to -- while also allowing credentials. The
# unified container serves the SPA same-origin and needs no cross-origin grant
# at all, so a split deployment must now name its frontend explicitly via
# CORS_ORIGINS, or opt into a pattern via CORS_ORIGIN_REGEX.
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=os.getenv("CORS_ORIGIN_REGEX") or None,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["authorization", "content-type", "x-demo-teacher"],
    allow_credentials=False,
)

def current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    payload = read_token(authorization)
    user = db.get(User, payload["sub"])
    if not user or user.role != payload["role"]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Your session is no longer valid")
    return user

def require_student(user: User = Depends(current_user)) -> User:
    if user.role != "student" or not user.student_code:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This area is available to student accounts")
    return user

def require_teacher(user: User = Depends(current_user)) -> User:
    if user.role != "teacher" or not user.teacher_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This area is available to teacher accounts")
    return user

def require_demo_mode() -> None:
    """Block demo-only, credential-free endpoints on a real deployment."""
    if not demo_mode():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")

def student_for(code: str, db: Session):
    student = db.scalar(select(Student).where(Student.code == code))
    if not student: raise HTTPException(404, "Student not found")
    return student

def question_out(q: Question):
    # The explanation is withheld here and sent only after an attempt: it usually
    # states the answer, so including it would let anyone read answers off the wire.
    return {"id":q.id, "concept_id":q.concept_id, "stage":q.stage, "difficulty":q.difficulty, "prompt":q.prompt, "type":q.question_type, "options":q.options, "is_transfer":q.is_transfer}

def progress_out(p: LearnerProgress, code="", progress_by_concept=None):
    entry = misconception_entry(p.misconception)
    gap = prerequisite_gap(progress_by_concept, p.concept_id) if progress_by_concept is not None and p.prerequisite_status == "needs-check" else None
    return {"prerequisite_gap":gap, "student_code":code, "concept_id":p.concept_id, "mastery":p.mastery, "evidence_count":p.evidence_count, "misconception":p.misconception, "misconception_title":entry["title"] if entry else None, "misconception_remedy":entry["remedy"] if entry else None, "misconception_confidence":p.misconception_confidence, "prerequisite_status":p.prerequisite_status, "recommendation":p.recommendation, "provisional":True}

@app.get("/api/health", tags=["System"], summary="Service health probe")
def health(): return {"status":"ok"}

@app.post("/api/auth/login", tags=["Authentication"], summary="Sign in and receive JWT token")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.strip().lower()))
    matched, upgraded_hash = verify_and_upgrade(payload.password, user.password_salt, user.password_hash) if user else (False, None)
    if not matched:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email or password is incorrect")
    if upgraded_hash:
        user.password_hash = upgraded_hash
        db.commit()
    return {"access_token": create_token(user.id, user.role), "token_type": "bearer", "user": user_out(user)}

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")
    salt, password_hash = hash_password(payload.password)
    if payload.role == "teacher":
        classroom = Classroom(code=f"CLASS-{secrets.token_hex(3).upper()}", grade=8, curriculum="CBSE-aligned · NCERT reference")
        db.add(classroom); db.flush()
        teacher = Teacher(demo_identity=f"TEACHER-{secrets.token_hex(4).upper()}", name=payload.name.strip(), classroom_id=classroom.id)
        db.add(teacher); db.flush()
        user = User(email=email, name=payload.name.strip(), role="teacher", password_salt=salt, password_hash=password_hash, teacher_id=teacher.id)
    else:
        requested = (payload.classroom_code or "").strip().upper()
        target_code = requested or "8A-CBSE"
        room = db.scalar(select(Classroom).where(Classroom.code == target_code))
        if not room and requested:
            # A mistyped code used to create an empty classroom no teacher could see.
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"No classroom found with code '{requested}'. Check it with your teacher.")
        if not room:
            room = Classroom(code=target_code, grade=8, curriculum="CBSE-aligned · NCERT reference"); db.add(room); db.flush()
        code = f"STU-{secrets.token_hex(4).upper()}"
        db.add(Student(code=code, grade=8, language="en", classroom_id=room.id))
        user = User(email=email, name=payload.name.strip(), role="student", password_salt=salt, password_hash=password_hash, student_code=code)
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_token(user.id, user.role), "token_type": "bearer", "user": user_out(user)}

@app.get("/api/auth/me")
def me(user: User = Depends(current_user)):
    return user_out(user)

def user_out(user: User):
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role, "student_code": user.student_code}

@app.get("/api/curriculum")
def curriculum():
    """The declared board framework, with each chapter's prerequisites."""
    return {
        **CBSE_CURRICULUM,
        "prerequisite_graph": [
            {
                "unit_id": chapter["id"],
                "number": chapter["number"],
                "title": chapter["title"],
                "concept": chapter["concept"],
                "skills": [{"id": node, "title": concept_title(node)} for node in prerequisite_checks(chapter["concept"])],
                "chapters": [
                    {"id": node, "title": concept_title(node)}
                    for node in CONCEPT_GRAPH[chapter["concept"]]
                    if node in CHAPTER_CONCEPTS
                ],
            }
            for chapter in CHAPTERS
        ],
    }

@app.get("/api/learning/units")
def learning_units():
    return CHAPTERS

def progress_for(student_id: int, concept_id: str, db: Session) -> LearnerProgress:
    progress = db.scalar(select(LearnerProgress).where(LearnerProgress.student_id == student_id, LearnerProgress.concept_id == concept_id))
    if progress:
        return progress
    progress = LearnerProgress(student_id=student_id, concept_id=concept_id, mastery=0, evidence_count=0, recommendation="diagnostic")
    db.add(progress); db.flush()
    return progress

@app.get("/api/learning/my-progress")
def my_progress(user: User = Depends(require_student), db: Session = Depends(get_db)):
    student = student_for(user.student_code, db)
    rows = []
    known = progress_map(db, student.id)
    for unit in CHAPTERS:
        progress = progress_for(student.id, unit["concept"], db)
        rows.append({"unit_id": unit["id"], **progress_out(progress, student.code, known)})
    db.commit()
    return rows

@app.get("/api/learning/units/{unit_id}/questions")
def unit_questions(unit_id: str, stage: str, user: User = Depends(require_student), db: Session = Depends(get_db)):
    unit = chapter_for(unit_id)
    if not unit or stage not in {"diagnostic", "practice", "test"}:
        raise HTTPException(404, "Learning activity not found")
    # A chapter also asks about its own prerequisite skills. Without this no learner
    # could produce prerequisite evidence, and the foundation route would only be
    # reachable from seeded data. Chapter questions come first, then the checks.
    concepts = [unit["concept"], *prerequisite_checks(unit["concept"])]
    questions = db.scalars(select(Question).where(Question.concept_id.in_(concepts), Question.stage == stage).order_by(Question.id)).all()
    return [question_out(q) for q in sorted(questions, key=lambda q: q.id.startswith("prereq-"))]

def record_attempt(db: Session, student: Student, payload: AttemptIn) -> dict:
    """Grade, store and derive from one attempt. Safe to call twice with one submission_id.

    The read below handles an ordinary retry. Two truly simultaneous retries can both
    pass it, in which case the UNIQUE(student_id, submission_id) constraint rejects the
    second insert and it is answered as the duplicate it is.
    """
    question = db.get(Question, payload.question_id)
    if not question or question.stage != payload.stage:
        raise HTTPException(422, "Question does not belong to this activity")
    existing = db.scalar(select(Attempt).where(Attempt.student_id == student.id, Attempt.submission_id == payload.submission_id))
    if existing:
        return {"saved": True, "duplicate": True, "correct": existing.correct, "feedback": "This response was already saved."}
    correct = payload.response.strip().lower().replace(" ", "") == question.expected_answer.lower().replace(" ", "")
    db.add(Attempt(student_id=student.id, question_id=question.id, submission_id=payload.submission_id, response=payload.response, correct=correct, stage=payload.stage))
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        existing = db.scalar(select(Attempt).where(Attempt.student_id == student.id, Attempt.submission_id == payload.submission_id))
        return {"saved": True, "duplicate": True, "correct": existing.correct if existing else correct, "feedback": "This response was already saved."}
    result = recompute_after_attempt(db, student.id, question.concept_id)
    progress = progress_for(student.id, question.concept_id, db)
    db.commit()
    return {
        "saved": True,
        "duplicate": False,
        "correct": correct,
        "feedback": question.explanation if correct else "Not quite. Review the explanation and continue with the next activity.",
        "explanation": question.explanation,
        "profile": progress_out(progress, student.code, progress_map(db, student.id)),
        "reason": result.reason,
        "route": result.recommendation,
    }

@app.post("/api/learning/attempts")
def learning_attempt(payload: AttemptIn, user: User = Depends(require_student), db: Session = Depends(get_db)):
    return record_attempt(db, student_for(user.student_code, db), payload)

@app.post("/api/students/join-classroom", tags=["Student"], summary="Enroll into a classroom using teacher's class code")
def join_classroom(payload: JoinClassroomIn, user: User = Depends(require_student), db: Session = Depends(get_db)):
    student = student_for(user.student_code, db)
    room = db.scalar(select(Classroom).where(Classroom.code == payload.classroom_code.strip().upper()))
    if not room:
        raise HTTPException(404, f"Classroom with code '{payload.classroom_code}' not found")
    student.classroom_id = room.id
    db.commit()
    teacher = db.scalar(select(Teacher).where(Teacher.classroom_id == room.id))
    return {
        "status": "joined",
        "classroom_code": room.code,
        "curriculum": room.curriculum,
        "teacher_name": teacher.name if teacher else "Classroom Lead"
    }

def resolve_teacher(x_demo_teacher: str = "", authorization: str | None = None, db: Session = Depends(get_db)) -> Teacher:
    """Identify the calling teacher.

    A valid bearer token is the only route outside demo mode. There is
    deliberately no anonymous fallback: this function previously returned the
    seeded TEACHER-PRISM record to any caller presenting no credentials at all,
    which exposed the full classroom roster to unauthenticated requests.
    """
    # These handlers are also invoked directly (by the test suite and by
    # teacher_workspace), in which case FastAPI's Header sentinel arrives
    # unresolved instead of a string. Treat anything that is not a header
    # string as "no credentials presented".
    if not isinstance(authorization, str):
        authorization = None
    if not isinstance(x_demo_teacher, str):
        x_demo_teacher = ""

    if authorization:
        payload = read_token(authorization)
        user = db.get(User, payload["sub"])
        if user and user.role == "teacher" and user.teacher_id:
            teacher = db.get(Teacher, user.teacher_id)
            if teacher:
                return teacher
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This area is available to teacher accounts")
    if x_demo_teacher and demo_mode():
        teacher = db.scalar(select(Teacher).where(Teacher.demo_identity == x_demo_teacher))
        if teacher:
            return teacher
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sign in as a teacher to view this classroom")

def learner_summaries(db: Session, students: list[Student]) -> dict[int, dict]:
    """Each learner's profile across chapters, with their most recent chapter in focus.

    Fetched in bulk so a class of 60 costs three queries, not three per learner.
    """
    ids = [student.id for student in students]
    if not ids:
        return {}
    users = {u.student_code: u for u in db.scalars(select(User).where(User.student_code.in_([s.code for s in students]))).all()}
    rows = db.scalars(select(LearnerProgress).where(LearnerProgress.student_id.in_(ids))).all()
    latest = {
        (student_id, concept_id): last_attempt
        for student_id, concept_id, last_attempt in db.execute(
            select(Attempt.student_id, Question.concept_id, func.max(Attempt.id))
            .join(Question, Question.id == Attempt.question_id)
            .where(Attempt.student_id.in_(ids))
            .group_by(Attempt.student_id, Question.concept_id)
        ).all()
    }
    summaries = {}
    for student in students:
        profiles = [row for row in rows if row.student_id == student.id]
        chapters = sorted(
            (p for p in profiles if p.evidence_count > 0 and p.concept_id in CHAPTER_BY_CONCEPT),
            key=lambda p: CHAPTER_BY_CONCEPT[p.concept_id]["number"],
        )
        focus = max(chapters, key=lambda p: latest.get((student.id, p.concept_id), 0), default=None)
        known = {p.concept_id: (p.mastery, p.evidence_count) for p in profiles}
        gap_for = lambda p: prerequisite_gap(known, p.concept_id) if p.prerequisite_status == "needs-check" else None
        user = users.get(student.code)
        entry = misconception_entry(focus.misconception) if focus else None
        summaries[student.id] = {
            "code": student.code,
            "name": user.name if user else student.code,
            "mastery": round(focus.mastery, 2) if focus else 0,
            # Every recorded response, including prerequisite-only evidence.
            "evidence_count": sum(p.evidence_count for p in profiles),
            "active_units": len(chapters),
            "focus_unit": CHAPTER_BY_CONCEPT[focus.concept_id]["id"] if focus else None,
            "focus_chapter_number": CHAPTER_BY_CONCEPT[focus.concept_id]["number"] if focus else None,
            "recommendation": focus.recommendation if focus else "diagnostic",
            "misconception": focus.misconception if focus else None,
            "misconception_title": entry["title"] if entry else None,
            "misconception_confidence": focus.misconception_confidence if focus else 0.0,
            "prerequisite_status": focus.prerequisite_status if focus else "unknown",
            "prerequisite_gap": gap_for(focus) if focus else None,
            "chapters": [
                {
                    "unit_id": CHAPTER_BY_CONCEPT[p.concept_id]["id"],
                    "number": CHAPTER_BY_CONCEPT[p.concept_id]["number"],
                    "title": CHAPTER_BY_CONCEPT[p.concept_id]["title"],
                    "mastery": p.mastery,
                    "evidence_count": p.evidence_count,
                    "misconception": p.misconception,
                    "misconception_title": (misconception_entry(p.misconception) or {}).get("title"),
                    "misconception_confidence": p.misconception_confidence,
                    "prerequisite_status": p.prerequisite_status,
                    "prerequisite_gap": gap_for(p),
                    "recommendation": p.recommendation,
                }
                for p in chapters
            ],
        }
    return summaries

@app.get("/api/teacher/workspace")
def teacher_workspace(authorization: str | None = Header(default=None), x_demo_teacher: str = Header(default=""), db: Session = Depends(get_db)):
    teacher = resolve_teacher(x_demo_teacher, authorization, db)
    students = db.scalars(select(Student).where(Student.classroom_id == teacher.classroom_id)).all()
    summaries = learner_summaries(db, list(students))
    room = db.get(Classroom, teacher.classroom_id)
    return {"class_code": room.code if room else "8A-CBSE", "teacher_name": teacher.name, "learners": [summaries[s.id] for s in students], "interventions": classroom_plans(db, teacher.classroom_id)}

@app.get("/api/teacher/students/{code}/detail")
def teacher_student_detail(code: str, authorization: str | None = Header(default=None), x_demo_teacher: str = Header(default=""), db: Session = Depends(get_db)):
    teacher = resolve_teacher(x_demo_teacher, authorization, db)
    student = student_for(code, db)
    # Same response as a missing student, so codes in other classes cannot be probed.
    if student.classroom_id != teacher.classroom_id:
        raise HTTPException(404, "Student not found")
    summary = learner_summaries(db, [student])[student.id]
    u = db.scalar(select(User).where(User.student_code == code))
    rows = db.execute(
        select(Attempt, Question)
        .join(Question, Question.id == Attempt.question_id)
        .where(Attempt.student_id == student.id)
        .order_by(Attempt.created_at.desc(), Attempt.id.desc())
    ).all()
    history = [
        {
            "id": a.id,
            "question_id": a.question_id,
            "chapter_title": CHAPTER_BY_CONCEPT[q.concept_id]["title"] if q.concept_id in CHAPTER_BY_CONCEPT else "Prerequisite check",
            "prompt": q.prompt,
            "stage": a.stage,
            "response": a.response,
            "expected_answer": q.expected_answer,
            "correct": a.correct,
            "misconception": (q.misconception_map or {}).get(a.response),
            "explanation": q.explanation,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a, q in rows
    ]
    return {**summary, "email": u.email if u else f"{code.lower()}@prism.demo", "grade": student.grade, "attempts": history}

@app.get("/api/demo")
def demo(db: Session = Depends(get_db)):
    require_demo_mode()
    return {"students":[s.code for s in db.scalars(select(Student).order_by(Student.id)).all()], "teacher":"TEACHER-PRISM", "curriculum":CBSE_CURRICULUM}

@app.get("/api/demo/personas")
def demo_personas(db: Session = Depends(get_db)):
    require_demo_mode()
    return [
        {
            "id": "aarav",
            "name": "Aarav Sharma",
            "role": "student",
            "email": "student@prism.demo",
            "student_code": "STU-VISUAL",
            "archetype": "Denominator-Magnitude Misconception",
            "route": "visual-support",
            "tag": "Misconception Archetype",
            "description": "Thinks 1/8 > 1/3 because 8 > 3. System identifies pattern and prescribes Visual Fraction Bar exploration."
        },
        {
            "id": "diya",
            "name": "Diya Patel",
            "role": "student",
            "email": "diya@prism.demo",
            "student_code": "STU-FOUNDATION",
            "archetype": "Foundational Prerequisite Gap",
            "route": "foundation",
            "tag": "Prerequisite Gap",
            "description": "Confuses equal parts and fraction anatomy. Prescribes hands-on paper-strip fraction part verification."
        },
        {
            "id": "kabir",
            "name": "Kabir Verma",
            "role": "student",
            "email": "kabir@prism.demo",
            "student_code": "STU-CALC",
            "archetype": "Calculation / Unequal Operations Slip",
            "route": "guided-practice",
            "tag": "Calculation Errors",
            "description": "Understands equivalence concept but makes arithmetic slips. Prescribes step-by-step scaffolded practice."
        },
        {
            "id": "meera",
            "name": "Meera Iyer",
            "role": "student",
            "email": "meera@prism.demo",
            "student_code": "STU-EXTEND",
            "archetype": "Demonstrated Mastery",
            "route": "extension",
            "tag": "High Mastery",
            "description": "Consistently solves standard and transfer problems accurately. Prescribes Recipe Scaling Extension Challenge."
        },
        {
            "id": "teacher",
            "name": "Ms. Ananya",
            "role": "teacher",
            "email": "teacher@prism.demo",
            "student_code": None,
            "archetype": "Classroom Educator",
            "route": "control-room",
            "tag": "Teacher Workspace",
            "description": "Lead Teacher for Class 8-A. Inspects individual evidence, reviews and edits the compiled intervention groups."
        }
    ]

@app.post("/api/demo/reset")
def reset_demo(db: Session = Depends(get_db)):
    require_demo_mode()
    from .seed import reset_to_seed
    reset_to_seed(db)
    return {"status": "ok", "message": "Classroom demo data reset to pristine state."}

@app.get("/api/students/{code}/questions")
def questions(code: str, stage: str, db: Session = Depends(get_db)):
    require_demo_mode()
    student_for(code, db)
    return [question_out(q) for q in db.scalars(select(Question).where(Question.stage == stage).order_by(Question.id)).all()]

@app.get("/api/students/{code}/progress")
def student_progress(code: str, db: Session = Depends(get_db)):
    require_demo_mode()
    student = student_for(code, db)
    return [progress_out(p, code) for p in db.scalars(select(LearnerProgress).where(LearnerProgress.student_id == student.id)).all()]

@app.post("/api/students/{code}/attempts")
def submit_attempt(code: str, payload: AttemptIn, db: Session = Depends(get_db)):
    require_demo_mode()
    return record_attempt(db, student_for(code, db), payload)

@app.get("/api/teacher/overview")
def overview(x_demo_teacher: str = Header(default=""), db: Session = Depends(get_db)):
    require_demo_mode()
    teacher = db.scalar(select(Teacher).where(Teacher.demo_identity == x_demo_teacher))
    if not teacher: raise HTTPException(403, "Teacher demo identity required")
    students = db.scalars(select(Student).where(Student.classroom_id == teacher.classroom_id)).all()
    output=[]
    for s in students:
        output.extend(progress_out(p, s.code) for p in db.scalars(select(LearnerProgress).where(LearnerProgress.student_id==s.id)).all())
    room=db.get(Classroom,teacher.classroom_id)
    return {"class_code":room.code,"curriculum":CBSE_CURRICULUM,"students":output}

@app.get("/api/teacher/interventions")
def interventions(x_demo_teacher: str = Header(default=""), db: Session = Depends(get_db), authorization: str | None = Header(default=None)):
    teacher = resolve_teacher(x_demo_teacher, authorization, db)
    return classroom_plans(db, teacher.classroom_id)

@app.post("/api/teacher/interventions/recompile", tags=["Teacher"], summary="Refresh proposed pods from live evidence, keeping every teacher decision")
def recompile_interventions(x_demo_teacher: str = Header(default=""), authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    teacher = resolve_teacher(x_demo_teacher, authorization, db)
    recompile_classroom(db, teacher.classroom_id)
    db.commit()
    return classroom_plans(db, teacher.classroom_id)

@app.put("/api/teacher/interventions/{intervention_id}")
def decide_intervention(intervention_id:int, payload:InterventionDecision, x_demo_teacher: str = Header(default=""), db:Session=Depends(get_db), authorization: str | None = Header(default=None)):
    teacher=resolve_teacher(x_demo_teacher, authorization, db)
    record=db.get(Intervention, intervention_id)
    if not record or record.classroom_id != teacher.classroom_id: raise HTTPException(404,"Intervention not found")
    record.status = payload.status
    if payload.teacher_notes is not None:
        record.teacher_notes = payload.teacher_notes
    if payload.activity is not None:
        record.activity = payload.activity
    if payload.duration is not None:
        record.duration = payload.duration
    if payload.outcome is not None:
        record.outcome = payload.outcome
    if payload.student_codes is not None:
        assigned = [student_for(c, db) for c in payload.student_codes]
        if any(s.classroom_id != teacher.classroom_id for s in assigned):
            raise HTTPException(404, "Student not found")
        record.student_ids = [s.id for s in assigned]
    db.commit()
    return {
        "id": record.id,
        "group_key": record.group_key,
        "status": record.status,
        "teacher_notes": record.teacher_notes,
        "activity": record.activity,
        "duration": record.duration,
        "outcome": record.outcome,
        "student_codes": [db.get(Student, i).code for i in record.student_ids if db.get(Student, i)]
    }

# ====================================================
# PRISM ENGINE SUITE: SEARCH, ANSWER & GENERATIVE
# ====================================================

# ----------------------------------------------------
# 1. PRISM Search Engine API
# ----------------------------------------------------
@app.post("/api/search", tags=["Search Engine"], summary="Indexed curriculum, DAG & question search")
def search_post(payload: SearchQueryIn):
    results = search_engine.search(
        query=payload.query,
        entity_type=payload.entity_type,
        chapter_id=payload.chapter_id,
        limit=payload.limit,
    )
    return {
        "query": payload.query,
        "total_results": len(results),
        "results": [
            {
                "id": r.id,
                "type": r.type,
                "title": r.title,
                "snippet": r.snippet,
                "relevance_score": r.relevance_score,
                "chapter_id": r.chapter_id,
                "concept_id": r.concept_id,
                "tags": r.tags,
                "metadata": r.metadata,
            }
            for r in results
        ],
    }

@app.get("/api/search", tags=["Search Engine"], summary="Quick query search with filters")
def search_get(q: str = "", entity_type: str = "all", chapter_id: str = "all", limit: int = 15):
    results = search_engine.search(query=q, entity_type=entity_type, chapter_id=chapter_id, limit=limit)
    return {
        "query": q,
        "total_results": len(results),
        "results": [
            {
                "id": r.id,
                "type": r.type,
                "title": r.title,
                "snippet": r.snippet,
                "relevance_score": r.relevance_score,
                "chapter_id": r.chapter_id,
                "concept_id": r.concept_id,
                "tags": r.tags,
                "metadata": r.metadata,
            }
            for r in results
        ],
    }

@app.get("/api/search/suggestions", tags=["Search Engine"], summary="Autocomplete suggestions")
def search_suggestions(q: str = "", lang: str = "en"):
    return {"suggestions": search_engine.get_suggestions(prefix=q, lang=lang)}

# ----------------------------------------------------
# 2. PRISM Answer Engine API
# ----------------------------------------------------
@app.post("/api/answer", tags=["Answer Engine"], summary="Pedagogical NCERT step-by-step problem solver")
def answer_post(payload: AnswerQueryIn):
    result = answer_engine.solve(query=payload.query, concept_id=payload.concept_id)
    return {
        "query": result.query,
        "category": result.category,
        "direct_answer": result.direct_answer,
        "confidence": result.confidence,
        "steps": result.steps,
        "verification": result.verification,
        "misconception_warning": result.misconception_warning,
        "prerequisites": result.prerequisites,
        "practice_challenge": result.practice_challenge,
        "source": result.source,
    }

@app.get("/api/answer", tags=["Answer Engine"], summary="Get step-by-step pedagogical answer for a query")
def answer_get(q: str = "", concept_id: str = ""):
    result = answer_engine.solve(query=q, concept_id=concept_id if concept_id else None)
    return {
        "query": result.query,
        "category": result.category,
        "direct_answer": result.direct_answer,
        "confidence": result.confidence,
        "steps": result.steps,
        "verification": result.verification,
        "misconception_warning": result.misconception_warning,
        "prerequisites": result.prerequisites,
        "practice_challenge": result.practice_challenge,
        "source": result.source,
    }

# ----------------------------------------------------
# 3. PRISM Generative Engine API
# ----------------------------------------------------
@app.post("/api/generate/question", tags=["Generative Engine"], summary="Generate practice/diagnostic question with tagged misconception distractors")
def generate_question_endpoint(payload: GenerateQuestionIn):
    question = generative_engine.generate_question(
        concept_id=payload.concept_id,
        stage=payload.stage,
        difficulty=payload.difficulty,
    )
    return question

@app.post("/api/generate/remediation", tags=["Generative Engine"], summary="Generate personalized remediation guide for student misconception")
def generate_remediation_endpoint(payload: GenerateRemediationIn):
    try:
        return generative_engine.generate_remediation(
            misconception_id=payload.misconception_id,
            student_name=payload.student_name,
            grade=payload.grade,
        )
    except ValueError as error:
        raise HTTPException(404, str(error))

@app.post("/api/generate/lesson-plan", tags=["Generative Engine"], summary="Generate 45-min differentiated classroom plan for teacher pods")
def generate_lesson_plan_endpoint(payload: GenerateLessonPlanIn):
    plan = generative_engine.generate_lesson_plan(
        concept_id=payload.concept_id,
        classroom_code=payload.classroom_code,
    )
    return plan

@app.post("/api/generate/transfer-task", tags=["Generative Engine"], summary="Generate authentic Indian real-world transfer problem")
def generate_transfer_task_endpoint(payload: GenerateTransferIn):
    task = generative_engine.generate_transfer_task(
        concept_id=payload.concept_id,
        theme=payload.theme,
    )
    return task

# ----------------------------------------------------
# Production SPA Static File Serving
# Enables 1-Click All-in-One Deployment (Frontend + Backend on single port)
# Path resolution order:
#   1. /app/frontend/dist  (Docker container layout)
#   2. ../../frontend/dist (local dev: running from backend/app)
#   3. frontend/dist        (local dev: running from project root)
# ----------------------------------------------------
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

def _find_frontend_dist() -> str | None:
    candidates = [
        "/app/frontend/dist",                                           # Docker
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")),  # from backend/app/
        os.path.abspath(os.path.join(os.getcwd(), "frontend", "dist")),  # from project root
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    return None

frontend_dist = _find_frontend_dist()

if frontend_dist:
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    _dist_root = os.path.realpath(frontend_dist)
    _index = os.path.join(_dist_root, "index.html")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_spa(full_path: str):
        """Serve a built asset, falling back to the SPA entry point.

        StaticFiles performs its own containment check; this hand-rolled handler
        must do the same, or a path such as ../../etc/passwd escapes the build
        directory and serves an arbitrary file off the container.
        """
        if full_path:
            candidate = os.path.realpath(os.path.join(_dist_root, full_path))
            within_root = candidate == _dist_root or candidate.startswith(_dist_root + os.sep)
            if within_root and os.path.isfile(candidate):
                return FileResponse(candidate)
        return FileResponse(_index)
