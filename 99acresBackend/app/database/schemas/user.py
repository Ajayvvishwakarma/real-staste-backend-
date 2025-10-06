from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.database.enums import UserRole


# Base schemas
class UserBase(BaseModel):
    email: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.CLIENT

    
# Request schemas
class UserCreate(UserBase):
    password: str


# Alternative registration schema that accepts frontend field names
class UserRegister(BaseModel):
    name: Optional[str] = None  # Maps to full_name
    full_name: Optional[str] = None
    username: Optional[str] = None  # Maps to email
    email: Optional[str] = None
    password: str
    phone: Optional[str] = None
    user_type: Optional[str] = None  # Maps to role
    role: Optional[UserRole] = None
    
    def to_user_create(self) -> UserCreate:
        """Convert frontend format to UserCreate format"""
        return UserCreate(
            email=self.email or self.username or "",
            full_name=self.full_name or self.name or "",
            phone=self.phone,
            password=self.password,
            role=self.role or (UserRole[self.user_type.upper()] if self.user_type else UserRole.CLIENT)
        )


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