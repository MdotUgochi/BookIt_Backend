from sqlalchemy.orm import Session
from repositories.booking import BookingRepository
from repositories.service import ServiceRepository
from models.booking import Booking, BookingStatus
from fastapi import HTTPException
from datetime import datetime

class BookingService:

    @staticmethod
    def create_booking(db: Session, user_id: int, service_id: int, start_time: datetime, end_time: datetime) -> Booking:
        service = ServiceRepository.get_active_by_id(db, service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found or inactive")

        if BookingRepository.conflict_exists(db, service_id, start_time, end_time):
            raise HTTPException(status_code=400, detail="Time slot not available")

        booking = Booking(
            user_id=user_id,
            service_id=service_id,
            start_time=start_time,
            end_time=end_time,
            status=BookingStatus.pending,
        )
        return BookingRepository.create(db, booking)

    @staticmethod
    def list_bookings(db: Session, user_id: int, role: str):
        if role == "admin":
            return BookingRepository.list_all(db)
        return BookingRepository.list_user_bookings(db, user_id)

    @staticmethod
    def get_booking(db: Session, booking_id: int, user_id: int, role: str):
        booking = BookingRepository.get_by_id(db, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if role != "admin" and booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")

        return booking

    @staticmethod
    def update_booking(db: Session, booking_id: int, new_status: BookingStatus, user_id: int, role: str):
        booking = BookingRepository.get_by_id(db, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if role != "admin":
            if booking.user_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            if new_status != BookingStatus.cancelled:
                raise HTTPException(status_code=403, detail="Only cancellation allowed")

        booking.status = new_status
        return BookingRepository.update(db, booking)

    @staticmethod
    def delete_booking(db: Session, booking_id: int):
        booking = BookingRepository.get_by_id(db, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        BookingRepository.delete(db, booking)
