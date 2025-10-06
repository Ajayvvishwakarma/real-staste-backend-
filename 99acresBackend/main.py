"""Entrypoint for FastAPI app. Exports the FastAPI `app` instance for Uvicorn.
"""
from app.config import settings
from app.database.sqlite_db import init_db
from app.routes.auth_simple import router as auth_router  # Simple auth without database dependencies
from app.routes.properties_simple import router as properties_router  # Simple properties with sample data
from app.routes.listings import router as listings_router  # Property listings with filtering
from app.routes.plain_listings import router as plain_listings_router  # Plain simple listings
from app.routes.basic_listings import router as basic_listings_router  # Basic listings with enhanced features
from app.routes.platinum_listings import router as platinum_listings_router  # Platinum listings with premium features
from app.routes.premium_listings import router as premium_listings_router  # Premium listings with ultra-luxury features
from app.routes.leads import router as leads_router  # Lead management and CRM
from app.routes.lead_packages import router as lead_packages_router  # Lead packages and pricing plans
from app.routes.lead_success_stories import router as lead_success_stories_router  # Success stories and testimonials
from app.routes.banners import router as banners_router  # Website banners and advertisements
from app.routes.emailers_sqlite import router as emailers_router  # SQLite emailers with database persistence
from app.routes.products_redirect import router as products_router  # Redirect products to properties
from app.routes.subscriptions import router as subscriptions_router  # Subscription plans and management
from app.routes.user_simple import router as user_router  # Simple user management
from app.routes.loans import router as loans_router  # Loan management and applications
from app.routes.root_endpoints import router as root_router  # Root level endpoints for direct access
# from app.routes.users import router as users_router  # User management and authentication
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    yield
    # Shutdown logic (if needed)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="99Acres Real Estate API - Complete backend for property management",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIRECTORY), name="uploads")

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(properties_router, prefix="/api/properties", tags=["Properties"])
app.include_router(listings_router, prefix="/api/listings", tags=["Property Listings"])
app.include_router(plain_listings_router, prefix="/api/plain-listings", tags=["Plain Listings"])
app.include_router(basic_listings_router, prefix="/api/basic-listings", tags=["Basic Listings"])
app.include_router(platinum_listings_router, prefix="/api/platinum-listings", tags=["Platinum Listings"])
app.include_router(premium_listings_router, prefix="/api/premium-listings", tags=["Premium Listings"])
app.include_router(leads_router, prefix="/api/leads", tags=["Lead Management"])
app.include_router(lead_packages_router, prefix="/api/lead-packages", tags=["Lead Packages"])
app.include_router(lead_success_stories_router, prefix="/api/lead-success-stories", tags=["Success Stories"])
app.include_router(banners_router, prefix="/api/banners", tags=["Website Banners"])
app.include_router(emailers_router, prefix="/api/emailers", tags=["Email Management"])
app.include_router(products_router, prefix="/api/products", tags=["Products Redirect"])
app.include_router(subscriptions_router, prefix="/api/subscription", tags=["Subscription Management"])
app.include_router(user_router, prefix="/api/user", tags=["User Management"])
app.include_router(loans_router, prefix="/api/apply-loan", tags=["Loan Management"])
app.include_router(root_router, prefix="/api", tags=["Root Endpoints"])  # Direct access endpoints
# app.include_router(users_router, prefix="/api/user", tags=["User Management"])
# app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
# app.include_router(appointments.router, prefix="/api/appointments", tags=["Appointments"])
# app.include_router(contacts.router, prefix="/api/contacts", tags=["Contacts"])
# app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/")
async def root():
    return {"message": "99Acres API is running!", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "allowed_origins": settings.ALLOWED_ORIGINS}
