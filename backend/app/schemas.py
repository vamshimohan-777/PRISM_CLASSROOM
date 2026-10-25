from pydantic import BaseModel, Field
from typing import Literal

class AttemptIn(BaseModel):
    question_id: str
    response: str = Field(min_length=1, max_length=200)
    stage: Literal["diagnostic", "practice", "test"]
    submission_id: str = Field(min_length=8, max_length=64)

class InterventionDecision(BaseModel):
    status: Literal["approved", "rejected"]
    teacher_notes: str = Field(default="", max_length=1000)
    activity: str | None = Field(default=None, max_length=2000)

