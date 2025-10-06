from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime
from bson import ObjectId
from app.config import settings
from app.database.models import User, UserRole

security = HTTPBearer()


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """Get current user if token is provided and valid, otherwise return None"""
    if not credentials:
        return None
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
            
        user = await User.get(ObjectId(user_id))
        return user
    except (JWTError, Exception):
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = await User.get(ObjectId(user_id))
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user


async def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current user if they are admin or super admin"""
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


async def get_super_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current user if they are super admin"""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return current_user


async def get_agent_or_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current user if they are agent, admin, or super admin"""
    if current_user.role not in [UserRole.AGENT, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent or admin access required"
        )
    return current_user


async def get_staff_or_higher_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current user if they are staff, agent, admin, or super admin"""
    if current_user.role not in [UserRole.STAFF, UserRole.AGENT, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access or higher required"
        )
    return current_user


def verify_user_access(current_user: User, target_user_id: str) -> bool:
    """Verify if current user can access target user's data"""
    # Super admin can access everything
    if current_user.role == UserRole.SUPER_ADMIN:
        return True
    
    # Admin can access non-super-admin users
    if current_user.role == UserRole.ADMIN:
        return True  # We'll check target user role in the route
    
    # Users can only access their own data
    return str(current_user.id) == target_user_id


def verify_property_access(current_user: User, property_created_by: str) -> bool:
    """Verify if current user can access/modify a property"""
    # Admin and super admin can access all properties
    if current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        return True
    
    # Agents and staff can access properties they created
    if current_user.role in [UserRole.AGENT, UserRole.STAFF]:
        return str(current_user.id) == property_created_by
    
    # Regular users can only access their own properties
    return str(current_user.id) == property_created_by