from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.deps import get_current_user, get_db
from schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from services.review import ReviewService
from models.user import User

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReviewService.create_review(db, current_user, payload)


@router.get("/service/{service_id}", response_model=list[ReviewResponse])
def list_service_reviews(service_id: int, db: Session = Depends(get_db)):
    return ReviewService.list_service_reviews(db, service_id)


@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    payload: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReviewService.update_review(db, current_user, review_id, payload)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ReviewService.delete_review(db, current_user, review_id)
    return None
