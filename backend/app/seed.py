"""Reproducible synthetic demo data. Run with `python -m app.seed`."""
from .database import Base, engine, SessionLocal
from .models import Classroom, Teacher, Student, Concept, Question, LearnerProgress, User, Attempt, Intervention
from .engine import validate_graph, compile_groups
from .scoring import recompute_student
from .curriculum import CBSE_CURRICULUM
from .auth import hash_password
from .catalog import CHAPTERS, QUESTION_BANK, misconception_tags_for

CONCEPTS = [
 ("fraction-parts", "Fraction parts", "Identify numerator, denominator, sign, and equal parts of a rational number.", []),
 ("fraction-magnitude", "Rational-number comparison", "Compare rational numbers using equal-sized wholes and sign.", ["fraction-parts"]),
 ("simplification", "Standard form", "Write a rational number in standard form by dividing both terms by a common factor.", ["fraction-parts"]),
 ("equivalent-fractions", "Equivalent rational numbers", "Generate, recognise, simplify, and apply equivalent rational numbers.", ["fraction-magnitude","simplification"]),
]
# (id, concept_id, stage, difficulty, prompt, options, answer, explanation, misconception_map)
# `diag-representation` assesses the *prerequisite* node `fraction-parts`, not
# equivalence itself, so evidence from it flows into the prerequisite DAG and can
# legitimately trigger the foundation route.
QUESTIONS = [
 ("diag-equivalent", "equivalent-fractions", "diagnostic", 1, "Which fraction is equivalent to 1/2?", ["2/3","2/4","3/4","1/4"], "2/4", "Multiplying the numerator and denominator of 1/2 by 2 gives 2/4.", {"2/3":"additive-bias"}),
 ("diag-magnitude", "equivalent-fractions", "diagnostic", 1, "Which is greater?", ["1/8","1/3","They are equal"], "1/3", "With the same numerator, the fraction with fewer equal parts is greater.", {"1/8":"denominator-magnitude"}),
 ("diag-simplify", "equivalent-fractions", "diagnostic", 2, "Write -18/24 in standard form.", ["-3/4","3/4","-9/12","-18/12"], "-3/4", "Divide numerator and denominator by 6 and keep the negative sign: -18/24 = -3/4.", {"3/4":"sign-error","-9/12":"incomplete-simplification","-18/12":"unequal-operations"}),
 ("diag-representation", "fraction-parts", "diagnostic", 2, "A strip is split into 6 equal parts and 3 are shaded. Which matching fraction names the same amount?", ["1/2","1/3","2/3","3/3"], "1/2", "Three of six equal parts is one half.", {"1/3":"fraction-parts-gap","2/3":"fraction-parts-gap"}),
 ("practice-guided", "equivalent-fractions", "practice", 2, "Complete: 3/5 = __/10", ["5","6","7","8"], "6", "Multiply both numerator and denominator by 2: 3/5 = 6/10.", {"5":"unequal-operations","8":"additive-bias"}),
 ("practice-standard", "equivalent-fractions", "practice", 3, "Which pair names the same rational number?", ["4/6 and 6/8","-3/4 and 6/-8","2/5 and 4/15","5/6 and 10/15"], "-3/4 and 6/-8", "A negative sign in either the numerator or denominator makes the rational number negative: 6/-8 = -3/4.", {"4/6 and 6/8":"additive-bias"}),
 ("test-transfer", "equivalent-fractions", "test", 3, "A recipe uses 2/3 cup of milk. Which amount is the same quantity in sixth-cup measures?", ["3/6","4/6","5/6","2/6"], "4/6", "Multiply 2/3 by 2/2 to write it in sixths: 4/6.", {"3/6":"denominator-magnitude","5/6":"additive-bias"}),
]

def main():
 validate_graph(); Base.metadata.create_all(bind=engine); db=SessionLocal()
 room=db.query(Classroom).filter_by(code="8A-CBSE").first()
 if not room:
  room=Classroom(code="8A-CBSE",grade=CBSE_CURRICULUM["grade"],curriculum="CBSE-aligned · NCERT reference"); db.add(room); db.flush()
 teacher=db.query(Teacher).filter_by(demo_identity="TEACHER-PRISM").first()
 if not teacher:
  teacher=Teacher(demo_identity="TEACHER-PRISM",name="Ms. Ananya",classroom_id=room.id); db.add(teacher); db.flush()
 else:
  teacher.classroom_id = room.id
  teacher.name = "Ms. Ananya"
 seen_concepts = set()
 for cid,name,obj,pre in CONCEPTS:
  seen_concepts.add(cid)
  if not db.get(Concept,cid): db.add(Concept(id=cid,name=name,objective=obj,grade=8,prerequisites=pre))
 for chapter in CHAPTERS:
  cid = chapter["concept"]
  if cid in seen_concepts:
   continue
  seen_concepts.add(cid)
  if not db.get(Concept,cid):
   db.add(Concept(id=cid,name=chapter["title"],objective=chapter["summary"],grade=8,prerequisites=[]))
  for index,(stage,prompt,options,answer,explanation) in enumerate(QUESTION_BANK[chapter["id"]],start=1):
   question_id=f'{chapter["id"]}-{stage}-{index}'
   if not db.get(Question,question_id):
    db.add(Question(id=question_id,concept_id=chapter["concept"],stage=stage,difficulty=index,prompt=prompt,question_type="choice",options=options,expected_answer=answer,explanation=explanation,misconception_map=misconception_tags_for(question_id),is_transfer=stage=="test"))
 for qid,concept,stage,difficulty,prompt,options,answer,explanation,mapping in QUESTIONS:
  if not db.get(Question,qid): db.add(Question(id=qid,concept_id=concept,stage=stage,difficulty=difficulty,prompt=prompt,question_type="choice",options=options,expected_answer=answer,explanation=explanation,misconception_map=mapping,is_transfer=stage=="test"))
 # Demo learners carry identity only. Their mastery, misconception label and
 # route are NOT stored here -- they are derived from seeded attempts by the
 # same engine that scores live traffic (see recompute_student below).
 LEARNERS = [
  ("STU-VISUAL", "Aarav Sharma", "student@prism.demo"),
  ("STU-FOUNDATION", "Diya Patel", "diya@prism.demo"),
  ("STU-CALC", "Kabir Verma", "kabir@prism.demo"),
  ("STU-EXTEND", "Meera Iyer", "meera@prism.demo"),
 ]
 for code, name, email in LEARNERS:
  s = db.query(Student).filter_by(code=code).first()
  if not s:
   s = Student(code=code, grade=8, language="en", classroom_id=room.id); db.add(s); db.flush()
  else:
   s.classroom_id = room.id

 db.flush()
 seed_attempts(db)
 db.flush()
 for student in db.query(Student).filter_by(classroom_id=room.id).all():
  recompute_student(db, student.id)
 db.flush()

 def demo_user(email, name, role, student_code=None, teacher_id=None):
  u = db.query(User).filter_by(email=email).first()
  if u: return
  salt, password_hash = hash_password("PrismDemo!2026")
  db.add(User(email=email, name=name, role=role, password_salt=salt, password_hash=password_hash, student_code=student_code, teacher_id=teacher_id))

 demo_user("student@prism.demo", "Aarav Sharma", "student", "STU-VISUAL")
 demo_user("diya@prism.demo", "Diya Patel", "student", "STU-FOUNDATION")
 demo_user("kabir@prism.demo", "Kabir Verma", "student", "STU-CALC")
 demo_user("meera@prism.demo", "Meera Iyer", "student", "STU-EXTEND")
 demo_user("teacher@prism.demo", "Ms. Ananya", "teacher", teacher_id=teacher.id)

 # Ensure initial interventions exist
 compile_initial_interventions(db, room.id)

 db.commit(); db.close()

def seed_attempts(db):
 attempts_data = [
  ("STU-VISUAL", [
   ("diag-equivalent", "2/4", True, "diagnostic", "seed-sub-aarav-1"),
   ("diag-magnitude", "1/8", False, "diagnostic", "seed-sub-aarav-2"),
   ("diag-simplify", "-3/4", True, "diagnostic", "seed-sub-aarav-3"),
   ("test-transfer", "3/6", False, "test", "seed-sub-aarav-4"),
  ]),
  ("STU-FOUNDATION", [
   ("diag-representation", "1/3", False, "diagnostic", "seed-sub-diya-1"),
   ("diag-equivalent", "2/3", False, "diagnostic", "seed-sub-diya-2"),
   ("diag-magnitude", "1/3", True, "diagnostic", "seed-sub-diya-3"),
  ]),
  ("STU-CALC", [
   ("diag-equivalent", "2/4", True, "diagnostic", "seed-sub-kabir-1"),
   ("diag-magnitude", "1/3", True, "diagnostic", "seed-sub-kabir-2"),
   ("diag-simplify", "-18/12", False, "diagnostic", "seed-sub-kabir-3"),
   ("practice-guided", "5", False, "practice", "seed-sub-kabir-4"),
   ("practice-standard", "-3/4 and 6/-8", True, "practice", "seed-sub-kabir-5"),
  ]),
  ("STU-EXTEND", [
   ("diag-equivalent", "2/4", True, "diagnostic", "seed-sub-meera-1"),
   ("diag-magnitude", "1/3", True, "diagnostic", "seed-sub-meera-2"),
   ("diag-simplify", "-3/4", True, "diagnostic", "seed-sub-meera-3"),
   ("practice-guided", "6", True, "practice", "seed-sub-meera-4"),
   ("test-transfer", "4/6", True, "test", "seed-sub-meera-5"),
  ]),
 ]
 for code, atts in attempts_data:
  stu = db.query(Student).filter_by(code=code).first()
  if not stu: continue
  for qid, resp, corr, stg, sub_id in atts:
   if not db.query(Attempt).filter_by(student_id=stu.id, submission_id=sub_id).first():
    db.add(Attempt(student_id=stu.id, question_id=qid, submission_id=sub_id, response=resp, correct=corr, stage=stg))

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
    """Return the classroom to its pristine demo state.

    Attempts are re-inserted and every profile is re-derived by the engine;
    no mastery score or route is written by hand.
    """
    db.query(Attempt).delete()
    db.query(Intervention).delete()
    db.query(LearnerProgress).delete()
    db.flush()
    seed_attempts(db)
    db.flush()
    for student in db.query(Student).all():
        recompute_student(db, student.id)
    db.flush()
    room = db.query(Classroom).filter_by(code="8A-CBSE").first()
    if room:
        compile_initial_interventions(db, room.id)
    db.commit()

if __name__ == "__main__":
 import sys, os
 sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 main()
