from sqlalchemy.orm import Session
from models.review import Review


class ReviewRepository:

    @staticmethod
    def get_by_id(db: Session, review_id: int) -> Review | None:
        return db.query(Review).filter(Review.id == review_id).first()

    @staticmethod
    def get_by_booking_id(db: Session, booking_id: int) -> Review | None:
        return db.query(Review).filter(Review.booking_id == booking_id).first()

    @staticmethod
    def get_for_service(db: Session, service_id: int) -> list[Review]:
        return (
            db.query(Review)
            .join(Review.booking)
            .filter(Review.booking.service_id == service_id)
            .all()
        )

    @staticmethod
    def create(db: Session, review: Review) -> Review:
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def delete(db: Session, review: Review) -> None:
        db.delete(review)
        db.commit()

    @staticmethod
    def save(db: Session, review: Review) -> Review:
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
