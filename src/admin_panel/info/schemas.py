from pydantic import BaseModel
from typing import Optional


class CreateInfo(BaseModel):
    icon: str
    description: str
    position: Optional[int]


class Info(BaseModel):
    id: int
    icon: str
    description: str
    position: int