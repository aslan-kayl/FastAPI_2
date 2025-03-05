from typing import Optional
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, Text
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Banner(SQLModel, table=True):
    __tablename__ = "banners"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str = Field (sa_column=Column(Text))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    is_main: bool = Field(default=False, nullable=False)


class Info(SQLModel, table=True):
    __tablename__ = "info"
    id: Optional[int] = Field(primary_key=True)
    icon: str
    description: str = Field(sa_column=Column(pg.TEXT))
    position: int = Field(default=1)


class Question(SQLModel, table=True):
    __tablename__ = "questions"
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    answer: Optional["Answer"] = Relationship(
        back_populates="question",
        cascade_delete=True,
        sa_relationship_kwargs={
            'uselist': False
        })


class Answer(SQLModel, table=True):
    __tablename__ = "answers"
    id: Optional[int] = Field(default=None, primary_key=True)
    answer: str
    question_id: Optional[int] = Field(foreign_key="questions.id", unique=True)
    question: Optional["Question"] = Relationship(back_populates="answer")
