from fastapi import APIRouter, HTTPException, status, Request, Depends, Security
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database.repositories.mongo_user_repository import MongoUserRepository
from app.database.mongo_models import User
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.config import settings
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import json

security = HTTPBearer()
router = APIRouter()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    """Get current user from token"""
    try:
        token = credentials.credentials
        user = await MongoUserRepository.get_user_from_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Custom registration model to match frontend field names
class UserRegister(BaseModel):
    email: str
    name: str  # Frontend sends 'name' instead of 'full_name'
    password: str
    phone: Optional[str] = None
    user_type: str = "Agent"  # Frontend sends 'user_type' instead of 'role'
    username: Optional[str] = None

# Custom login model to match frontend field names
class UserLoginCustom(BaseModel):
    email: str
    password: str
    user_type: Optional[str] = None  # Frontend sends user_type
    username: Optional[str] = None  # Frontend might send this
    remember_me: Optional[bool] = False

@router.post("/register", response_model=dict)
async def register(user_data: UserRegister):
    """Register a new user with MongoDB database"""
    try:
        # Check if user exists
        existing_user = await MongoUserRepository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Map frontend fields to database fields
        role_mapping = {
            "Agent": "agent",
            "Client": "client", 
            "Admin": "admin",
            "subuser": "subuser"
        }
        
        user_dict = {
            "email": user_data.email,
            "full_name": user_data.name,
            "phone": user_data.phone or "",
            "password": user_data.password,  # Will be hashed in repository
            "role": role_mapping.get(user_data.user_type, "client")
        }
        
        # Create user in database
        user = await MongoUserRepository.create_user(user_dict)
        
        # Generate token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "success": True,
            "message": "User registered successfully",
            "user_data": {
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
                "role": user.role,
                "user_id": str(user.id),
                "created_at": user.created_at.isoformat()
            },
            "token": access_token,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
@router.post("/login/")
async def login(request: Request, user_data: UserLoginCustom):
    """Login user with MongoDB database"""
    try:
        print(f"Login attempt for email: {user_data.email}, user_type: {user_data.user_type}")
        
        # Get user from database
        user = await MongoUserRepository.get_user_by_email(user_data.email)
        if not user:
            raise HTTPException(status_code=400, detail="User not found with this email address")
        
        # Verify password
        if not verify_password(user_data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid password")
            
        # Note: Removed strict user_type validation to allow flexible login
        # Users can login regardless of the user_type sent from frontend
        
        # Update last login
        await MongoUserRepository.update_last_login(str(user.id))
        
        # Generate token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Check content type for redirect or JSON response
        content_type = request.headers.get("content-type", "")
        
        # For form submissions, redirect
        if "application/x-www-form-urlencoded" in content_type:
            return RedirectResponse(url="http://localhost:3004/dashboard", status_code=302)
        
        # For AJAX requests, return JSON
        return {
            "success": True,
            "message": "Login successful! Redirecting to dashboard...",
            "user_data": {
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "user_id": str(user.id)
            },
            "token": access_token,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "redirect_url": "http://localhost:3004/dashboard",
            "should_redirect": True
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile from MongoDB database"""
    return {
        "success": True,
        "user_data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "full_name": current_user.full_name,
            "phone": current_user.phone,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "profile_picture": current_user.profile_picture,
            "address": current_user.address,
            "city": current_user.city,
            "state": current_user.state,
            "pincode": current_user.pincode,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "last_login": current_user.last_login.isoformat() if current_user.last_login else None
        }
    }

@router.post("/logout", response_model=dict)
async def logout():
    """Logout user - client-side token removal"""
    return {"message": "Logged out successfully"}