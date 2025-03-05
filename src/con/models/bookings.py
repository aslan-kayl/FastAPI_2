from typing import Optional

from sqlmodel import SQLModel, Field, Column
import sqlalchemy as sa

class Booking(SQLModel, table=True):
    __tablename__ = 'bookings'
    id: Optional[int] = Field(
        default=None,
        sa_column=Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    )
    ride_id: int = Field(foreign_key='rides.id')
    user_id: int = Field(foreign_key='users.id')
    seats_booked: int

    created_at: Optional[str] = Field(default=None)