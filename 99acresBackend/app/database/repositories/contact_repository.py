from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.database.sqlite_models import Contact, Inquiry
from app.database.enums import ContactStatus, InquiryType
from app.database.schemas.contact import ContactCreate, ContactUpdate, InquiryCreate


class ContactRepository:
    @staticmethod
    async def create_contact(contact_data: ContactCreate, user_id: Optional[ObjectId] = None) -> Contact:
        """Create a new contact"""
        contact_dict = contact_data.dict()
        
        if user_id:
            contact_dict["user_id"] = user_id
        
        if contact_data.property_id:
            contact_dict["property_id"] = ObjectId(contact_data.property_id)
        
        contact = Contact(**contact_dict)
        return await contact.insert()
    
    @staticmethod
    async def get_contact_by_id(contact_id: ObjectId) -> Optional[Contact]:
        """Get contact by ID"""
        return await Contact.get(contact_id)
    
    @staticmethod
    async def get_all_contacts(
        skip: int = 0,
        limit: int = 20,
        status: Optional[ContactStatus] = None
    ) -> List[Contact]:
        """Get all contacts"""
        query = {}
        if status:
            query["status"] = status
        
        return await Contact.find(query).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def update_contact(contact_id: ObjectId, update_data: ContactUpdate) -> Optional[Contact]:
        """Update a contact"""
        contact = await Contact.get(contact_id)
        if not contact:
            return None
        
        update_dict = update_data.dict(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()
        
        for key, value in update_dict.items():
            setattr(contact, key, value)
        
        await contact.save()
        return contact
    
    @staticmethod
    async def delete_contact(contact_id: ObjectId) -> bool:
        """Delete a contact"""
        contact = await Contact.get(contact_id)
        if not contact:
            return False
        
        await contact.delete()
        return True
    
    @staticmethod
    async def count_contacts(status: Optional[ContactStatus] = None) -> int:
        """Count contacts"""
        query = {}
        if status:
            query["status"] = status
        
        return await Contact.find(query).count()
    
    @staticmethod
    async def get_contacts_by_property(property_id: ObjectId) -> List[Contact]:
        """Get contacts for a specific property"""
        return await Contact.find(Contact.property_id == property_id).to_list()


class InquiryRepository:
    @staticmethod
    async def create_inquiry(inquiry_data: InquiryCreate, user_id: Optional[ObjectId] = None) -> Inquiry:
        """Create a new inquiry"""
        inquiry_dict = inquiry_data.dict()
        
        if user_id:
            inquiry_dict["user_id"] = user_id
        
        if inquiry_data.property_id:
            inquiry_dict["property_id"] = ObjectId(inquiry_data.property_id)
        
        inquiry = Inquiry(**inquiry_dict)
        return await inquiry.insert()
    
    @staticmethod
    async def get_inquiry_by_id(inquiry_id: ObjectId) -> Optional[Inquiry]:
        """Get inquiry by ID"""
        return await Inquiry.get(inquiry_id)
    
    @staticmethod
    async def get_all_inquiries(
        skip: int = 0,
        limit: int = 20,
        inquiry_type: Optional[InquiryType] = None,
        status: Optional[ContactStatus] = None
    ) -> List[Inquiry]:
        """Get all inquiries"""
        query = {}
        if inquiry_type:
            query["inquiry_type"] = inquiry_type
        if status:
            query["status"] = status
        
        return await Inquiry.find(query).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def get_inquiries_by_user(
        user_id: ObjectId,
        skip: int = 0,
        limit: int = 20
    ) -> List[Inquiry]:
        """Get inquiries by user"""
        return await Inquiry.find(Inquiry.user_id == user_id).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def update_inquiry_status(inquiry_id: ObjectId, status: ContactStatus) -> Optional[Inquiry]:
        """Update inquiry status"""
        inquiry = await Inquiry.get(inquiry_id)
        if not inquiry:
            return None
        
        inquiry.status = status
        inquiry.updated_at = datetime.utcnow()
        
        await inquiry.save()
        return inquiry
    
    @staticmethod
    async def delete_inquiry(inquiry_id: ObjectId) -> bool:
        """Delete an inquiry"""
        inquiry = await Inquiry.get(inquiry_id)
        if not inquiry:
            return False
        
        await inquiry.delete()
        return True
    
    @staticmethod
    async def count_inquiries(
        inquiry_type: Optional[InquiryType] = None,
        status: Optional[ContactStatus] = None
    ) -> int:
        """Count inquiries"""
        query = {}
        if inquiry_type:
            query["inquiry_type"] = inquiry_type
        if status:
            query["status"] = status
        
        return await Inquiry.find(query).count()
    
    @staticmethod
    async def get_inquiries_by_property(property_id: ObjectId) -> List[Inquiry]:
        """Get inquiries for a specific property"""
        return await Inquiry.find(Inquiry.property_id == property_id).to_list()
    
    @staticmethod
    async def get_callback_requests(
        skip: int = 0,
        limit: int = 20,
        status: Optional[ContactStatus] = None
    ) -> List[Inquiry]:
        """Get callback requests"""
        query = {"inquiry_type": InquiryType.CALLBACK_REQUEST}
        if status:
            query["status"] = status
        
        return await Inquiry.find(query).skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def count_callback_requests(status: Optional[ContactStatus] = None) -> int:
        """Count callback requests"""
        query = {"inquiry_type": InquiryType.CALLBACK_REQUEST}
        if status:
            query["status"] = status
        
        return await Inquiry.find(query).count()
    
    @staticmethod
    async def get_recent_inquiries(limit: int = 10) -> List[Inquiry]:
        """Get recent inquiries"""
        return await Inquiry.find().sort(-Inquiry.created_at).limit(limit).to_list()