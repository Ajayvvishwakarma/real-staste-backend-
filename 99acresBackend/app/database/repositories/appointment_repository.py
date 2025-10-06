from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.database.sqlite_models import Appointment, User
from app.database.enums import AppointmentStatus
from app.database.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentRepository:
    @staticmethod
    async def create_appointment(appointment_data: AppointmentCreate, user_id: ObjectId) -> Appointment:
        """Create a new appointment"""
        appointment_dict = appointment_data.dict()
        appointment_dict["user_id"] = user_id
        
        # Convert property_id and agent_id to ObjectId if provided
        if appointment_data.property_id:
            appointment_dict["property_id"] = ObjectId(appointment_data.property_id)
        if appointment_data.agent_id:
            appointment_dict["agent_id"] = ObjectId(appointment_data.agent_id)
        
        appointment = Appointment(**appointment_dict)
        return await appointment.insert()
    
    @staticmethod
    async def get_appointment_by_id(appointment_id: ObjectId) -> Optional[Appointment]:
        """Get appointment by ID"""
        return await Appointment.get(appointment_id)
    
    @staticmethod
    async def get_appointments_by_user(
        user_id: ObjectId, 
        skip: int = 0, 
        limit: int = 20,
        status: Optional[AppointmentStatus] = None
    ) -> List[Appointment]:
        """Get appointments for a user"""
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        
        return await Appointment.find(query).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def get_appointments_by_agent(
        agent_id: ObjectId,
        skip: int = 0,
        limit: int = 20,
        status: Optional[AppointmentStatus] = None
    ) -> List[Appointment]:
        """Get appointments for an agent"""
        query = {"agent_id": agent_id}
        if status:
            query["status"] = status
        
        return await Appointment.find(query).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def get_all_appointments(
        skip: int = 0,
        limit: int = 20,
        status: Optional[AppointmentStatus] = None
    ) -> List[Appointment]:
        """Get all appointments (admin only)"""
        query = {}
        if status:
            query["status"] = status
        
        return await Appointment.find(query).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def update_appointment(appointment_id: ObjectId, update_data: AppointmentUpdate) -> Optional[Appointment]:
        """Update an appointment"""
        appointment = await Appointment.get(appointment_id)
        if not appointment:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()
        
        for key, value in update_dict.items():
            setattr(appointment, key, value)
        
        await appointment.save()
        return appointment
    
    @staticmethod
    async def update_appointment_status(appointment_id: ObjectId, status: AppointmentStatus) -> Optional[Appointment]:
        """Update appointment status"""
        appointment = await Appointment.get(appointment_id)
        if not appointment:
            return None
        
        appointment.status = status
        appointment.updated_at = datetime.utcnow()
        
        await appointment.save()
        return appointment
    
    @staticmethod
    async def delete_appointment(appointment_id: ObjectId) -> bool:
        """Delete an appointment"""
        appointment = await Appointment.get(appointment_id)
        if not appointment:
            return False
        
        await appointment.delete()
        return True
    
    @staticmethod
    async def count_appointments_by_user(user_id: ObjectId, status: Optional[AppointmentStatus] = None) -> int:
        """Count appointments for a user"""
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        
        return await Appointment.find(query).count()
    
    @staticmethod
    async def count_appointments_by_agent(agent_id: ObjectId, status: Optional[AppointmentStatus] = None) -> int:
        """Count appointments for an agent"""
        query = {"agent_id": agent_id}
        if status:
            query["status"] = status
        
        return await Appointment.find(query).count()
    
    @staticmethod
    async def count_all_appointments(status: Optional[AppointmentStatus] = None) -> int:
        """Count all appointments"""
        query = {}
        if status:
            query["status"] = status
        
        return await Appointment.find(query).count()
    
    @staticmethod
    async def get_appointments_by_property(property_id: ObjectId) -> List[Appointment]:
        """Get appointments for a specific property"""
        return await Appointment.find(Appointment.property_id == property_id).to_list()
    
    @staticmethod
    async def get_upcoming_appointments(user_id: ObjectId, limit: int = 5) -> List[Appointment]:
        """Get upcoming appointments for a user"""
        now = datetime.utcnow()
        return await Appointment.find({
            "user_id": user_id,
            "appointment_date": {"$gte": now},
            "status": {"$in": [AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]}
        }).sort(Appointment.appointment_date).limit(limit).to_list()
    
    @staticmethod
    async def get_agent_upcoming_appointments(agent_id: ObjectId, limit: int = 5) -> List[Appointment]:
        """Get upcoming appointments for an agent"""
        now = datetime.utcnow()
        return await Appointment.find({
            "agent_id": agent_id,
            "appointment_date": {"$gte": now},
            "status": {"$in": [AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]}
        }).sort(Appointment.appointment_date).limit(limit).to_list()