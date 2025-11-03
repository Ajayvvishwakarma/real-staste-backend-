# Campaign models for MongoDB
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.database.mongo_models import PyObjectId

class Campaign(BaseModel):
    """Campaign model for MongoDB"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: Optional[str] = None
    campaignName: Optional[str] = None
    description: Optional[str] = None
    status: str = "draft"  # draft, active, paused, completed, archived
    campaign_type: str = "email"  # marketing, email, sms, social_media
    
    # Email campaign specific fields
    subject: Optional[str] = None
    emailContent: Optional[str] = None
    recipientList: Optional[List[str]] = []
    recipients: Optional[int] = None
    emailsSent: Optional[int] = 0
    emailsOpened: Optional[int] = 0
    emailsClicked: Optional[int] = 0
    openRate: Optional[float] = 0.0
    clickRate: Optional[float] = 0.0
    
    # Regular campaign fields
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = 0.0
    spent: Optional[float] = 0.0
    target_audience: Optional[str] = None
    platform: Optional[str] = None  # facebook, google, instagram, email, sms
    
    # Performance metrics
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    leads_generated: int = 0
    
    # Additional data
    tags: List[str] = []
    owner_id: Optional[str] = None
    created_by: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    createdAt: Optional[datetime] = None  # For frontend compatibility
    updated_at: Optional[datetime] = None
    updatedAt: Optional[datetime] = None  # For frontend compatibility
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str, datetime: lambda v: v.isoformat() if v else None}
    }

class CampaignCreate(BaseModel):
    """Schema for creating a campaign"""
    name: Optional[str] = None
    campaignName: Optional[str] = None
    description: Optional[str] = None
    status: str = "draft"
    campaign_type: str = "email"
    
    # Email campaign specific fields
    subject: Optional[str] = None
    emailContent: Optional[str] = None
    recipientList: Optional[List[str]] = []
    recipients: Optional[int] = None
    
    # Regular campaign fields
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = 0.0
    target_audience: Optional[str] = None
    platform: Optional[str] = None
    tags: List[str] = []
    
    # Accept createdAt from frontend but don't use it (will use server time)
    createdAt: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }

class CampaignUpdate(BaseModel):
    """Schema for updating a campaign"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    campaign_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    spent: Optional[float] = None
    target_audience: Optional[str] = None
    platform: Optional[str] = None
    impressions: Optional[int] = None
    clicks: Optional[int] = None
    conversions: Optional[int] = None
    leads_generated: Optional[int] = None
    tags: Optional[List[str]] = None

class CampaignStats(BaseModel):
    """Campaign statistics"""
    total_campaigns: int = 0
    active_campaigns: int = 0
    paused_campaigns: int = 0
    completed_campaigns: int = 0
    total_budget: float = 0.0
    total_spent: float = 0.0
    total_impressions: int = 0
    total_clicks: int = 0
    total_conversions: int = 0
    total_leads: int = 0
    avg_click_rate: float = 0.0
    avg_conversion_rate: float = 0.0
