from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.review import Review
from models.booking import Booking, BookingStatus
from models.user import User, UserRole
from schemas.review import ReviewCreate, ReviewUpdate
from repositories.review import ReviewRepository


class ReviewService:

    @staticmethod
    def create_review(db: Session, user: User, payload: ReviewCreate) -> Review:
        booking = db.query(Booking).filter(Booking.id == payload.booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if booking.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not your booking")

        if booking.status != BookingStatus.completed:
            raise HTTPException(status_code=400, detail="Can only review completed bookings")

        existing_review = ReviewRepository.get_by_booking_id(db, booking.id)
        if existing_review:
            raise HTTPException(status_code=400, detail="This booking already has a review")

        review = Review(
            booking_id=payload.booking_id,
            rating=payload.rating,
            comment=payload.comment,
        )
        return ReviewRepository.create(db, review)

    @staticmethod
    def list_service_reviews(db: Session, service_id: int) -> list[Review]:
        return ReviewRepository.get_for_service(db, service_id)

    @staticmethod
    def update_review(db: Session, user: User, review_id: int, payload: ReviewUpdate) -> Review:
        review = ReviewRepository.get_by_id(db, review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        if review.booking.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not your review")

        for field, value in payload.dict(exclude_unset=True).items():
            setattr(review, field, value)

        return ReviewRepository.save(db, review)

    @staticmethod
    def delete_review(db: Session, user: User, review_id: int) -> None:
        review = ReviewRepository.get_by_id(db, review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        if review.booking.user_id != user.id and user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Not authorized")

        ReviewRepository.delete(db, review)
