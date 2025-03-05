from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.con.main import get_session
from src.con.models.bookings import Booking
from src.con.services.booking_services import BookingService
from typing import List

router = APIRouter(prefix="/bookings", tags=["bookings"])
booking_service = BookingService()

async def create_booking(booking: Booking, session: AsyncSession = Depends(get_session)):
    try:
        new_booking = await booking_service.create_booking(session, booking)
        return new_booking
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[Booking])
async def get_all_bookings(session:AsyncSession = Depends(get_session)):
    return await booking_service.get_all_bookings(session)

@router.get("/{bookings_id}", response_model=Booking)
async def get_booking(booking_id: int, session: AsyncSession = Depends(get_session)):
    booking = await booking_service.get_booking(session, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking

@router.patch("/{booking_id}", response_model=Booking)
async def update_booking(booking_id: int, update_data: dict, session: AsyncSession = Depends(get_session)):
    booking = await booking_service.update_booking(booking_id, update_data, session)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, session: AsyncSession = Depends(get_session)):
    success = await booking_service.delete_booking(session, booking_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
