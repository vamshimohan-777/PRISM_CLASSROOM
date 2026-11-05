from pydantic import BaseModel, Field
from typing import Literal, Any

class AttemptIn(BaseModel):
    question_id: str
    response: str = Field(min_length=1, max_length=200)
    stage: Literal["diagnostic", "practice", "test"]
    submission_id: str = Field(min_length=8, max_length=64)

class InterventionDecision(BaseModel):
    status: Literal["approved", "rejected", "modified", "proposed"] = "approved"
    teacher_notes: str = Field(default="", max_length=1000)
    activity: str | None = Field(default=None, max_length=2000)
    duration: str | None = Field(default=None, max_length=24)
    outcome: str | None = Field(default=None, max_length=1000)
    student_codes: list[str] | None = None

class LoginIn(BaseModel):
    email: str = Field(min_length=5, max_length=180)
    password: str = Field(min_length=8, max_length=128)

class RegisterIn(LoginIn):
    name: str = Field(min_length=2, max_length=100)
    role: Literal["student", "teacher"] = "student"
    classroom_code: str | None = Field(default=None, max_length=32)

class JoinClassroomIn(BaseModel):
    classroom_code: str = Field(min_length=3, max_length=32)

# ----------------------------------------------------
# Search Engine Schemas
# ----------------------------------------------------
class SearchQueryIn(BaseModel):
    query: str = Field(min_length=1, max_length=250)
    entity_type: str | None = Field(default="all", max_length=32)
    chapter_id: str | None = Field(default="all", max_length=64)
    limit: int = Field(default=15, ge=1, le=50)

# ----------------------------------------------------
# Answer Engine Schemas
# ----------------------------------------------------
class AnswerQueryIn(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    concept_id: str | None = Field(default=None, max_length=64)

# ----------------------------------------------------
# Generative Engine Schemas
# ----------------------------------------------------
class GenerateQuestionIn(BaseModel):
    concept_id: str = Field(default="equivalent-fractions", max_length=64)
    stage: Literal["diagnostic", "practice", "test"] = "practice"
    difficulty: Literal["foundation", "standard", "challenge"] = "standard"

class GenerateRemediationIn(BaseModel):
    misconception_id: str = Field(default="denominator-magnitude", max_length=64)
    student_name: str = Field(default="Learner", max_length=80)
    grade: int = Field(default=8, ge=6, le=10)

class GenerateLessonPlanIn(BaseModel):
    concept_id: str = Field(default="equivalent-fractions", max_length=64)
    classroom_code: str = Field(default="8A-CBSE", max_length=32)

class GenerateTransferIn(BaseModel):
    concept_id: str = Field(default="equivalent-fractions", max_length=64)
    theme: str = Field(default="recipes", max_length=32)


