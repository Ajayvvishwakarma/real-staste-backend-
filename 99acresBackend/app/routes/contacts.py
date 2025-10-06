from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional
from bson import ObjectId
from datetime import datetime
from app.database.schemas.contact import (
    ContactCreate, ContactUpdate, ContactResponse, InquiryCreate, 
    InquiryResponse, CallbackRequest, ContactStats
)
from app.database.schemas.common import SuccessResponse, PaginatedResponse
from app.database.models import User, Contact, Inquiry, ContactStatus, InquiryType
from app.utils.dependencies import get_current_active_user, get_current_user_optional, get_admin_user

router = APIRouter()


@router.post("", response_model=SuccessResponse)
async def create_contact(
    contact_data: ContactCreate,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Create a new contact/inquiry"""
    contact_dict = contact_data.dict()
    
    # Set user_id if user is authenticated (keep as string)
    if current_user:
        contact_dict["user_id"] = str(current_user.id)
    
    # Keep property_id as string if provided (don't convert to ObjectId)
    # contact_data.property_id is already a string from the schema
    
    contact = Contact(**contact_dict)
    await contact.insert()
    
    return SuccessResponse(
        message="Contact inquiry submitted successfully",
        data={"contact_id": str(contact.id)}
    )


@router.post("/inquiries", response_model=SuccessResponse)
async def create_inquiry(
    inquiry_data: InquiryCreate,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Create a new property inquiry"""
    inquiry_dict = inquiry_data.dict()
    
    # Set user_id if user is authenticated (keep as string)
    if current_user:
        inquiry_dict["user_id"] = str(current_user.id)
    
    # Keep property_id as string if provided (don't convert to ObjectId)
    # inquiry_data.property_id is already a string from the schema
    
    inquiry = Inquiry(**inquiry_dict)
    await inquiry.insert()
    
    return SuccessResponse(
        message="Property inquiry submitted successfully",
        data={"inquiry_id": str(inquiry.id)}
    )


@router.post("/callback", response_model=SuccessResponse)
async def request_callback(
    callback_data: CallbackRequest,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Submit a callback request"""
    # Create as inquiry with callback type
    inquiry_dict = {
        "name": callback_data.name,
        "phone": callback_data.phone,
        "email": callback_data.email or "",
        "message": callback_data.message or f"Callback request. Preferred time: {callback_data.preferred_time or 'Anytime'}",
        "inquiry_type": InquiryType.CALLBACK_REQUEST
    }
    
    if current_user:
        inquiry_dict["user_id"] = str(current_user.id)
    
    if callback_data.property_id:
        # Keep property_id as string (don't convert to ObjectId)
        pass  # property_id is already set in inquiry_dict from callback_data.dict()
    
    inquiry = Inquiry(**inquiry_dict)
    await inquiry.insert()
    
    return SuccessResponse(
        message="Callback request submitted successfully",
        data={"callback_id": str(inquiry.id)}
    )


@router.get("", response_model=PaginatedResponse)
async def get_contacts(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[ContactStatus] = None,
    current_user: User = Depends(get_admin_user)
):
    """Get contacts list (Admin only)"""
    skip = (page - 1) * size
    
    query = {}
    if status:
        query["status"] = status
    
    contacts = await Contact.find(query).skip(skip).limit(size).to_list()
    total = await Contact.find(query).count()
    
    # Convert contacts to response format
    contacts_data = []
    for contact in contacts:
        contact_dict = contact.dict()
        contact_dict["id"] = str(contact.id)
        if contact.property_id:
            contact_dict["property_id"] = str(contact.property_id)
        if contact.user_id:
            contact_dict["user_id"] = str(contact.user_id)
        if contact.responded_by:
            contact_dict["responded_by"] = str(contact.responded_by)
        contacts_data.append(contact_dict)
    
    return PaginatedResponse(
        items=contacts_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/inquiries", response_model=PaginatedResponse)
async def get_inquiries(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    inquiry_type: Optional[InquiryType] = None,
    status: Optional[ContactStatus] = None,
    current_user: User = Depends(get_admin_user)
):
    """Get inquiries list (Admin only)"""
    skip = (page - 1) * size
    
    query = {}
    if inquiry_type:
        query["inquiry_type"] = inquiry_type
    if status:
        query["status"] = status
    
    inquiries = await Inquiry.find(query).skip(skip).limit(size).to_list()
    total = await Inquiry.find(query).count()
    
    # Convert inquiries to response format
    inquiries_data = []
    for inquiry in inquiries:
        inquiry_dict = inquiry.dict()
        inquiry_dict["id"] = str(inquiry.id)
        if inquiry.property_id:
            inquiry_dict["property_id"] = str(inquiry.property_id)
        if inquiry.user_id:
            inquiry_dict["user_id"] = str(inquiry.user_id)
        if inquiry.responded_by:
            inquiry_dict["responded_by"] = str(inquiry.responded_by)
        inquiries_data.append(inquiry_dict)
    
    return PaginatedResponse(
        items=inquiries_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/callbacks", response_model=PaginatedResponse)
async def get_callbacks(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[ContactStatus] = None,
    current_user: User = Depends(get_admin_user)
):
    """Get callback requests (Admin only)"""
    skip = (page - 1) * size
    
    query = {"inquiry_type": InquiryType.CALLBACK_REQUEST}
    if status:
        query["status"] = status
    
    callbacks = await Inquiry.find(query).skip(skip).limit(size).to_list()
    total = await Inquiry.find(query).count()
    
    # Convert callbacks to response format
    callbacks_data = []
    for callback in callbacks:
        callback_dict = callback.dict()
        callback_dict["id"] = str(callback.id)
        if callback.property_id:
            callback_dict["property_id"] = str(callback.property_id)
        if callback.user_id:
            callback_dict["user_id"] = str(callback.user_id)
        if callback.responded_by:
            callback_dict["responded_by"] = str(callback.responded_by)
        callbacks_data.append(callback_dict)
    
    return PaginatedResponse(
        items=callbacks_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/stats", response_model=ContactStats)
async def get_contact_stats(current_user: User = Depends(get_admin_user)):
    """Get contact statistics (Admin only)"""
    total_contacts = await Contact.find().count()
    pending_contacts = await Contact.find(Contact.status == ContactStatus.PENDING).count()
    resolved_contacts = await Contact.find(Contact.status == ContactStatus.RESOLVED).count()
    
    total_inquiries = await Inquiry.find().count()
    
    # Recent inquiries (last 30 days)
    from datetime import timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_inquiries = await Inquiry.find(
        Inquiry.created_at >= thirty_days_ago
    ).count()
    
    return ContactStats(
        total_contacts=total_contacts,
        pending_contacts=pending_contacts,
        resolved_contacts=resolved_contacts,
        total_inquiries=total_inquiries,
        recent_inquiries=recent_inquiries
    )


@router.put("/{contact_id}", response_model=SuccessResponse)
async def update_contact(
    contact_id: str,
    contact_update: ContactUpdate,
    current_user: User = Depends(get_admin_user)
):
    """Update contact (Admin only)"""
    try:
        contact = await Contact.get(ObjectId(contact_id))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    
    # Update contact
    update_data = contact_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    if update_data.get("response"):
        update_data["responded_by"] = str(current_user.id)  # Keep as string
        update_data["responded_at"] = datetime.utcnow()
    
    for key, value in update_data.items():
        setattr(contact, key, value)
    
    await contact.save()
    
    return SuccessResponse(message="Contact updated successfully")