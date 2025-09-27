from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from repositories import auth as auth_repo
from models.user import User
from models.refresh_tokens import RefreshToken
from schemas.auth import RegisterRequest, TokenResponse
from core.config import settings

class AuthService:
    @staticmethod
    def register_user(db: Session, data: RegisterRequest) -> User:
        existing = auth_repo.get_user_by_email(db, data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,  # Enum enforced by schema
        )
        return auth_repo.create_user(db, user)

    @staticmethod
    def login_user(db: Session, email: str, password: str) -> TokenResponse:
        user = auth_repo.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.value},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})

        db_token = RefreshToken(user_id=user.id, token=refresh_token)
        auth_repo.save_refresh_token(db, db_token)

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh_token(db: Session, refresh_token: str) -> TokenResponse:
        token_data = decode_token(refresh_token)
        if token_data.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        db_token = auth_repo.get_refresh_token(db, refresh_token)
        if not db_token or db_token.revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        user = db.query(User).filter(User.id == int(token_data["sub"])).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.value},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        new_refresh_token = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})

        auth_repo.revoke_refresh_token(db, db_token)

        db_token_new = RefreshToken(user_id=user.id, token=new_refresh_token)
        auth_repo.save_refresh_token(db, db_token_new)

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

    @staticmethod
    def logout_user(db: Session, refresh_token: str) -> None:
        db_token = auth_repo.get_refresh_token(db, refresh_token)
        if db_token:
            auth_repo.revoke_refresh_token(db, db_token)
