"""Reproducible synthetic demo data. Run with `python -m app.seed`."""
from .database import Base, engine, SessionLocal
from .models import Classroom, Teacher, Student, Concept, Question, LearnerProgress
from .engine import validate_graph

CONCEPTS = [
 ("fraction-parts", "Fraction parts", "Identify numerator, denominator, and equal parts of a whole.", []),
 ("fraction-magnitude", "Fraction magnitude", "Compare fractions using equal-sized wholes.", ["fraction-parts"]),
 ("simplification", "Simplifying fractions", "Simplify a fraction by dividing both terms by a common factor.", ["fraction-parts"]),
 ("equivalent-fractions", "Equivalent fractions", "Generate, recognise, and apply equivalent fractions.", ["fraction-magnitude","simplification"]),
]
QUESTIONS = [
 ("diag-equivalent", "diagnostic", 1, "Which fraction is equivalent to 1/2?", ["2/3","2/4","3/4","1/4"], "2/4", "Multiplying the numerator and denominator of 1/2 by 2 gives 2/4.", {}),
 ("diag-magnitude", "diagnostic", 1, "Which is greater?", ["1/8","1/3","They are equal"], "1/3", "With the same numerator, the fraction with fewer equal parts is greater.", {"1/8":"denominator-magnitude"}),
 ("diag-simplify", "diagnostic", 2, "Simplify 6/8.", ["3/4","2/3","6/4","1/2"], "3/4", "Divide both numerator and denominator by 2: 6/8 = 3/4.", {"2/3":"unequal-operations","6/4":"denominator-magnitude"}),
 ("diag-representation", "diagnostic", 2, "A strip is split into 6 equal parts and 3 are shaded. Which matching fraction names the same amount?", ["1/2","1/3","2/3","3/3"], "1/2", "Three of six equal parts is one half.", {"1/3":"fraction-parts-gap"}),
 ("practice-guided", "practice", 2, "Complete: 3/5 = __/10", ["5","6","7","8"], "6", "Multiply both numerator and denominator by 2: 3/5 = 6/10.", {"5":"unequal-operations","8":"additive-equivalence"}),
 ("practice-standard", "practice", 3, "Which pair is equivalent?", ["4/6 and 6/8","3/4 and 6/8","2/5 and 4/15","5/6 and 10/15"], "3/4 and 6/8", "Both 3/4 and 6/8 simplify to three quarters.", {"4/6 and 6/8":"additive-equivalence"}),
 ("test-transfer", "test", 3, "A recipe uses 2/3 cup of milk. Which amount is the same quantity in sixth-cup measures?", ["3/6","4/6","5/6","2/6"], "4/6", "Multiply 2/3 by 2/2 to write it in sixths: 4/6.", {"3/6":"denominator-magnitude","5/6":"additive-equivalence"}),
]

def main():
 validate_graph(); Base.metadata.create_all(bind=engine); db=SessionLocal()
 if db.query(Classroom).first(): db.close(); return
 room=Classroom(code="8A-PRISM",grade=8); db.add(room); db.flush()
 db.add(Teacher(demo_identity="TEACHER-PRISM",name="Ms. Ananya (Demo)",classroom_id=room.id))
 for cid,name,obj,pre in CONCEPTS: db.add(Concept(id=cid,name=name,objective=obj,grade=8,prerequisites=pre))
 for qid,stage,difficulty,prompt,options,answer,explanation,mapping in QUESTIONS:
  db.add(Question(id=qid,concept_id="equivalent-fractions",stage=stage,difficulty=difficulty,prompt=prompt,question_type="choice",options=options,expected_answer=answer,explanation=explanation,misconception_map=mapping,is_transfer=stage=="test"))
 profiles=[
  ("STU-VISUAL","visual-support",.38,4,"denominator-magnitude",.75,"needs-check"),
  ("STU-FOUNDATION","foundation",.27,3,"fraction-parts-gap",.55,"needs-check"),
  ("STU-CALC","guided-practice",.54,4,"unequal-operations",.5,"secure"),
  ("STU-EXTEND","extension",.88,5,None,0,"secure"),
 ]
 for code,route,mastery,count,miscon,conf,pre in profiles:
  s=Student(code=code,grade=8,language="en",classroom_id=room.id); db.add(s); db.flush()
  db.add(LearnerProgress(student_id=s.id,concept_id="equivalent-fractions",mastery=mastery,evidence_count=count,recent_correct=max(0,count-1),misconception=miscon,misconception_confidence=conf,prerequisite_status=pre,recommendation=route))
 db.commit(); db.close()

if __name__ == "__main__": main()
