from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.database.models import User, Property, Appointment, Contact, Inquiry
import os


async def init_db():
    """Initialize database connection"""
    try:
        # Allow skipping DB initialization via settings (useful for local dev without MongoDB)
        if getattr(settings, "SKIP_DB", False):
            print("SKIP_DB is true — skipping database initialization.")
            return

        print("Attempting to connect to MongoDB Atlas...")
        print(f"Connection URL: {settings.MONGODB_URL[:80]}...")
        
        # Configure TLS options for Atlas with Windows SSL fixes
        client_options = {
            "tls": True,
            "serverSelectionTimeoutMS": 30000,
            "connectTimeoutMS": 30000,
            "socketTimeoutMS": 30000,
            "heartbeatFrequencyMS": 10000,
            "maxIdleTimeMS": 30000,
        }
        
        # Try different SSL configurations for Windows compatibility
        try:
            import certifi
            import ssl
            
            # Method 1: Use certifi with explicit SSL context
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            
            client_options.update({
                "tlsCAFile": certifi.where(),
                "tlsInsecure": False,
            })
            print("Using certifi CA bundle for TLS verification")
            
        except ImportError:
            print("Warning: certifi not available")
            
        # Windows-specific SSL workarounds
        if os.name == 'nt':  # Windows
            print("Applying Windows-specific SSL configurations...")
            client_options.update({
                "tlsInsecure": True,  # Allow for Windows SSL issues
                "retryWrites": False,  # Disable retryable writes which can cause SSL issues
            })
        
        # Development fallback: complete TLS bypass for local testing
        if os.getenv("MONGODB_INSECURE", "").lower() == "true":
            print("WARNING: MONGODB_INSECURE=true - bypassing ALL TLS verification (DEV ONLY)")
            client_options.update({
                "tls": True,
                "tlsAllowInvalidCertificates": True,
                "tlsAllowInvalidHostnames": True,
                "tlsInsecure": True,
            })
        
        # Create MongoDB client with multiple retry strategies
        client = None
        connection_successful = False
        
        # Strategy 1: Try with enhanced SSL options
        try:
            print("Attempting connection with enhanced SSL configuration...")
            client = AsyncIOMotorClient(settings.MONGODB_URL, **client_options)
            await client.admin.command('ping')
            connection_successful = True
            print("MongoDB Atlas connection successful with enhanced SSL!")
        except Exception as e:
            print(f"Enhanced SSL connection failed: {e}")
            
        # Strategy 2: Try with minimal TLS if first attempt failed
        if not connection_successful:
            try:
                print("Attempting connection with minimal TLS configuration...")
                minimal_options = {
                    "tls": True,
                    "tlsInsecure": True,
                    "serverSelectionTimeoutMS": 10000,
                }
                client = AsyncIOMotorClient(settings.MONGODB_URL, **minimal_options)
                await client.admin.command('ping')
                connection_successful = True
                print("MongoDB Atlas connection successful with minimal TLS!")
            except Exception as e:
                print(f"Minimal TLS connection failed: {e}")
                
        # Strategy 3: Try with appName parameter (sometimes helps with Atlas)
        if not connection_successful:
            try:
                print("Attempting connection with appName parameter...")
                app_options = {
                    "tls": True,
                    "tlsInsecure": True,
                    "appName": "99acresBackend",
                    "serverSelectionTimeoutMS": 5000,
                }
                client = AsyncIOMotorClient(settings.MONGODB_URL, **app_options)
                await client.admin.command('ping')
                connection_successful = True
                print("MongoDB Atlas connection successful with appName!")
            except Exception as e:
                print(f"Connection with appName failed: {e}")
                
        if not connection_successful:
            raise Exception("All connection strategies failed")
        
        # Initialize beanie with the database
        database = client.get_default_database()
        print(f"Using database: {database.name}")
        
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
        
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Running without database connection for now... (set SKIP_DB=True to silence attempts)")