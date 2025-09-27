from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from api.deps import get_current_user, require_admin
from schemas.bookings import BookingCreate, BookingUpdate, BookingResponse
from services.booking import BookingService
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return BookingService.create_booking(
        db=db,
        user_id=current_user.id,
        service_id=data.service_id,
        start_time=data.start_time,
        end_time=data.end_time
    )

@router.get("/", response_model=List[BookingResponse])
def list_bookings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return BookingService.list_bookings(db, current_user.id, current_user.role)

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return BookingService.get_booking(db, booking_id, current_user.id, current_user.role)

@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, data: BookingUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return BookingService.update_booking(db, booking_id, data.status, current_user.id, current_user.role)

@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    BookingService.delete_booking(db, booking_id)
    return None
