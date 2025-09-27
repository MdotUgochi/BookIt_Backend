from sqlalchemy.orm import Session
from models.user import User
from models.refresh_tokens import RefreshToken

def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def save_refresh_token(db: Session, token: RefreshToken) -> RefreshToken:
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def get_refresh_token(db: Session, token: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()

def revoke_refresh_token(db: Session, token: RefreshToken) -> None:
    token.revoked = True
    db.commit()
