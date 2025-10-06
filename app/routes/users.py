from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from app.database.schemas.user import (
    UserResponse, UserUpdate, UserProfile, ChangePassword, UserStats
)
from app.database.schemas.common import SuccessResponse, PaginatedResponse
from app.database.repositories.user_repository import UserRepository
from app.database.models import User, UserRole
from app.utils.dependencies import get_current_active_user, get_admin_user
from app.utils.auth import verify_password, get_password_hash

router = APIRouter()


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    user_dict = current_user.dict()
    user_dict["id"] = str(current_user.id)
    return UserProfile(**user_dict)


@router.put("/profile", response_model=SuccessResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile"""
    update_data = user_update.dict(exclude_unset=True)
    
    # Check if email is being updated and is unique
    if "email" in update_data:
        existing_user = await UserRepository.get_user_by_email(update_data["email"])
        if existing_user and str(existing_user.id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if username is being updated and is unique
    if "username" in update_data and update_data["username"]:
        existing_user = await UserRepository.get_user_by_username(update_data["username"])
        if existing_user and str(existing_user.id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    updated_user = await UserRepository.update_user(str(current_user.id), update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return SuccessResponse(message="Profile updated successfully")


@router.post("/change-password", response_model=SuccessResponse)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_active_user)
):
    """Change user password"""
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    new_password_hash = get_password_hash(password_data.new_password)
    await UserRepository.update_user(
        str(current_user.id),
        {"password_hash": new_password_hash}
    )
    
    return SuccessResponse(message="Password changed successfully")


@router.get("", response_model=PaginatedResponse)
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    role: Optional[UserRole] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get users list (Restricted based on user role)"""
    skip = (page - 1) * size
    
    # Regular users can only see basic info of other users
    if current_user.role == UserRole.CLIENT:
        # Clients can only see agents and staff for contact purposes
        if role and role not in [UserRole.AGENT, UserRole.STAFF]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        # Force role filter for clients
        if not role:
            role = UserRole.AGENT
    
    users = await UserRepository.get_users(
        skip=skip,
        limit=size,
        role=role,
        search=search
    )
    
    total = await UserRepository.count_users(role=role, status=status)
    
    # Convert users to response format
    users_data = []
    for user in users:
        user_dict = user.dict()
        user_dict["id"] = str(user.id)
        users_data.append(user_dict)
    
    return PaginatedResponse(
        items=users_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/stats", response_model=UserStats)
async def get_user_stats(current_user: User = Depends(get_current_active_user)):
    """Get user statistics (Restricted based on user role)"""
    # Only staff and higher can see full stats
    if current_user.role not in [UserRole.STAFF, UserRole.AGENT, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    stats = await UserRepository.get_user_stats()
    return UserStats(**stats)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID (Users can access their own data, admins can access any)"""
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    user = await UserRepository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_dict = user.dict()
    user_dict["id"] = str(user.id)
    return UserResponse(**user_dict)


@router.delete("/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_admin_user)
):
    """Delete user (Admin only)"""
    # Prevent self-deletion
    if str(current_user.id) == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    success = await UserRepository.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return SuccessResponse(message="User deleted successfully")