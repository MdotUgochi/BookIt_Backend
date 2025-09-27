# schemas/review.py
from pydantic import BaseModel, Field
from datetime import datetime


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)  # 1–5 rating constraint
    comment: str | None = None


class ReviewCreate(ReviewBase):
    booking_id: int  # must be tied to a completed booking


class ReviewUpdate(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    comment: str | None = None


class ReviewResponse(ReviewBase):
    id: int
    booking_id: int
    created_at: datetime

    class Config:
        from_attributes = True
