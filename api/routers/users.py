from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from api.deps import get_current_user
from schemas.user import UserResponse, UserUpdate
from models.user import User
from services.user import get_me, update_me

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return get_me(current_user)

@router.patch("/me", response_model=UserResponse)
def patch_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_me(db, current_user, data)
