from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.database.models import User, Property, Appointment, Contact, Inquiry


async def init_db():
    """Initialize database connection"""
    try:
        # Create Motor client
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        
        # Test the connection
        await client.admin.command('ping')
        
        # Initialize beanie with the database
        database = client.get_default_database()
        
        # Initialize beanie with document models
        await init_beanie(
            database=database,
            document_models=[
                User,
                Property, 
                Appointment,
                Contact,
                Inquiry
            ]
        )
        
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"⚠️ Database connection failed: {str(e)}")
        print("📍 Running without database connection for now...")