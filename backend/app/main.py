from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from .database import Base, engine, get_db
from .models import Student, Teacher, Question, Attempt, LearnerProgress, Classroom, Intervention
from .schemas import AttemptIn, InterventionDecision
from .engine import update_profile, compile_groups, validate_graph

validate_graph()
Base.metadata.create_all(bind=engine)
app = FastAPI(title="PRISM Classroom API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])

def student_for(code: str, db: Session):
    student = db.scalar(select(Student).where(Student.code == code))
    if not student: raise HTTPException(404, "Student not found")
    return student

def question_out(q: Question):
    return {"id":q.id, "concept_id":q.concept_id, "stage":q.stage, "difficulty":q.difficulty, "prompt":q.prompt, "type":q.question_type, "options":q.options, "explanation":q.explanation, "is_transfer":q.is_transfer}

def progress_out(p: LearnerProgress, code=""):
    return {"student_code":code, "mastery":p.mastery, "evidence_count":p.evidence_count, "misconception":p.misconception, "misconception_confidence":p.misconception_confidence, "prerequisite_status":p.prerequisite_status, "recommendation":p.recommendation, "provisional":True}

@app.get("/api/health")
def health(): return {"status":"ok"}

@app.get("/api/demo")
def demo(db: Session = Depends(get_db)):
    return {"students":[s.code for s in db.scalars(select(Student).order_by(Student.id)).all()], "teacher":"TEACHER-PRISM"}

@app.get("/api/students/{code}/questions")
def questions(code: str, stage: str, db: Session = Depends(get_db)):
    student_for(code, db)
    return [question_out(q) for q in db.scalars(select(Question).where(Question.stage == stage).order_by(Question.id)).all()]

@app.get("/api/students/{code}/progress")
def student_progress(code: str, db: Session = Depends(get_db)):
    student = student_for(code, db)
    progress = db.scalar(select(LearnerProgress).where(LearnerProgress.student_id == student.id, LearnerProgress.concept_id == "equivalent-fractions"))
    if not progress: raise HTTPException(404, "Progress not initialized")
    return progress_out(progress, code)

@app.post("/api/students/{code}/attempts")
def submit_attempt(code: str, payload: AttemptIn, db: Session = Depends(get_db)):
    student = student_for(code, db)
    question = db.get(Question, payload.question_id)
    if not question or question.stage != payload.stage: raise HTTPException(422, "Question does not belong to this stage")
    existing = db.scalar(select(Attempt).where(Attempt.student_id == student.id, Attempt.submission_id == payload.submission_id))
    if existing: return {"saved":True, "duplicate":True, "correct":existing.correct, "feedback":"This response was already saved."}
    response = payload.response.strip().lower().replace(" ", "")
    correct = response == question.expected_answer.lower().replace(" ", "")
    attempt = Attempt(student_id=student.id, question_id=question.id, submission_id=payload.submission_id, response=payload.response, correct=correct, stage=payload.stage)
    db.add(attempt); db.flush()
    all_attempts = db.scalars(select(Attempt).join(Question).where(Attempt.student_id == student.id, Question.concept_id == "equivalent-fractions").order_by(Attempt.created_at)).all()
    evidence = [{"correct":a.correct, "stage":a.stage, "transfer":db.get(Question,a.question_id).is_transfer, "misconception":db.get(Question,a.question_id).misconception_map.get(a.response, None)} for a in all_attempts]
    progress = db.scalar(select(LearnerProgress).where(LearnerProgress.student_id == student.id, LearnerProgress.concept_id == "equivalent-fractions"))
    result = update_profile(progress.mastery if progress else .35, evidence)
    if not progress:
        progress = LearnerProgress(student_id=student.id, concept_id="equivalent-fractions")
        db.add(progress)
    progress.mastery, progress.evidence_count = result.mastery, result.evidence_count
    progress.misconception, progress.misconception_confidence = result.misconception, result.misconception_confidence
    progress.prerequisite_status, progress.recommendation = result.prerequisite_status, result.recommendation
    db.commit()
    return {"saved":True, "duplicate":False, "correct":correct, "feedback":question.explanation if correct else "Not quite — review the explanation, then try the next evidence-gathering activity.", "profile":progress_out(progress, code), "reason":result.reason}

@app.get("/api/teacher/overview")
def overview(x_demo_teacher: str = Header(default=""), db: Session = Depends(get_db)):
    teacher = db.scalar(select(Teacher).where(Teacher.demo_identity == x_demo_teacher))
    if not teacher: raise HTTPException(403, "Teacher demo identity required")
    students = db.scalars(select(Student).where(Student.classroom_id == teacher.classroom_id)).all()
    output=[]
    for s in students:
        p=db.scalar(select(LearnerProgress).where(LearnerProgress.student_id==s.id, LearnerProgress.concept_id=="equivalent-fractions"))
        output.append(progress_out(p,s.code))
    return {"class_code":db.get(Classroom,teacher.classroom_id).code,"synthetic":True,"students":output}

@app.get("/api/teacher/interventions")
def interventions(x_demo_teacher: str = Header(default=""), db: Session = Depends(get_db)):
    teacher = db.scalar(select(Teacher).where(Teacher.demo_identity == x_demo_teacher))
    if not teacher: raise HTTPException(403, "Teacher demo identity required")
    records=db.scalars(select(Intervention).where(Intervention.classroom_id==teacher.classroom_id)).all()
    if not records:
        students=db.scalars(select(Student).where(Student.classroom_id==teacher.classroom_id)).all()
        profiles=[]
        for s in students:
            p=db.scalar(select(LearnerProgress).where(LearnerProgress.student_id==s.id, LearnerProgress.concept_id=="equivalent-fractions"))
            p.code=s.code; profiles.append(p)
        for plan in compile_groups(profiles):
            ids=[student_for(c,db).id for c in plan.pop("students")]
            records.append(Intervention(classroom_id=teacher.classroom_id,concept_id="equivalent-fractions",student_ids=ids,**plan))
            db.add(records[-1])
        db.commit()
    return [{"id":r.id,"group_key":r.group_key,"student_codes":[db.get(Student,i).code for i in r.student_ids],"barrier":r.barrier,"evidence":r.evidence,"confidence":r.confidence,"activity":r.activity,"duration":r.duration,"outcome":r.outcome,"follow_up":r.follow_up,"status":r.status,"teacher_notes":r.teacher_notes} for r in records]

@app.put("/api/teacher/interventions/{intervention_id}")
def decide_intervention(intervention_id:int, payload:InterventionDecision, x_demo_teacher: str = Header(default=""), db:Session=Depends(get_db)):
    teacher=db.scalar(select(Teacher).where(Teacher.demo_identity==x_demo_teacher))
    record=db.get(Intervention, intervention_id)
    if not teacher or not record or record.classroom_id != teacher.classroom_id: raise HTTPException(404,"Intervention not found")
    record.status, record.teacher_notes = payload.status, payload.teacher_notes
    if payload.activity: record.activity = payload.activity
    db.commit()
    return {"id":record.id,"status":record.status,"teacher_notes":record.teacher_notes,"activity":record.activity}
