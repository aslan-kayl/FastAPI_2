from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.con.models.bookings import Booking
from src.con.models.rides import Ride


class BookingService:
    async def get_all_bookings(self, session: AsyncSession) -> List[Booking]:
        statement = select(Booking)
        result = await session.exec(statement)
        return result.all()

    async def create_booking(self, session: AsyncSession, booking: Booking) -> Booking:
        ride_stmt = select(Ride).where(Ride.id == booking.ride_id)
        ride_result = await session.exec(ride_stmt)
        ride = ride_result.first()
        if not ride:
            raise ValueError("Ride not found")

        bookings_stmt = select(Booking).where(Booking.ride_id == ride.id)
        result = await session.exec(bookings_stmt)
        existing_bookings = result.all()

        total_booked = sum(b.seats_booked for b in existing_bookings)

        if total_booked + booking.seats_booked > ride.seats:
            raise ValueError("Not enough seats")

        session.add(booking)
        await session.commit()
        await session.refresh(booking)
        return booking

    async def get_booking(self, session: AsyncSession, booking_id: int) -> Optional[Booking]:
        statement = select(Booking).where(Booking.id == booking_id)
        result = await session.exec(statement)
        return result.first()

    async def update_booking(self, booking_id: int, updated_data: dict, session: AsyncSession) -> Optional[Booking]:
        booking = await self.get_booking(booking_id, session)
        if not booking:
            return None
        for key, value in updated_data.items():
            setattr(booking, key, value)
            await session.commit()
            await session.refresh(booking)
            return booking

    async def delete_booking(self, session: AsyncSession, booking_id: int) -> bool:
        booking = await self.get_booking(session, booking_id)
        if not booking:
            return False
        await session.delete(booking)
        await session.commit()
        return True