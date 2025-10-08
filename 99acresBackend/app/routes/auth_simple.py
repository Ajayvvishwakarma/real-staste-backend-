from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from app.database.schemas.user import UserCreate, UserLogin
from app.database.schemas.common import Token, SuccessResponse
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter()

# Custom registration model to match frontend field names
class UserRegister(BaseModel):
    email: str
    name: str  # Frontend sends 'name' instead of 'full_name'
    password: str
    phone: Optional[str] = None
    user_type: str = "Agent"  # Frontend sends 'user_type' instead of 'role'
    username: Optional[str] = None  # Frontend sends this but we don't need it

# Custom login model to match frontend field names
class UserLoginCustom(BaseModel):
    email: str
    password: str
    username: Optional[str] = None  # Frontend might send this
    remember_me: Optional[bool] = False

# Login model
class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=dict)
async def register(user_data: UserRegister):
    """Register a new user - accepts frontend field names"""
    try:
        # Map frontend field names to backend field names
        role_mapping = {
            "Agent": "AGENT",
            "Client": "CLIENT", 
            "Admin": "ADMIN"
        }
        
        mapped_role = role_mapping.get(user_data.user_type, "CLIENT")
        
        return {
            "success": True,
            "message": "User registered successfully",
            "user_data": {
                "email": user_data.email,
                "full_name": user_data.name,  # Map 'name' to 'full_name'
                "phone": user_data.phone,
                "role": mapped_role,  # Map 'user_type' to 'role'
                "user_id": 1,  # Temporary ID
                "created_at": "2024-10-07T10:30:00Z"
            },
            "token": "dummy-jwt-token-here",  # For frontend compatibility
            "expires_in": 3600
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@router.post("/login")
@router.post("/login/")
async def login(request: Request, user_data: UserLoginCustom):
    """Login user - accepts frontend field names"""
    try:
        # Simple validation - in real app, check against database
        if "@" not in user_data.email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        print(f"✅ Login successful for: {user_data.email}")
        
        # Check if this is a form submission or AJAX request
        content_type = request.headers.get("content-type", "")
        user_agent = request.headers.get("user-agent", "")
        
        # If it's a form submission (not AJAX), redirect directly
        if "application/x-www-form-urlencoded" in content_type:
            print("🔄 Redirecting via form submission")
            return RedirectResponse(url="http://localhost:3004/dashboard", status_code=302)
        
        # For AJAX requests, return JSON with redirect instruction
        response_data = {
            "success": True,
            "message": "Login successful! Redirecting to dashboard...",
            "user_data": {
                "email": user_data.email,
                "full_name": "User Name",
                "role": "AGENT",
                "user_id": 1
            },
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzI4MzcyODU4fQ.dummy-signature",
            "expires_in": 3600,
            "redirect_url": "http://localhost:3004/dashboard",  # Full URL for frontend
            "should_redirect": True
        }
        
        print(f"📤 Sending JSON response: {response_data}")
        return response_data
        
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")

@router.post("/login/form")
async def login_form(user_data: UserLoginCustom):
    """Form-based login that always redirects"""
    try:
        # Simple validation - in real app, check against database
        if "@" not in user_data.email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        print(f"✅ Form login successful for: {user_data.email}")
        print("🔄 Redirecting to dashboard...")
        
        # Always redirect for form submissions to frontend dashboard
        return RedirectResponse(url="http://localhost:3004/dashboard", status_code=302)
    except Exception as e:
        print(f"❌ Form login failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")

@router.get("/login/success")
async def login_success():
    """Redirect endpoint after successful login"""
    return RedirectResponse(url="http://localhost:3004/dashboard", status_code=302)

@router.get("/dashboard/redirect")
async def dashboard_redirect():
    """Direct redirect to frontend dashboard"""
    print("🔄 Redirecting to frontend dashboard")
    return RedirectResponse(url="http://localhost:3004/dashboard", status_code=302)

@router.get("/me", response_model=dict)
async def get_current_user():
    """Get current user info - SQLite integration pending"""
    return {
        "message": "User profile endpoint - SQLite integration in progress"
    }

@router.post("/logout", response_model=dict)
async def logout():
    """Logout user"""
    return {"message": "Logout successful"}