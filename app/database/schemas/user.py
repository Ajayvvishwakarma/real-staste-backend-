from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.database.models import UserRole


# Base schemas
class UserBase(BaseModel):
    email: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.CLIENT

    
# Request schemas
class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None


class UserLogin(BaseModel):
    email: str  # Can be email or username
    password: str
    user_type: Optional[str] = "client"


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


# Response schemas
class UserResponse(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProfile(UserResponse):
    # Additional profile fields for agents
    license_number: Optional[str] = None
    agency_name: Optional[str] = None
    experience_years: Optional[int] = None
    specialization: Optional[str] = None


# Admin specific schemas
class AdminUserUpdate(BaseModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserStats(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int  # Changed from blocked_users
    verified_users: int  # Added verified users count
    recent_registrations: int
    users_by_role: dict