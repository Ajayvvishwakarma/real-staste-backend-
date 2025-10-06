from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.database.enums import ContactStatus, InquiryType


# Contact schemas
class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    subject: Optional[str] = None
    message: str


class ContactCreate(ContactBase):
    property_id: Optional[str] = None
    property_title: Optional[str] = None


class ContactUpdate(BaseModel):
    status: Optional[ContactStatus] = None
    response: Optional[str] = None


class ContactResponse(ContactBase):
    id: str
    property_id: Optional[str] = None
    property_title: Optional[str] = None
    user_id: Optional[str] = None
    status: ContactStatus
    response: Optional[str] = None
    responded_by: Optional[str] = None
    responded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Inquiry schemas
class InquiryBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    message: str


class InquiryCreate(InquiryBase):
    inquiry_type: InquiryType
    property_id: Optional[str] = None
    property_title: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    preferred_location: Optional[str] = None


class InquiryUpdate(BaseModel):
    status: Optional[ContactStatus] = None
    response: Optional[str] = None


class InquiryResponse(InquiryBase):
    id: str
    inquiry_type: InquiryType
    property_id: Optional[str] = None
    property_title: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    preferred_location: Optional[str] = None
    user_id: Optional[str] = None
    status: ContactStatus
    response: Optional[str] = None
    responded_by: Optional[str] = None
    responded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Callback request schema
class CallbackRequest(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    message: Optional[str] = None
    property_id: Optional[str] = None
    preferred_time: Optional[str] = None


class ContactStats(BaseModel):
    total_contacts: int
    pending_contacts: int
    resolved_contacts: int
    total_inquiries: int
    recent_inquiries: int