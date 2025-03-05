from pydantic import BaseModel

class CreateQuestion(BaseModel):
    question: str


class Question(BaseModel):
    id: int
    question: str



