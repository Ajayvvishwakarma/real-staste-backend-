from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database.sqlite_models import Base
import os

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True if settings.DEBUG else False,
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Initialize SQLite database"""
    try:
        print("🗄️ Initializing SQLite database...")
        print(f"Database URL: {settings.DATABASE_URL}")
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ SQLite database initialized successfully!")
        print("📊 All tables created successfully!")
        
        # Create some sample data if database is empty
        await create_sample_data()
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise e

async def create_sample_data():
    """Create sample data if database is empty"""
    try:
        from app.database.sqlite_models import User, EmailTemplate
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        async with AsyncSessionLocal() as session:
            # Check if users exist
            from sqlalchemy import text
            result = await session.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            
            if count == 0:
                print("📝 Creating sample data...")
                
                # Create sample users
                sample_users = [
                    User(
                        email="admin@99acres.com",
                        full_name="Admin User",
                        phone="+919999999999",
                        password_hash=pwd_context.hash("admin123"),
                        role="admin",
                        is_verified=True,
                        city="Delhi",
                        state="Delhi"
                    ),
                    User(
                        email="ajay10@gmail.com",
                        full_name="Ajay",
                        phone="7068009780",
                        password_hash=pwd_context.hash("password123"),
                        role="client",
                        is_verified=False,
                        city="Mumbai",
                        state="Maharashtra"
                    ),
                    User(
                        email="agent@99acres.com",
                        full_name="Agent Smith",
                        phone="+919876543210",
                        password_hash=pwd_context.hash("agent123"),
                        role="agent",
                        is_verified=True,
                        agent_id="AG001",
                        commission_rate=2.5,
                        city="Bangalore",
                        state="Karnataka"
                    )
                ]
                
                for user in sample_users:
                    session.add(user)
                
                # Create sample email templates
                sample_templates = [
                    EmailTemplate(
                        name="Welcome Email",
                        subject="Welcome to 99Acres!",
                        template="Hello {{name}}, Welcome to 99Acres platform!",
                        type="welcome",
                        is_active=True
                    ),
                    EmailTemplate(
                        name="Property Alert",
                        subject="New Property Match Found!",
                        template="Hi {{name}}, We found a property that matches your criteria.",
                        type="property_alert",
                        is_active=True
                    ),
                    EmailTemplate(
                        name="Appointment Confirmation",
                        subject="Appointment Confirmed",
                        template="Your appointment for {{property_title}} is confirmed for {{date}}.",
                        type="appointment",
                        is_active=True
                    )
                ]
                
                for template in sample_templates:
                    session.add(template)
                
                await session.commit()
                print("✅ Sample data created successfully!")
            else:
                print("📊 Database already has data, skipping sample data creation")
                
    except Exception as e:
        print(f"⚠️ Sample data creation failed: {e}")

async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()