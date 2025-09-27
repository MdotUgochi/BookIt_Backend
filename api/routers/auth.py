from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from db.session import SessionLocal
from schemas.auth import RegisterRequest, TokenResponse
from services.auth import AuthService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = AuthService.register_user(db, data)
    return AuthService.login_user(db, user.email, data.password)

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService.login_user(db, form_data.username, form_data.password)

@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    return AuthService.refresh_token(db, refresh_token)

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    AuthService.logout_user(db, refresh_token)
    return {"message": "Logged out"}
