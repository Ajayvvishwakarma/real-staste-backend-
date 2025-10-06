from datetime import datetime
from typing import Optional, List
from enum import Enum
from beanie import Document
from pydantic import Field, EmailStr, ConfigDict


# Enums
class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STAFF = "staff"
    AGENT = "agent"
    CLIENT = "client"
    SUBUSER = "subuser"


class PropertyType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    PLOT = "plot"
    VILLA = "villa"
    APARTMENT = "apartment"
    INDEPENDENT_HOUSE = "independent_house"
    BUILDER_FLOOR = "builder_floor"
    PENTHOUSE = "penthouse"
    STUDIO = "studio"


class PropertyStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SOLD = "sold"
    RENTED = "rented"
    UNDER_REVIEW = "under_review"


class ListingType(str, Enum):
    SALE = "sale"
    RENT = "rent"
    PG = "pg"


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


class ContactStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class InquiryType(str, Enum):
    GENERAL = "general"
    PROPERTY_SPECIFIC = "property_specific"
    CALLBACK_REQUEST = "callback_request"
    PRICE_INQUIRY = "price_inquiry"
    VISIT_REQUEST = "visit_request"


# Models
class User(Document):
    email: EmailStr = Field(..., unique=True)
    full_name: str
    phone: Optional[str] = None
    password_hash: str
    role: UserRole = UserRole.CLIENT
    is_active: bool = True
    is_verified: bool = False
    profile_picture: Optional[str] = None
    
    # Additional profile fields
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    
    # System fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    # Agent specific fields
    agent_id: Optional[str] = None
    commission_rate: Optional[float] = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "role", 
            "is_active",
            "created_at"
        ]


class Property(Document):
    title: str
    description: Optional[str] = ""
    property_type: PropertyType
    listing_type: ListingType
    
    # Location
    address: str
    city: str
    state: str
    pincode: Optional[str] = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Property details
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None
    floor_number: Optional[int] = None
    total_floors: Optional[int] = None
    
    # Pricing
    price: float
    price_per_sqft: Optional[float] = None
    maintenance_charges: Optional[float] = None
    security_deposit: Optional[float] = None
    
    # Features and amenities
    amenities: List[str] = []
    features: List[str] = []
    
    # Media
    images: List[str] = []
    documents: List[str] = []
    video_url: Optional[str] = None
    virtual_tour_url: Optional[str] = None
    
    # Status and management
    status: PropertyStatus = PropertyStatus.PENDING
    is_featured: bool = False
    views: int = 0
    
    # Ownership
    created_by: str
    agent_id: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    class Settings:
        name = "properties"
        indexes = [
            "city",
            "property_type",
            "listing_type",
            "status",
            "price",
            "created_by",
            "created_at"
        ]


class Appointment(Document):
    property_id: str
    user_id: str
    agent_id: Optional[str] = None
    
    # Appointment details
    appointment_date: datetime
    appointment_time: str
    message: Optional[str] = None
    
    # Contact info
    name: str
    phone: str
    email: Optional[EmailStr] = None
    
    # Status
    status: AppointmentStatus = AppointmentStatus.PENDING
    notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    class Settings:
        name = "appointments"
        indexes = [
            "property_id",
            "user_id",
            "agent_id",
            "status",
            "appointment_date",
            "created_at"
        ]


class Contact(Document):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    subject: Optional[str] = None
    message: str
    
    # Optional property reference
    property_id: Optional[str] = None
    property_title: Optional[str] = None
    
    # User reference (if logged in)
    user_id: Optional[str] = None
    
    # Status and response
    status: ContactStatus = ContactStatus.PENDING
    response: Optional[str] = None
    responded_by: Optional[str] = None
    responded_at: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    class Settings:
        name = "contacts"
        indexes = [
            "status",
            "property_id",
            "user_id",
            "created_at"
        ]


class Inquiry(Document):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    message: str
    
    # Inquiry type and details
    inquiry_type: InquiryType = InquiryType.GENERAL
    property_id: Optional[str] = None
    property_title: Optional[str] = None
    
    # Budget and preferences (for property inquiries)
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    preferred_location: Optional[str] = None
    
    # User reference (if logged in)
    user_id: Optional[str] = None
    
    # Status and response
    status: ContactStatus = ContactStatus.PENDING
    response: Optional[str] = None
    responded_by: Optional[str] = None
    responded_at: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    class Settings:
        name = "inquiries"
        indexes = [
            "inquiry_type",
            "status",
            "property_id",
            "user_id",
            "created_at"
        ]