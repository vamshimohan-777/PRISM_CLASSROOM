from typing import Literal

from pydantic import BaseModel, Field


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
