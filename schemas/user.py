# schemas/user.py - COMPLETE AND CORRECTED
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models.user import UserRole

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole  # enforce enum

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True  
        

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserUpdate(BaseModel):
    
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  

    class Config:
        from_attributes = True
