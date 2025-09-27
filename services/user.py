from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from schemas.user import UserUpdate
from core.security import hash_password
from repositories import user as user_repo

def get_me(user: User) -> User:
    return user

def update_me(db: Session, user: User, payload: UserUpdate) -> User:
    if payload.name:
        user.name = payload.name
    if payload.email:
        existing = user_repo.get_user_by_email_excluding_id(db, payload.email, user.id)
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")
        user.email = payload.email
    if payload.password:
        user.password_hash = hash_password(payload.password)

    return user_repo.save_user(db, user)
