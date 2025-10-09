from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import asyncio

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

mongodb = MongoDB()

async def connect_to_mongo():
    """Create database connection"""
    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongodb.database = mongodb.client[settings.DATABASE_NAME]
        
        # Test the connection
        await mongodb.client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        print(f"📊 Database: {settings.DATABASE_NAME}")
        
        # Create indexes for better performance
        await create_indexes()
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
        print("🔌 MongoDB connection closed")

async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Users collection indexes
        await mongodb.database.users.create_index("email", unique=True)
        await mongodb.database.users.create_index("phone")
        await mongodb.database.users.create_index("role")
        
        # Properties collection indexes
        await mongodb.database.properties.create_index("owner_id")
        await mongodb.database.properties.create_index("city")
        await mongodb.database.properties.create_index("property_type")
        await mongodb.database.properties.create_index("status")
        await mongodb.database.properties.create_index("price")
        
        # Appointments collection indexes
        await mongodb.database.appointments.create_index("user_id")
        await mongodb.database.appointments.create_index("property_id")
        await mongodb.database.appointments.create_index("appointment_date")
        
        # Campaigns collection indexes
        await mongodb.database.campaigns.create_index("owner_id")
        await mongodb.database.campaigns.create_index("status")
        await mongodb.database.campaigns.create_index("campaign_type")
        await mongodb.database.campaigns.create_index("created_at")
        
        print("📑 Database indexes created successfully!")
        
    except Exception as e:
        print(f"⚠️ Failed to create indexes: {e}")

async def create_sample_data():
    """Create sample data if database is empty"""
    try:
        from passlib.context import CryptContext
        from datetime import datetime
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Check if users exist
        user_count = await mongodb.database.users.count_documents({})
        
        if user_count == 0:
            print("📝 Creating sample data...")
            
            # Create sample users
            sample_users = [
                {
                    "email": "admin@99acres.com",
                    "full_name": "Admin User",
                    "phone": "+919999999999",
                    "password_hash": pwd_context.hash("admin123"),
                    "role": "admin",
                    "is_active": True,
                    "is_verified": True,
                    "city": "Delhi",
                    "state": "Delhi",
                    "created_at": datetime.utcnow(),
                    "updated_at": None,
                    "last_login": None
                },
                {
                    "email": "ajayvishwakrma1@gmail.com",
                    "full_name": "Ajay Vishwakarma",
                    "phone": "7068009780",
                    "password_hash": pwd_context.hash("Ajay@123"),
                    "role": "client",
                    "is_active": True,
                    "is_verified": True,
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "created_at": datetime.utcnow(),
                    "updated_at": None,
                    "last_login": None
                },
                {
                    "email": "ajayvishwakrma2021@gmail.com",
                    "full_name": "Ajay Vishwakarma",
                    "phone": "7068009780",
                    "password_hash": pwd_context.hash("Ajay@123"),
                    "role": "client",
                    "is_active": True,
                    "is_verified": True,
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "created_at": datetime.utcnow(),
                    "updated_at": None,
                    "last_login": None
                },
                {
                    "email": "agent@99acres.com",
                    "full_name": "Agent Smith",
                    "phone": "+919876543210",
                    "password_hash": pwd_context.hash("agent123"),
                    "role": "agent",
                    "is_active": True,
                    "is_verified": True,
                    "agent_id": "AG001",
                    "commission_rate": 2.5,
                    "city": "Bangalore",
                    "state": "Karnataka",
                    "created_at": datetime.utcnow(),
                    "updated_at": None,
                    "last_login": None
                }
            ]
            
            # Insert sample users
            result = await mongodb.database.users.insert_many(sample_users)
            print(f"✅ Created {len(result.inserted_ids)} sample users")
            
            # Create sample properties
            sample_properties = [
                {
                    "title": "Luxury 3BHK Apartment in Mumbai",
                    "description": "Beautiful apartment with sea view",
                    "property_type": "apartment",
                    "price": 8500000,
                    "area": 1200,
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "furnished_status": "furnished",
                    "address": "Bandra West, Mumbai",
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "pincode": "400050",
                    "status": "available",
                    "is_featured": True,
                    "is_active": True,
                    "owner_id": result.inserted_ids[1],  # Ajay's ID
                    "created_at": datetime.utcnow(),
                    "updated_at": None
                },
                {
                    "title": "Modern 2BHK in Bangalore",
                    "description": "Well-connected location with all amenities",
                    "property_type": "apartment",
                    "price": 6500000,
                    "area": 950,
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "furnished_status": "semi-furnished",
                    "address": "Koramangala, Bangalore",
                    "city": "Bangalore",
                    "state": "Karnataka",
                    "pincode": "560034",
                    "status": "available",
                    "is_featured": False,
                    "is_active": True,
                    "owner_id": result.inserted_ids[2],  # Agent's ID
                    "created_at": datetime.utcnow(),
                    "updated_at": None
                }
            ]
            
            # Insert sample properties
            prop_result = await mongodb.database.properties.insert_many(sample_properties)
            print(f"✅ Created {len(prop_result.inserted_ids)} sample properties")
            
            print("🎉 Sample data creation completed!")
            
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")

def get_database():
    """Get database instance"""
    return mongodb.database