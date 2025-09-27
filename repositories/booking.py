from sqlalchemy.orm import Session
from models.booking import Booking
from datetime import datetime

class BookingRepository:

    @staticmethod
    def create(db: Session, booking: Booking) -> Booking:
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def get_by_id(db: Session, booking_id: int) -> Booking | None:
        return db.query(Booking).filter(Booking.id == booking_id).first()

    @staticmethod
    def list_all(db: Session) -> list[Booking]:
        return db.query(Booking).all()

    @staticmethod
    def list_user_bookings(db: Session, user_id: int) -> list[Booking]:
        return db.query(Booking).filter(Booking.user_id == user_id).all()

    @staticmethod
    def conflict_exists(db: Session, service_id: int, start_time: datetime, end_time: datetime) -> bool:
        return (
            db.query(Booking)
            .filter(
                Booking.service_id == service_id,
                Booking.start_time < end_time,
                Booking.end_time > start_time,
            )
            .first()
            is not None
        )

    @staticmethod
    def update(db: Session, booking: Booking) -> Booking:
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def delete(db: Session, booking: Booking) -> None:
        db.delete(booking)
        db.commit()
