from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from app.database.mongo_models import User, UserRole
from app.database.mongodb import get_database
from app.utils.auth import get_password_hash, verify_token

class MongoUserRepository:
    
    @staticmethod
    async def create_user(user_data: dict) -> User:
        """Create a new user"""
        db = get_database()
        
        # Hash the password
        if 'password' in user_data:
            user_data['password_hash'] = get_password_hash(user_data.pop('password'))
        
        user_data['created_at'] = datetime.utcnow()
        
        # Insert user
        result = await db.users.insert_one(user_data)
        
        # Get the created user
        created_user = await db.users.find_one({"_id": result.inserted_id})
        return User(**created_user)
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        db = get_database()
        try:
            user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                return User(**user_doc)
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        db = get_database()
        try:
            user_doc = await db.users.find_one({"email": email})
            if user_doc:
                return User(**user_doc)
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    @staticmethod
    async def get_user_by_email_or_username(identifier: str) -> Optional[User]:
        """Get user by email"""
        return await MongoUserRepository.get_user_by_email(identifier)
            
    @staticmethod
    async def get_user_from_token(token: str) -> Optional[User]:
        """Get user from JWT token"""
        try:
            payload = verify_token(token)
            if payload and "sub" in payload:
                user_id = payload["sub"]
                return await MongoUserRepository.get_user_by_id(user_id)
            return None
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None
    
    @staticmethod
    async def update_user(user_id: str, update_data: dict) -> Optional[User]:
        """Update user"""
        db = get_database()
        try:
            update_data['updated_at'] = datetime.utcnow()
            
            result = await db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
                return User(**user_doc)
            return None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
    
    @staticmethod
    async def update_last_login(user_id: str) -> None:
        """Update user's last login time"""
        db = get_database()
        try:
            await db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"last_login": datetime.utcnow()}}
            )
        except Exception as e:
            print(f"Error updating last login: {e}")
    
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Delete user"""
        db = get_database()
        try:
            result = await db.users.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
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
        db = get_database()
        try:
            query = {}
            
            if role:
                query['role'] = role
            
            if search:
                query["$or"] = [
                    {"full_name": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}}
                ]
            
            cursor = db.users.find(query).skip(skip).limit(limit)
            users = []
            async for user_doc in cursor:
                users.append(User(**user_doc))
            
            return users
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    @staticmethod
    async def count_users(role: Optional[UserRole] = None) -> int:
        """Count users with filters"""
        db = get_database()
        try:
            query = {}
            if role:
                query['role'] = role
            
            return await db.users.count_documents(query)
        except Exception as e:
            print(f"Error counting users: {e}")
            return 0