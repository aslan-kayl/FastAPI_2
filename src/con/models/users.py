from enum import Enum
from typing import Optional, List


from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import sqlalchemy as sa

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(sa.Integer, autoincrement=True, primary_key=True, nullable=False)
    )

    username: str
    phone: str
    first_name: str
    last_name: str
    role: UserRole = Field(
        default=UserRole.user,
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False), exclude=True)
    created_at: datetime = Field(default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(default_factory=datetime.now, sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<User {self .username}>"

    rides: List["Ride"] = Relationship(back_populates="user")

