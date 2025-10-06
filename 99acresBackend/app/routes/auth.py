from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from datetime import timedelta
from app.database.schemas.user import UserCreate, UserLogin
from app.database.schemas.common import Token, SuccessResponse
from app.database.repositories.user_repository import UserRepository
from app.utils.auth import verify_password, create_access_token
from app.config import settings

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=SuccessResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Check if user already exists
    existing_user = await UserRepository.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    
    # Create user
    user_dict = user_data.dict()
    user = await UserRepository.create_user(user_dict)
    
    return SuccessResponse(
        message="User registered successfully",
        data={"user_id": str(user.id)}
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user"""
    # Find user by email or username
    user = await UserRepository.get_user_by_email_or_username(credentials.email)
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Update last login
    await UserRepository.update_last_login(str(user.id))
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # Convert user to dict for response
    user_dict = {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "user_type": user.role,  # For frontend compatibility
        "phone": user.phone,
        "is_active": user.is_active
    }
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_dict
    )


@router.post("/logout", response_model=SuccessResponse)
async def logout():
    """Logout user (token invalidation handled on frontend)"""
    return SuccessResponse(message="Logged out successfully")
