from enum import Enum

class UserRole(str, Enum):
    CLIENT = "CLIENT"
    AGENT = "AGENT"
    ADMIN = "ADMIN"

class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    VILLA = "villa"
    COMMERCIAL = "commercial"
    PLOT = "plot"

class ListingType(str, Enum):
    SALE = "sale"
    RENT = "rent"

class PropertyStatus(str, Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    RENTED = "rented"
    UNDER_NEGOTIATION = "under_negotiation"

class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ContactStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class InquiryType(str, Enum):
    GENERAL = "general"
    PROPERTY_SPECIFIC = "property_specific"
    INVESTMENT = "investment"