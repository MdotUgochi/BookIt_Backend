from pydantic import BaseModel, EmailStr
from models.user import UserRole

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole  # enforce enum

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
