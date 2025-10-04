from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.auth import RegisterRequest, TokenResponse, LoginRequest, LogoutRequest, RefreshRequest
from services.auth import AuthService
from api.deps import get_db

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService.register_user(db, data)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login_user(db, data.email, data.password)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    return AuthService.refresh_token(db, data.refresh_token)

@router.post("/logout")
def logout(data: LogoutRequest, db: Session = Depends(get_db)):
    AuthService.logout_user(db, data.refresh_token)
    return {"message": "Logged out successfully"}
