from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from app.database.schemas.property import (
    PropertyCreate, PropertyUpdate, PropertyResponse, PropertySearch, 
    PropertyStats, AdminPropertyUpdate
)
from app.database.schemas.common import SuccessResponse, PaginatedResponse
from app.database.repositories.property_repository import PropertyRepository
from app.database.models import User, Property, PropertyType, ListingType, PropertyStatus, UserRole
from app.utils.dependencies import (
    get_current_active_user, get_current_user_optional, 
    get_admin_user, get_agent_or_admin_user
)

router = APIRouter()


def convert_property_to_response(property_obj: Property) -> dict:
    """Convert Property model to PropertyResponse dict with proper field mapping"""
    prop_dict = property_obj.dict()
    prop_dict["id"] = str(property_obj.id)
    
    # Map model fields to response schema fields
    prop_dict["area"] = property_obj.address or ""  # Map address to area for response
    prop_dict["carpet_area"] = property_obj.area_sqft  # Map area_sqft to carpet_area
    prop_dict["views_count"] = property_obj.views  # Map views to views_count
    prop_dict["is_verified"] = True  # Default value since not in model
    prop_dict["videos"] = []  # Default empty list since not in model
    
    # Add missing owner information
    # TODO: Fetch actual user data based on created_by field
    prop_dict["owner_name"] = "Property Owner"
    prop_dict["owner_phone"] = "Contact for details"
    prop_dict["owner_email"] = None
    prop_dict["agent_name"] = None
    prop_dict["agent_phone"] = None
    
    return prop_dict


@router.post("", response_model=SuccessResponse)
async def create_property(
    property_data: PropertyCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new property"""
    property_dict = property_data.dict()
    property_obj = await PropertyRepository.create_property(property_dict, str(current_user.id))
    
    return SuccessResponse(
        message="Property created successfully",
        data={"property_id": str(property_obj.id)}
    )


@router.get("", response_model=PaginatedResponse)
async def get_properties(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    city: Optional[str] = None,
    state: Optional[str] = None,
    property_type: Optional[PropertyType] = None,
    listing_type: Optional[ListingType] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    is_featured: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get properties list"""
    skip = (page - 1) * size
    
    # Only show approved properties for non-admin users
    status_filter = PropertyStatus.ACTIVE
    if current_user and current_user.role in ["admin", "super_admin"]:
        status_filter = None
    
    properties = await PropertyRepository.get_properties(
        skip=skip,
        limit=size,
        city=city,
        state=state,
        property_type=property_type,
        listing_type=listing_type,
        status=status_filter,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        is_featured=is_featured,
        search=search
    )
    
    total = await PropertyRepository.count_properties(
        city=city,
        state=state,
        property_type=property_type,
        listing_type=listing_type,
        status=status_filter
    )
    
    # Convert properties to response format
    properties_data = []
    for prop in properties:
        prop_dict = prop.dict()
        prop_dict["id"] = str(prop.id)
        properties_data.append(prop_dict)
    
    return PaginatedResponse(
        items=properties_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/my-properties", response_model=PaginatedResponse)
async def get_my_properties(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's properties"""
    skip = (page - 1) * size
    
    properties = await PropertyRepository.get_properties(
        skip=skip,
        limit=size,
        owner_id=str(current_user.id)
    )
    
    total = await PropertyRepository.count_properties(owner_id=str(current_user.id))
    
    # Convert properties to response format
    properties_data = []
    for prop in properties:
        prop_dict = prop.dict()
        prop_dict["id"] = str(prop.id)
        properties_data.append(prop_dict)
    
    return PaginatedResponse(
        items=properties_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/stats", response_model=PropertyStats)
async def get_property_stats(current_user: User = Depends(get_current_active_user)):
    """Get property statistics (Staff, Agent, Admin access)"""
    # Check permissions - use string values since role is stored as string
    if current_user.role not in ["staff", "agent", "admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    stats = await PropertyRepository.get_property_stats()
    return PropertyStats(**stats)


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get property by ID"""
    property_obj = await PropertyRepository.get_property_by_id(property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check if user can view this property
    if property_obj.status != PropertyStatus.ACTIVE:
        if not current_user or (
            str(current_user.id) != str(property_obj.created_by) and 
            current_user.role not in ["admin", "super_admin"]
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
    
    # Increment views count
    await PropertyRepository.increment_views(property_id)
    
    # Convert to response format
    prop_dict = convert_property_to_response(property_obj)
    return PropertyResponse(**prop_dict)


@router.put("/{property_id}", response_model=SuccessResponse)
async def update_property(
    property_id: str,
    property_update: PropertyUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update property"""
    property_obj = await PropertyRepository.get_property_by_id(property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check if user can update this property
    if (str(current_user.id) != str(property_obj.owner_id) and 
        current_user.role not in ["admin", "super_admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    update_data = property_update.dict(exclude_unset=True)
    updated_property = await PropertyRepository.update_property(property_id, update_data)
    
    if not updated_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return SuccessResponse(message="Property updated successfully")


@router.delete("/{property_id}", response_model=SuccessResponse)
async def delete_property(
    property_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete property"""
    property_obj = await PropertyRepository.get_property_by_id(property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check if user can delete this property
    if (str(current_user.id) != str(property_obj.owner_id) and 
        current_user.role not in ["admin", "super_admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    success = await PropertyRepository.delete_property(property_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return SuccessResponse(message="Property deleted successfully")


@router.post("/search", response_model=PaginatedResponse)
async def search_properties(
    search_data: PropertySearch,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Search properties"""
    skip = (page - 1) * size
    
    properties = await PropertyRepository.get_properties(
        skip=skip,
        limit=size,
        city=search_data.city,
        state=search_data.state,
        property_type=search_data.property_type,
        listing_type=search_data.listing_type,
        status=PropertyStatus.ACTIVE,
        min_price=search_data.min_price,
        max_price=search_data.max_price,
        bedrooms=search_data.bedrooms
    )
    
    total = await PropertyRepository.count_properties(
        city=search_data.city,
        state=search_data.state,
        property_type=search_data.property_type,
        listing_type=search_data.listing_type,
        status=PropertyStatus.ACTIVE
    )
    
    # Convert properties to response format
    properties_data = []
    for prop in properties:
        prop_dict = prop.dict()
        prop_dict["id"] = str(prop.id)
        properties_data.append(prop_dict)
    
    return PaginatedResponse(
        items=properties_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )