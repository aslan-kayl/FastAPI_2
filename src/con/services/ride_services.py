from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, date
from typing import List
from src.con.models import Ride


class RideService:
    async def create_ride(
        self,
        user_id: int,
        starting_point: str,
        end_point: str,
        seats: int,
        ride_time: datetime,
        session: AsyncSession
) -> Ride:
        new_ride = Ride(
            user_id=user_id,
            start_time=starting_point,
            end_time=end_point,
            seats=seats,
            ride_time=ride_time,
        )
        session.add(new_ride)
        await session.commit()
        await session.refresh(new_ride)
        return new_ride

    async def search_rides(
        self,
        starting_point: str,
        end_point: str,
        requested_seats: int,
        ride_time: date,
        session: AsyncSession
) -> List[Ride]:

        statement = select(Ride).where(
Ride.starting_point == starting_point,
            Ride.end_point == end_point,
            Ride.ride_date == ride_time,
            Ride.seats == requested_seats,
        )
        result = await session.exec(statement)
        rides = result.all()
        return rides