from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Classroom(Base):
    __tablename__ = "classrooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    grade: Mapped[int] = mapped_column(Integer, default=8)
    curriculum: Mapped[str] = mapped_column(String(80), default="CBSE-aligned · NCERT reference")

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    demo_identity: Mapped[str] = mapped_column(String(48), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    grade: Mapped[int] = mapped_column(Integer, default=8)
    language: Mapped[str] = mapped_column(String(12), default="en")
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Concept(Base):
    __tablename__ = "concepts"
    id: Mapped[str] = mapped_column(String(48), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    objective: Mapped[str] = mapped_column(Text)
    grade: Mapped[int] = mapped_column(Integer, default=8)
    prerequisites: Mapped[list] = mapped_column(JSON, default=list)

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[str] = mapped_column(String(48), primary_key=True)
    concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"), index=True)
    stage: Mapped[str] = mapped_column(String(24), index=True)
    difficulty: Mapped[int] = mapped_column(Integer)
    prompt: Mapped[str] = mapped_column(Text)
    question_type: Mapped[str] = mapped_column(String(24), default="choice")
    options: Mapped[list] = mapped_column(JSON, default=list)
    expected_answer: Mapped[str] = mapped_column(String(80))
    explanation: Mapped[str] = mapped_column(Text)
    misconception_map: Mapped[dict] = mapped_column(JSON, default=dict)
    is_transfer: Mapped[bool] = mapped_column(Boolean, default=False)

class Attempt(Base):
    __tablename__ = "attempts"
    __table_args__ = (UniqueConstraint("student_id", "submission_id", name="uq_submission"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    question_id: Mapped[str] = mapped_column(ForeignKey("questions.id"), index=True)
    submission_id: Mapped[str] = mapped_column(String(64))
    response: Mapped[str] = mapped_column(String(200))
    correct: Mapped[bool] = mapped_column(Boolean)
    stage: Mapped[str] = mapped_column(String(24))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class LearnerProgress(Base):
    __tablename__ = "learner_progress"
    __table_args__ = (UniqueConstraint("student_id", "concept_id", name="uq_progress"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"), index=True)
    mastery: Mapped[float] = mapped_column(Float, default=0.35)
    evidence_count: Mapped[int] = mapped_column(Integer, default=0)
    recent_correct: Mapped[int] = mapped_column(Integer, default=0)
    misconception: Mapped[str | None] = mapped_column(String(80), nullable=True)
    misconception_confidence: Mapped[float] = mapped_column(Float, default=0)
    prerequisite_status: Mapped[str] = mapped_column(String(24), default="unknown")
    recommendation: Mapped[str] = mapped_column(String(48), default="diagnostic")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Intervention(Base):
    __tablename__ = "interventions"
    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"), index=True)
    concept_id: Mapped[str] = mapped_column(ForeignKey("concepts.id"))
    group_key: Mapped[str] = mapped_column(String(64))
    student_ids: Mapped[list] = mapped_column(JSON)
    barrier: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str] = mapped_column(Text)
    confidence: Mapped[str] = mapped_column(String(16))
    activity: Mapped[str] = mapped_column(Text)
    duration: Mapped[str] = mapped_column(String(24))
    outcome: Mapped[str] = mapped_column(Text)
    follow_up: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="proposed")
    teacher_notes: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
