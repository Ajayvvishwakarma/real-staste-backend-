from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="client")  # client, agent, admin
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    profile_picture = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    
    # Agent specific fields
    agent_id = Column(String, nullable=True)
    commission_rate = Column(Float, nullable=True)
    
    # Relationships
    properties = relationship("Property", back_populates="owner")
    appointments = relationship("Appointment", back_populates="user")
    contacts = relationship("Contact", back_populates="user")
    campaigns = relationship("EmailCampaign", back_populates="creator")


class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    property_type = Column(String, nullable=False)  # apartment, house, commercial, etc.
    price = Column(Float, nullable=False)
    area = Column(Float, nullable=True)  # in sq ft
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    furnished_status = Column(String, nullable=True)  # furnished, semi-furnished, unfurnished
    
    # Location
    address = Column(Text, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Status
    status = Column(String, default="available")  # available, sold, rented
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    appointments = relationship("Appointment", back_populates="property")


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String, default="pending")  # pending, confirmed, cancelled, completed
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="appointments")
    property = relationship("Property", back_populates="appointments")


class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    subject = Column(String, nullable=True)
    
    # Optional user association
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Status
    status = Column(String, default="new")  # new, in_progress, resolved
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="contacts")


class Inquiry(Base):
    __tablename__ = "inquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    property_type = Column(String, nullable=False)
    budget = Column(Float, nullable=True)
    location = Column(String, nullable=False)
    message = Column(Text, nullable=True)
    
    status = Column(String, default="new")  # new, in_progress, resolved
    
    created_at = Column(DateTime, default=datetime.utcnow)


class EmailCampaign(Base):
    __tablename__ = "email_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    recipients = Column(Integer, nullable=False)
    status = Column(String, default="active")  # active, completed, draft, cancelled
    total_sent = Column(Integer, default=0)
    total_opened = Column(Integer, default=0)
    open_rate = Column(Float, default=0.0)
    
    # Optional user association (who created the campaign)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    creator = relationship("User", back_populates="campaigns")
    email_logs = relationship("EmailLog", back_populates="campaign")


class EmailTemplate(Base):
    __tablename__ = "email_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    template = Column(Text, nullable=False)
    type = Column(String, nullable=False)  # welcome, property_alert, appointment, etc.
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)


class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("email_campaigns.id"), nullable=True)
    template_id = Column(Integer, ForeignKey("email_templates.id"), nullable=True)
    
    to_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String, default="sent")  # sent, delivered, bounced, failed, opened
    
    sent_at = Column(DateTime, default=datetime.utcnow)
    opened_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    campaign = relationship("EmailCampaign", back_populates="email_logs")
    template = relationship("EmailTemplate")