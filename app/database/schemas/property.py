from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.database.enums import PropertyType, ListingType, PropertyStatus


# Base schemas
class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    property_type: PropertyType
    listing_type: ListingType
    city: str
    state: str
    area: str
    pincode: Optional[str] = None


# Request schemas
class PropertyCreate(PropertyBase):
    # Property details
    carpet_area: Optional[float] = None
    built_area: Optional[float] = None
    plot_area: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    balconies: Optional[int] = None
    parking: Optional[int] = None
    floor_number: Optional[int] = None
    total_floors: Optional[int] = None
    
    # Features and amenities
    features: List[str] = []
    amenities: List[str] = []
    
    # Owner information
    owner_name: str
    owner_phone: str
    owner_email: Optional[str] = None


class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    property_type: Optional[PropertyType] = None
    listing_type: Optional[ListingType] = None
    city: Optional[str] = None
    state: Optional[str] = None
    area: Optional[str] = None
    pincode: Optional[str] = None
    carpet_area: Optional[float] = None
    built_area: Optional[float] = None
    plot_area: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    balconies: Optional[int] = None
    parking: Optional[int] = None
    floor_number: Optional[int] = None
    total_floors: Optional[int] = None
    features: Optional[List[str]] = None
    amenities: Optional[List[str]] = None


class PropertySearch(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    property_type: Optional[PropertyType] = None
    listing_type: Optional[ListingType] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None


# Response schemas
class PropertyResponse(PropertyBase):
    id: str
    carpet_area: Optional[float] = None
    built_area: Optional[float] = None
    plot_area: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    balconies: Optional[int] = None
    parking: Optional[int] = None
    floor_number: Optional[int] = None
    total_floors: Optional[int] = None
    features: List[str] = []
    amenities: List[str] = []
    images: List[str] = []
    videos: List[str] = []
    status: PropertyStatus
    is_featured: bool
    is_verified: bool
    views_count: int
    owner_name: str
    owner_phone: str
    owner_email: Optional[str] = None
    agent_name: Optional[str] = None
    agent_phone: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PropertyStats(BaseModel):
    total_properties: int
    pending_properties: int
    approved_properties: int
    featured_properties: int
    properties_by_type: dict
    properties_by_city: dict
    recent_listings: int


# Admin specific schemas
class AdminPropertyUpdate(BaseModel):
    status: Optional[PropertyStatus] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None