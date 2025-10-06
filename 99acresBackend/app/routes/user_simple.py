from fastapi import APIRouter, HTTPException, status
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
import hashlib
import re

router = APIRouter()

# Simple User Models
class UserLogin(BaseModel):
    username: str
    password: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserProfile

# Simple password hashing (in production, use proper bcrypt)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def validate_password_strength(password: str) -> bool:
    """Validate password meets security requirements"""
    if len(password) < 6:
        return False
    if not re.search(r"[A-Z]", password):  # Uppercase letter
        return False
    if not re.search(r"[a-z]", password):  # Lowercase letter  
        return False
    if not re.search(r"\d", password):     # Digit
        return False
    return True

# Sample users data
USERS = [
    {
        "id": 1,
        "username": "ajay_admin",
        "email": "ajay@99acres.com",
        "password_hash": hash_password("Ajay@123"),
        "full_name": "Ajay Kumar",
        "phone": "+91-9876543210",
        "role": "admin",
        "is_active": True,
        "created_at": datetime(2024, 1, 15),
        "last_login": datetime(2024, 10, 1, 14, 30)
    },
    {
        "id": 2,
        "username": "priya_agent", 
        "email": "priya.sharma@99acres.com",
        "password_hash": hash_password("Priya@456"),
        "full_name": "Priya Sharma",
        "phone": "+91-9876543211",
        "role": "agent",
        "is_active": True,
        "created_at": datetime(2024, 2, 10),
        "last_login": datetime(2024, 10, 2, 10, 15)
    },
    {
        "id": 3,
        "username": "rohit_user",
        "email": "rohit.mehta@gmail.com", 
        "password_hash": hash_password("Rohit@789"),
        "full_name": "Rohit Mehta",
        "phone": "+91-9876543212",
        "role": "client",
        "is_active": True,
        "created_at": datetime(2024, 3, 5),
        "last_login": datetime(2024, 10, 1, 16, 45)
    }
]

# Current user session (simplified)
CURRENT_USER_SESSION = {
    "user_id": 1,  # Ajay admin is logged in by default
    "username": "ajay_admin"
}

def get_current_user() -> dict:
    """Get current logged in user"""
    user_id = CURRENT_USER_SESSION.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/login", response_model=LoginResponse)
async def login(login_data: UserLogin):
    """Simple login endpoint"""
    user = next((u for u in USERS if u["username"] == login_data.username), None)
    
    if not user or not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update session
    CURRENT_USER_SESSION["user_id"] = user["id"]
    CURRENT_USER_SESSION["username"] = user["username"]
    
    # Update last login
    user["last_login"] = datetime.now()
    
    # Create user profile
    profile = UserProfile(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        phone=user.get("phone"),
        role=user["role"],
        is_active=user["is_active"],
        created_at=user["created_at"],
        last_login=user.get("last_login")
    )
    
    return LoginResponse(
        access_token=f"token_{user['username']}_123",
        token_type="bearer",
        user=profile
    )

@router.get("/profile", response_model=UserProfile)
async def get_profile():
    """Get current user profile"""
    user = get_current_user()
    
    return UserProfile(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        phone=user.get("phone"),
        role=user["role"],
        is_active=user["is_active"],
        created_at=user["created_at"],
        last_login=user.get("last_login")
    )

@router.post("/change-password")
async def change_password(password_data: PasswordChange):
    """Change user password"""
    user = get_current_user()
    
    # Verify current password
    if not verify_password(password_data.current_password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password strength
    if not validate_password_strength(password_data.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 6 characters with uppercase, lowercase, and number"
        )
    
    # Check if new password is different from current
    if verify_password(password_data.new_password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )
    
    # Update password
    user["password_hash"] = hash_password(password_data.new_password)
    
    return {"message": "Password changed successfully"}

@router.post("/logout")
async def logout():
    """Logout current user"""
    CURRENT_USER_SESSION.clear()
    return {"message": "Successfully logged out"}

@router.get("/users")
async def get_users():
    """Get all users (admin only)"""
    current_user = get_current_user()
    
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    users_list = []
    for user in USERS:
        users_list.append(UserProfile(
            id=user["id"],
            username=user["username"], 
            email=user["email"],
            full_name=user["full_name"],
            phone=user.get("phone"),
            role=user["role"],
            is_active=user["is_active"],
            created_at=user["created_at"],
            last_login=user.get("last_login")
        ))
    
    return users_list

@router.get("/current-session")
async def get_current_session():
    """Get current session info"""
    if not CURRENT_USER_SESSION:
        return {"logged_in": False, "user": None}
    
    user = get_current_user()
    return {
        "logged_in": True, 
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "full_name": user["full_name"]
        }
    }