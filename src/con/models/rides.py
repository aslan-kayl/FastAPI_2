from typing import Optional

import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Column, Relationship

import sqlalchemy.dialects.postgresql as pg
from datetime import datetime

class Ride(SQLModel, table=True):
    __tablename__ = "rides"
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(sa.Integer, autoincrement=True, primary_key=True, nullable=False)
    )
    user_id: int = Field(foreign_key="users.id")
    starting_point: str
    end_point: str
    seats: int
    ride_time: datetime
    created_at: datetime = Field(default=datetime.now, sa_column=Column(sa.DateTime, default=sa.func.now()))

    user: 'User' = Relationship(back_populates="rides")