import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "99Acres Real Estate API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database - SQLite Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./99acres.db"
    
    # Legacy MongoDB settings (not used with SQLite)
    MONGODB_URL: str = "mongodb://localhost:27017/99acres_db"
    SKIP_DB: bool = False
    MONGODB_TLS_CA_FILE: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8080"
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"]
    UPLOAD_DIRECTORY: str = "uploads"
    
    # Email (Optional)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    
    # External APIs (Optional)
    GOOGLE_MAPS_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env file


settings = Settings()