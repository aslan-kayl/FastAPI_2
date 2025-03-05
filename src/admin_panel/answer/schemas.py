from typing import Optional
from pydantic import BaseModel


class Answer(BaseModel):
    id: int
    answer: str
    question_id: Optional[int]


class CreateAnswer(BaseModel):
    answer: str
    question_id: int

