from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional
from app.database.schemas.user import AdminUserUpdate, UserStats
from app.database.schemas.property import AdminPropertyUpdate, PropertyStats
from app.database.schemas.common import SuccessResponse
from app.database.schemas.dashboard import DashboardStats, AdminDashboard
from app.database.repositories.user_repository import UserRepository
from app.database.repositories.property_repository import PropertyRepository
from app.database.repositories.appointment_repository import AppointmentRepository
from app.database.models import User
from app.utils.dependencies import get_admin_user

router = APIRouter()


@router.get("/dashboard/stats", response_model=AdminDashboard)
async def get_admin_dashboard_stats(current_user: User = Depends(get_admin_user)):
    """Get admin dashboard statistics"""
    # Get user stats
    user_stats = await UserRepository.get_user_stats()
    
    # Get property stats
    property_stats = await PropertyRepository.get_property_stats()
    
    # Mock data for additional dashboard metrics (you can implement these)
    dashboard_data = {
        "totalUsers": user_stats["total_users"],
        "totalProperties": property_stats["total_properties"],
        "pendingApprovals": property_stats["pending_properties"],
        "totalAppointments": 0,  # Implement appointment count
        "totalContacts": 0,  # Implement contact count
        "totalAgents": user_stats["users_by_role"].get("agent", 0),
        "totalRevenue": 2500000,  # Mock data
        "monthlyGrowth": 15.3,  # Mock data
        "activeListings": property_stats["approved_properties"],
        "premiumUsers": 89,  # Mock data
        "leadConversion": 24.5,  # Mock data
        "propertyStats": {
            "residential": property_stats["properties_by_type"].get("apartment", 0) + property_stats["properties_by_type"].get("villa", 0),
            "commercial": property_stats["properties_by_type"].get("office", 0),
            "plots": property_stats["properties_by_type"].get("plot", 0)
        },
        "recentActivities": [
            {
                "id": 1,
                "type": "User Registration",
                "message": "New user registered",
                "time": "30 minutes ago",
                "status": "success",
                "icon": "user"
            }
        ],
        "topPerformingAgents": [
            {"name": "Rajesh Kumar", "properties": 25, "revenue": 125000, "growth": 15},
            {"name": "Priya Sharma", "properties": 20, "revenue": 98000, "growth": 12}
        ],
        "revenueData": []
    }
    
    return AdminDashboard(**dashboard_data)


@router.get("/stats", response_model=DashboardStats)
async def get_admin_stats(current_user: User = Depends(get_admin_user)):
    """Get basic admin statistics"""
    user_stats = await UserRepository.get_user_stats()
    property_stats = await PropertyRepository.get_property_stats()
    total_appointments = await AppointmentRepository.count_all_appointments()
    
    stats = {
        "total_users": user_stats["total_users"],
        "total_properties": property_stats["total_properties"],
        "total_appointments": total_appointments,  # Added missing field
    }
    
    return DashboardStats(**stats)


@router.put("/users/{user_id}", response_model=SuccessResponse)
async def admin_update_user(
    user_id: str,
    user_update: AdminUserUpdate,
    current_user: User = Depends(get_admin_user)
):
    """Update user (Admin only)"""
    # Prevent updating own account role/status
    if str(current_user.id) == user_id and (
        user_update.role is not None or 
        user_update.status is not None or 
        user_update.is_active is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify your own role or status"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    updated_user = await UserRepository.update_user(user_id, update_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return SuccessResponse(message="User updated successfully")


@router.post("/users/{user_id}/block", response_model=SuccessResponse)
async def block_user(
    user_id: str,
    current_user: User = Depends(get_admin_user)
):
    """Block user (Admin only)"""
    if str(current_user.id) == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot block your own account"
        )
    
    updated_user = await UserRepository.update_user(user_id, {"is_blocked": True})
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return SuccessResponse(message="User blocked successfully")


@router.post("/users/{user_id}/unblock", response_model=SuccessResponse)
async def unblock_user(
    user_id: str,
    current_user: User = Depends(get_admin_user)
):
    """Unblock user (Admin only)"""
    updated_user = await UserRepository.update_user(user_id, {"is_blocked": False})
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return SuccessResponse(message="User unblocked successfully")


@router.put("/properties/{property_id}", response_model=SuccessResponse)
async def admin_update_property(
    property_id: str,
    property_update: AdminPropertyUpdate,
    current_user: User = Depends(get_admin_user)
):
    """Update property status (Admin only)"""
    update_data = property_update.dict(exclude_unset=True)
    
    # Add approved_at timestamp if approving
    if update_data.get("status") == "approved":
        from datetime import datetime
        update_data["approved_at"] = datetime.utcnow()
    
    updated_property = await PropertyRepository.update_property(property_id, update_data)
    if not updated_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return SuccessResponse(message="Property updated successfully")