from typing import Optional, List
from datetime import datetime
from sqlalchemy import select
from app.database.sqlite_models import User
from app.database.enums import UserRole
from app.utils.auth import get_password_hash, verify_token
from app.database.sqlite_db import get_session


class UserRepository:
    
    @staticmethod
    async def create_user(user_data: dict) -> User:
        """Create a new user"""
        # Hash the password
        if 'password' in user_data:
            user_data['password_hash'] = get_password_hash(user_data.pop('password'))
        
        user = User(**user_data)
        async with get_session() as session:
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            except Exception as e:
                await session.rollback()
                raise e
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        async with get_session() as session:
            try:
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
            except Exception as e:
                print(f"Error getting user by ID: {e}")
                return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        async with get_session() as session:
            try:
                stmt = select(User).where(User.email == email)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
            except Exception as e:
                print(f"Error getting user by email: {e}")
                return None
    
    @staticmethod
    async def get_user_by_email_or_username(identifier: str) -> Optional[User]:
        """Get user by email"""
        async with get_session() as session:
            try:
                stmt = select(User).where(User.email == identifier)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
            except Exception as e:
                print(f"Error getting user by identifier: {e}")
                return None
            
    @staticmethod
    async def get_user_from_token(token: str) -> Optional[User]:
        """Get user from JWT token"""
        try:
            user_id = verify_token(token)
            if user_id:
                return await UserRepository.get_user_by_id(user_id)
            return None
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None
    
    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> Optional[User]:
        """Update user"""
        async with get_session() as session:
            try:
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                
                if user:
                    update_data['updated_at'] = datetime.utcnow()
                    for key, value in update_data.items():
                        setattr(user, key, value)
                    await session.commit()
                    await session.refresh(user)
                    return user
                return None
            except Exception as e:
                await session.rollback()
                print(f"Error updating user: {e}")
                return None
    
    @staticmethod
    async def update_last_login(user_id: str) -> None:
        """Update user's last login time"""
        async with get_session() as session:
            try:
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                
                if user:
                    user.last_login = datetime.utcnow()
                    await session.commit()
            except Exception as e:
                await session.rollback()
                print(f"Error updating last login: {e}")
    
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Delete user"""
        async with get_session() as session:
            try:
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                
                if user:
                    await session.delete(user)
                    await session.commit()
                    return True
                return False
            except Exception as e:
                await session.rollback()
                print(f"Error deleting user: {e}")
                return False
    
    @staticmethod
    async def get_users(
        skip: int = 0,
        limit: int = 20,
        role: Optional[UserRole] = None,
        search: Optional[str] = None
    ) -> List[User]:
        """Get users with filters"""
        query = {}
        
        if role:
            query['role'] = role
        
        users = User.find(query)
        
        if search:
            users = users.find({
                "$or": [
                    {"full_name": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}},
                    {"username": {"$regex": search, "$options": "i"}}
                ]
            })
        
        return await users.skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def count_users(
        role: Optional[UserRole] = None
    ) -> int:
        """Count users with filters"""
        query = {}
        if role:
            query['role'] = role
        
        return await User.find(query).count()
    
    @staticmethod
    async def update_last_login(user_id: str) -> None:
        """Update user's last login timestamp"""
        try:
            user = await User.get(ObjectId(user_id))
            if user:
                user.last_login = datetime.utcnow()
                await user.save()
        except:
            pass
    
    @staticmethod
    async def get_user_stats() -> dict:
        """Get user statistics"""
        total_users = await User.find().count()
        active_users = await User.find(User.is_active == True).count()
        inactive_users = await User.find(User.is_active == False).count()  # Use inactive instead of blocked
        verified_users = await User.find(User.is_verified == True).count()
        
        # Get users by role
        roles_count = {}
        for role in UserRole:
            count = await User.find(User.role == role).count()
            roles_count[role.value] = count
        
        # Recent registrations (last 30 days)
        from datetime import timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_registrations = await User.find(
            User.created_at >= thirty_days_ago
        ).count()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users,  # Changed from blocked_users
            "verified_users": verified_users,  # Added verified users count
            "recent_registrations": recent_registrations,
            "users_by_role": roles_count
        }