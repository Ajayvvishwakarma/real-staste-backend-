from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class RecentActivity(BaseModel):
    type: str  # "property", "appointment", "inquiry", "user"
    description: str
    timestamp: datetime


class TopProperties(BaseModel):
    id: str
    title: str
    views: int
    inquiries_count: int


class UserActivityStats(BaseModel):
    total_logins: int = 0
    last_login: Optional[datetime] = None
    properties_created: int = 0
    appointments_scheduled: int = 0
    inquiries_made: int = 0


class PropertyStats(BaseModel):
    total_properties: int
    active_properties: int
    pending_properties: int
    sold_properties: int


class DashboardStats(BaseModel):
    total_properties: int
    total_users: int
    total_appointments: int
    user_specific_data: Dict[str, Any] = {}


class UserDashboard(BaseModel):
    total_properties: int
    total_appointments: int
    pending_appointments: int
    favorites_count: int
    property_views: int
    recent_activities: List[RecentActivity] = []


class AdminDashboard(BaseModel):
    total_users: int
    total_properties: int
    total_appointments: int
    total_inquiries: int
    pending_properties: int
    pending_appointments: int
    pending_inquiries: int
    active_users: int
    monthly_users: int
    monthly_properties: int
    monthly_appointments: int
    recent_activities: List[RecentActivity] = []
    top_properties: List[TopProperties] = []


class MonthlyStats(BaseModel):
    month: str
    properties: int
    users: int
    appointments: int
    inquiries: int


class YearlyStats(BaseModel):
    year: int
    monthly_data: List[MonthlyStats]
    total_properties: int
    total_users: int
    total_revenue: float = 0.0