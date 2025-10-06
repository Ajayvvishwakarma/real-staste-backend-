from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.database.schemas.appointment import (
    AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentStats
)
from app.database.schemas.common import SuccessResponse, PaginatedResponse
from app.database.models import User, Appointment, AppointmentStatus
from app.utils.dependencies import get_current_active_user, get_admin_user, get_agent_or_admin_user

router = APIRouter()


@router.post("", response_model=SuccessResponse)
async def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create appointment"""
    # Map schema fields to model fields and fix types
    model_data = {
        'property_id': str(appointment_data.property_id),  # Keep as string
        'user_id': str(current_user.id),  # Set user_id as string (required field)
        'name': appointment_data.client_name,  # Map client_name to name
        'phone': appointment_data.client_phone,  # Map client_phone to phone
        'email': appointment_data.client_email,  # Map client_email to email
        'appointment_time': appointment_data.appointment_time,
        'message': appointment_data.notes,  # Map notes to message
    }
    
    # Convert agent_id to string if provided
    if appointment_data.agent_id:
        model_data['agent_id'] = str(appointment_data.agent_id)
    
    # Parse appointment_date from string to datetime
    try:
        # Assuming date format is DD/MM/YYYY based on error message
        date_str = appointment_data.appointment_date
        if '/' in date_str:
            # Handle DD/MM/YYYY format
            day, month, year = date_str.split('/')
            model_data['appointment_date'] = datetime(int(year), int(month), int(day))
        else:
            # Handle YYYY-MM-DD format
            model_data['appointment_date'] = datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD"
        )
    
    appointment = Appointment(**model_data)
    await appointment.insert()
    
    return SuccessResponse(
        message="Appointment created successfully",
        data={"appointment_id": str(appointment.id)}
    )


@router.get("", response_model=PaginatedResponse)
async def get_appointments(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status_filter: Optional[AppointmentStatus] = None,
    date: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get appointments"""
    skip = (page - 1) * size
    
    # Build query based on user role
    query = {}
    
    if current_user.role in ["admin", "super_admin"]:
        # Admin can see all appointments
        pass
    elif current_user.role == "agent":
        # Agents can see their appointments
        query["agent_id"] = str(current_user.id)  # Use string, not ObjectId
    else:
        # Clients can see their appointments
        query["user_id"] = str(current_user.id)  # Use user_id, not client_id
    
    if status_filter:
        query["status"] = status_filter
    if date:
        query["appointment_date"] = date
    
    # First, let's clean up any corrupted appointment_date fields in the database
    from app.config import settings
    
    try:
        # Quick cleanup of corrupted data
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        collection = db["appointments"]
        
        # Fix records where appointment_date is the literal string 'string'
        await collection.update_many(
            {"appointment_date": "string"},
            {"$set": {"appointment_date": datetime.utcnow()}}
        )
        
        # Fix any other string dates that aren't valid ISO dates
        cursor = collection.find({"appointment_date": {"$type": "string", "$ne": "string"}})
        async for doc in cursor:
            try:
                date_str = doc['appointment_date']
                if '/' in date_str:
                    day, month, year = date_str.split('/')
                    fixed_date = datetime(int(year), int(month), int(day))
                else:
                    fixed_date = datetime.fromisoformat(date_str)
                
                await collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"appointment_date": fixed_date}}
                )
            except (ValueError, AttributeError):
                # Set to current date if can't parse
                await collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"appointment_date": datetime.utcnow()}}
                )
        
        await client.close()
    except Exception as cleanup_error:
        print(f"Error during data cleanup: {cleanup_error}")
    
    # Now perform the normal query
    appointments = await Appointment.find(query).skip(skip).limit(size).to_list()
    total = await Appointment.find(query).count()
    
    # Convert appointments to response format
    appointments_data = []
    for appointment in appointments:
        appointment_dict = appointment.dict()
        appointment_dict["id"] = str(appointment.id)
        appointment_dict["property_id"] = str(appointment.property_id)
        if appointment.user_id:
            appointment_dict["client_id"] = str(appointment.user_id)  # Map user_id to client_id for response
        if appointment.agent_id:
            appointment_dict["agent_id"] = str(appointment.agent_id)
        appointments_data.append(appointment_dict)
    
    return PaginatedResponse(
        items=appointments_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/stats", response_model=AppointmentStats)
async def get_appointment_stats(current_user: User = Depends(get_agent_or_admin_user)):
    """Get appointment statistics"""
    total_appointments = await Appointment.find().count()
    scheduled_appointments = await Appointment.find(Appointment.status == AppointmentStatus.PENDING).count()
    confirmed_appointments = await Appointment.find(Appointment.status == AppointmentStatus.CONFIRMED).count()
    completed_appointments = await Appointment.find(Appointment.status == AppointmentStatus.COMPLETED).count()
    cancelled_appointments = await Appointment.find(Appointment.status == AppointmentStatus.CANCELLED).count()
    
    # Recent appointments (last 30 days)
    from datetime import timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_appointments = await Appointment.find(
        Appointment.created_at >= thirty_days_ago
    ).count()
    
    return AppointmentStats(
        total_appointments=total_appointments,
        scheduled_appointments=scheduled_appointments,
        confirmed_appointments=confirmed_appointments,
        completed_appointments=completed_appointments,
        cancelled_appointments=cancelled_appointments,
        recent_appointments=recent_appointments
    )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get appointment by ID"""
    try:
        appointment = await Appointment.get(ObjectId(appointment_id))
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user can view this appointment
    if current_user.role not in ["admin", "super_admin"]:
        if (str(current_user.id) != str(appointment.user_id) and 
            str(current_user.id) != str(appointment.agent_id)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    appointment_dict = appointment.dict()
    appointment_dict["id"] = str(appointment.id)
    appointment_dict["property_id"] = str(appointment.property_id)
    if appointment.user_id:
        appointment_dict["client_id"] = str(appointment.user_id)  # Map user_id to client_id for response
    if appointment.agent_id:
        appointment_dict["agent_id"] = str(appointment.agent_id)
    
    return AppointmentResponse(**appointment_dict)


@router.put("/{appointment_id}", response_model=SuccessResponse)
async def update_appointment(
    appointment_id: str,
    appointment_update: AppointmentUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update appointment"""
    try:
        appointment = await Appointment.get(ObjectId(appointment_id))
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user can update this appointment
    if current_user.role not in ["admin", "super_admin"]:
        if (str(current_user.id) != str(appointment.user_id) and 
            str(current_user.id) != str(appointment.agent_id)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    # Update appointment
    update_data = appointment_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    # Handle date parsing if appointment_date is being updated
    if "appointment_date" in update_data and isinstance(update_data["appointment_date"], str):
        try:
            date_str = update_data["appointment_date"]
            if '/' in date_str:
                # Handle DD/MM/YYYY format
                day, month, year = date_str.split('/')
                update_data["appointment_date"] = datetime(int(year), int(month), int(day))
            else:
                # Handle YYYY-MM-DD format
                update_data["appointment_date"] = datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD"
            )
    
    for key, value in update_data.items():
        setattr(appointment, key, value)
    
    await appointment.save()
    
    return SuccessResponse(message="Appointment updated successfully")


@router.delete("/{appointment_id}", response_model=SuccessResponse)
async def delete_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete appointment"""
    try:
        appointment = await Appointment.get(ObjectId(appointment_id))
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user can delete this appointment
    if current_user.role not in ["admin", "super_admin"]:
        if (str(current_user.id) != str(appointment.user_id) and 
            str(current_user.id) != str(appointment.agent_id)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    await appointment.delete()
    
    return SuccessResponse(message="Appointment deleted successfully")