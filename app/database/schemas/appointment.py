from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.database.enums import AppointmentStatus


# Base schemas
class AppointmentBase(BaseModel):
    client_name: str
    client_email: EmailStr
    client_phone: str
    agent_name: Optional[str] = None  # Made optional since not stored in model
    property_title: Optional[str] = None  # Made optional since not stored in model
    appointment_date: str  # Format: YYYY-MM-DD
    appointment_time: str  # Format: HH:MM
    notes: Optional[str] = None


# Request schemas
class AppointmentCreate(AppointmentBase):
    property_id: str
    agent_id: Optional[str] = None


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None


# Response schemas
class AppointmentResponse(AppointmentBase):
    id: str
    property_id: str
    client_id: Optional[str] = None
    agent_id: Optional[str] = None
    status: AppointmentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AppointmentStats(BaseModel):
    total_appointments: int
    scheduled_appointments: int
    confirmed_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    recent_appointments: int