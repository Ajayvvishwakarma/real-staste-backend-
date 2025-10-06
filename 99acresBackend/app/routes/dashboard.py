from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId
from app.database.schemas.dashboard import (
    DashboardStats, UserDashboard, AdminDashboard, PropertyStats,
    RecentActivity, TopProperties, UserActivityStats
)
from app.database.schemas.common import SuccessResponse
from app.database.models import (
    User, Property, Appointment, Contact, Inquiry, 
    PropertyStatus, AppointmentStatus, ContactStatus, UserRole
)
from app.utils.dependencies import get_current_active_user, get_admin_user

router = APIRouter()


@router.get("/user", response_model=UserDashboard)
async def get_user_dashboard(current_user: User = Depends(get_current_active_user)):
    """Get user dashboard data"""
    user_id = ObjectId(str(current_user.id))
    
    # Get user properties count
    my_properties = await Property.find(Property.created_by == user_id).count()
    
    # Get user appointments
    my_appointments = await Appointment.find(
        {"$or": [
            {"user_id": user_id},
            {"agent_id": user_id}
        ]}
    ).count()
    
    # Get pending appointments
    pending_appointments = await Appointment.find({
        "$and": [
            {"$or": [
                {"user_id": user_id},
                {"agent_id": user_id}
            ]},
            {"status": AppointmentStatus.PENDING}
        ]
    }).count()
    
    # Get recent inquiries
    recent_inquiries = await Inquiry.find(
        Inquiry.user_id == user_id
    ).sort(-Inquiry.created_at).limit(5).to_list()
    
    # Get favorite properties count (assuming we have a favorites collection)
    favorites_count = 0  # Placeholder for favorites feature
    
    # Calculate property views (placeholder)
    property_views = 0
    if current_user.role in [UserRole.AGENT, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        properties = await Property.find(Property.created_by == user_id).to_list()
        property_views = sum(prop.views or 0 for prop in properties)
    
    # Recent activities
    activities = []
    if recent_inquiries:
        for inquiry in recent_inquiries:
            activities.append(RecentActivity(
                type="inquiry",
                description=f"New inquiry: {inquiry.message[:50]}...",
                timestamp=inquiry.created_at
            ))
    
    return UserDashboard(
        total_properties=my_properties,
        total_appointments=my_appointments,
        pending_appointments=pending_appointments,
        favorites_count=favorites_count,
        property_views=property_views,
        recent_activities=activities
    )


@router.get("/admin", response_model=AdminDashboard)
async def get_admin_dashboard(current_user: User = Depends(get_admin_user)):
    """Get admin dashboard data"""
    # Get total counts
    total_users = await User.find().count()
    total_properties = await Property.find().count()
    total_appointments = await Appointment.find().count()
    total_inquiries = await Inquiry.find().count()
    
    # Get pending counts
    pending_properties = await Property.find(Property.status == PropertyStatus.PENDING).count()
    pending_appointments = await Appointment.find(Appointment.status == AppointmentStatus.PENDING).count()
    pending_inquiries = await Inquiry.find(Inquiry.status == ContactStatus.PENDING).count()
    
    # Get active users (users who logged in last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_users = await User.find(User.last_login >= thirty_days_ago).count()
    
    # Get monthly stats
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    monthly_properties = await Property.find(Property.created_at >= one_month_ago).count()
    monthly_users = await User.find(User.created_at >= one_month_ago).count()
    monthly_appointments = await Appointment.find(Appointment.created_at >= one_month_ago).count()
    
    # Get recent activities
    recent_properties = await Property.find().sort(-Property.created_at).limit(5).to_list()
    recent_users = await User.find().sort(-User.created_at).limit(5).to_list()
    recent_inquiries = await Inquiry.find().sort(-Inquiry.created_at).limit(5).to_list()
    
    activities = []
    
    # Add recent property activities
    for prop in recent_properties:
        activities.append(RecentActivity(
            type="property",
            description=f"New property: {prop.title}",
            timestamp=prop.created_at
        ))
    
    # Add recent user activities
    for user in recent_users:
        activities.append(RecentActivity(
            type="user",
            description=f"New user registration: {user.full_name}",
            timestamp=user.created_at
        ))
    
    # Add recent inquiry activities
    for inquiry in recent_inquiries:
        activities.append(RecentActivity(
            type="inquiry",
            description=f"New inquiry from: {inquiry.name}",
            timestamp=inquiry.created_at
        ))
    
    # Sort activities by timestamp
    activities.sort(key=lambda x: x.timestamp, reverse=True)
    activities = activities[:10]  # Keep only 10 most recent
    
    # Get top properties by views
    top_properties_data = await Property.find().sort(-Property.views).limit(5).to_list()
    top_properties = []
    for prop in top_properties_data:
        top_properties.append(TopProperties(
            id=str(prop.id),
            title=prop.title,
            views=prop.views or 0,
            inquiries_count=await Inquiry.find(Inquiry.property_id == prop.id).count()
        ))
    
    return AdminDashboard(
        total_users=total_users,
        total_properties=total_properties,
        total_appointments=total_appointments,
        total_inquiries=total_inquiries,
        pending_properties=pending_properties,
        pending_appointments=pending_appointments,
        pending_inquiries=pending_inquiries,
        active_users=active_users,
        monthly_users=monthly_users,
        monthly_properties=monthly_properties,
        monthly_appointments=monthly_appointments,
        recent_activities=activities,
        top_properties=top_properties
    )


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: User = Depends(get_current_active_user)):
    """Get general dashboard statistics"""
    if current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        # Admin stats
        total_properties = await Property.find().count()
        total_users = await User.find().count()
        total_appointments = await Appointment.find().count()
        
        return DashboardStats(
            total_properties=total_properties,
            total_users=total_users,
            total_appointments=total_appointments,
            user_specific_data={}
        )
    else:
        # User stats
        user_id = ObjectId(str(current_user.id))
        my_properties = await Property.find(Property.created_by == user_id).count()
        my_appointments = await Appointment.find(Appointment.user_id == user_id).count()
        my_inquiries = await Inquiry.find(Inquiry.user_id == user_id).count()
        
        return DashboardStats(
            total_properties=my_properties,
            total_users=0,
            total_appointments=my_appointments,
            user_specific_data={
                "my_inquiries": my_inquiries,
                "favorites": 0  # Placeholder for favorites
            }
        )


@router.get("/property-stats", response_model=PropertyStats)
async def get_property_stats(current_user: User = Depends(get_current_active_user)):
    """Get property-related statistics"""
    if current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        # Admin property stats
        total_properties = await Property.find().count()
        active_properties = await Property.find(Property.status == PropertyStatus.ACTIVE).count()
        pending_properties = await Property.find(Property.status == PropertyStatus.PENDING).count()
        sold_properties = await Property.find(Property.status == PropertyStatus.SOLD).count()
    else:
        # User property stats
        user_id = ObjectId(str(current_user.id))
        total_properties = await Property.find(Property.created_by == user_id).count()
        active_properties = await Property.find({
            "created_by": user_id,
            "status": PropertyStatus.ACTIVE
        }).count()
        pending_properties = await Property.find({
            "created_by": user_id,
            "status": PropertyStatus.PENDING
        }).count()
        sold_properties = await Property.find({
            "created_by": user_id,
            "status": PropertyStatus.SOLD
        }).count()
    
    return PropertyStats(
        total_properties=total_properties,
        active_properties=active_properties,
        pending_properties=pending_properties,
        sold_properties=sold_properties
    )


@router.get("/activity", response_model=List[RecentActivity])
async def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_active_user)
):
    """Get recent user activity"""
    activities = []
    
    if current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        # Admin sees all activities
        recent_properties = await Property.find().sort(-Property.created_at).limit(limit//3).to_list()
        recent_appointments = await Appointment.find().sort(-Appointment.created_at).limit(limit//3).to_list()
        recent_inquiries = await Inquiry.find().sort(-Inquiry.created_at).limit(limit//3).to_list()
        
        for prop in recent_properties:
            activities.append(RecentActivity(
                type="property",
                description=f"Property '{prop.title}' was created",
                timestamp=prop.created_at
            ))
        
        for appointment in recent_appointments:
            activities.append(RecentActivity(
                type="appointment",
                description=f"Appointment scheduled for {appointment.appointment_date}",
                timestamp=appointment.created_at
            ))
        
        for inquiry in recent_inquiries:
            activities.append(RecentActivity(
                type="inquiry",
                description=f"New inquiry from {inquiry.name}",
                timestamp=inquiry.created_at
            ))
    else:
        # User sees only their activities
        user_id = ObjectId(str(current_user.id))
        
        user_properties = await Property.find(Property.created_by == user_id).sort(-Property.created_at).limit(limit//2).to_list()
        user_appointments = await Appointment.find(Appointment.user_id == user_id).sort(-Appointment.created_at).limit(limit//2).to_list()
        
        for prop in user_properties:
            activities.append(RecentActivity(
                type="property",
                description=f"You created property '{prop.title}'",
                timestamp=prop.created_at
            ))
        
        for appointment in user_appointments:
            activities.append(RecentActivity(
                type="appointment",
                description=f"You scheduled an appointment for {appointment.appointment_date}",
                timestamp=appointment.created_at
            ))
    
    # Sort by timestamp and limit
    activities.sort(key=lambda x: x.timestamp, reverse=True)
    return activities[:limit]