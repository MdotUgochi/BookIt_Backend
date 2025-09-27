# schemas/user.py - COMPLETE AND CORRECTED
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    """Schema for user profile response"""
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True  
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Mercy User",
                "email": "mercy@example.com",
                "role": "user",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }

class UserUpdate(BaseModel):
    """Schema for updating user profile - all fields optional"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # FIXED: This was missing!
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Name",
                "email": "newemail@example.com", 
                "password": "newpassword123"
            }
        }