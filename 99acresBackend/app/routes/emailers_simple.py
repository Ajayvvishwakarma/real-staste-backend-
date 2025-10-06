from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for request/response
class EmailSendRequest(BaseModel):
    name: str
    subject: str
    recipients: int
    body: str

class EmailTemplateRequest(BaseModel):
    name: str
    subject: str
    template: str
    type: str
    is_active: bool = True

class CampaignCreateRequest(BaseModel):
    name: str
    subject: str
    recipients: int
    body: str
    template_id: Optional[int] = None

@router.get("/", response_model=dict)
async def get_emailers_info():
    """Get emailers module information and dashboard"""
    return {
        "success": True,
        "message": "Email Management API",
        "dashboard": {
            "total_campaigns": EMAIL_STATS["total_campaigns"],
            "active_campaigns": EMAIL_STATS["active_campaigns"], 
            "total_emails_sent": EMAIL_STATS["total_emails_sent"],
            "open_rate": f"{EMAIL_STATS['overall_open_rate']}%"
        },
        "recent_campaigns": CAMPAIGNS_STORAGE[-3:] if CAMPAIGNS_STORAGE else [],
        "available_endpoints": {
            "dashboard": "/api/emailers/dashboard",
            "campaigns": "/api/emailers/campaigns",
            "templates": "/api/emailers/templates",
            "logs": "/api/emailers/logs", 
            "stats": "/api/emailers/stats",
            "send": "/api/emailers/send (POST)",
            "create_template": "/api/emailers/templates (POST)"
        }
    }

@router.post("/", response_model=dict)
async def send_email_direct(email_data: EmailSendRequest):
    """Send email directly from main emailers endpoint - this creates a campaign"""
    global EMAIL_STATS
    
    # Create new campaign
    new_campaign = {
        "id": len(CAMPAIGNS_STORAGE) + 1,
        "name": email_data.name,
        "subject": email_data.subject,
        "recipients": email_data.recipients,
        "status": "active",
        "sent_date": "2025-10-01",
        "open_rate": 0.0,  # Initial open rate
        "total_sent": email_data.recipients,
        "total_opened": 0,
        "created_at": "2025-10-01T12:50:00Z"
    }
    
    # Add to persistent storage
    CAMPAIGNS_STORAGE.append(new_campaign)
    
    # Update stats
    EMAIL_STATS["total_campaigns"] = len(CAMPAIGNS_STORAGE)
    EMAIL_STATS["active_campaigns"] = len([c for c in CAMPAIGNS_STORAGE if c["status"] == "active"])
    EMAIL_STATS["total_emails_sent"] = sum(c["total_sent"] for c in CAMPAIGNS_STORAGE)
    
    return {
        "success": True,
        "message": "Campaign created and email sent successfully",
        "data": {
            "campaign_id": new_campaign["id"],
            "email_id": f"email_{new_campaign['id']:03d}",
            "campaign_name": email_data.name,
            "subject": email_data.subject,
            "recipients_count": email_data.recipients,
            "body_preview": email_data.body[:50] + "..." if len(email_data.body) > 50 else email_data.body,
            "status": "sent",
            "sent_at": "2025-10-01T12:50:00Z"
        }
    }

@router.get("/campaigns", response_model=dict)
async def get_campaigns():
    """Get all email campaigns"""
    return {
        "success": True,
        "message": "Campaigns retrieved successfully",
        "data": CAMPAIGNS_STORAGE,
        "count": len(CAMPAIGNS_STORAGE)
    }

@router.get("/dashboard", response_model=dict)  
async def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        "success": True,
        "message": "Dashboard stats retrieved successfully",
        "data": {
            "total_campaigns": EMAIL_STATS["total_campaigns"],
            "active_campaigns": EMAIL_STATS["active_campaigns"], 
            "total_emails_sent": EMAIL_STATS["total_emails_sent"],
            "open_rate": f"{EMAIL_STATS['overall_open_rate']}%",
            "campaigns": CAMPAIGNS_STORAGE
        }
    }

@router.get("/campaigns/{campaign_id}", response_model=dict)
async def get_campaign(campaign_id: int):
    """Get single campaign details"""
    campaign = next((c for c in CAMPAIGNS_STORAGE if c["id"] == campaign_id), None)
    
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail=f"Campaign with ID {campaign_id} not found"
        )
    
    return {
        "success": True,
        "message": "Campaign retrieved successfully",
        "data": campaign
    }

@router.post("/campaigns/{campaign_id}/duplicate", response_model=dict)
async def duplicate_campaign(campaign_id: int):
    """Duplicate a campaign"""
    original = next((c for c in CAMPAIGNS_STORAGE if c["id"] == campaign_id), None)
    
    if not original:
        raise HTTPException(
            status_code=404,
            detail=f"Campaign with ID {campaign_id} not found"
        )
    
    # Create duplicate
    duplicate = original.copy()
    duplicate["id"] = len(CAMPAIGNS_STORAGE) + 1
    duplicate["name"] = f"{original['name']} (Copy)"
    duplicate["status"] = "draft"
    duplicate["sent_date"] = None
    duplicate["total_opened"] = 0
    duplicate["open_rate"] = 0.0
    duplicate["created_at"] = "2025-10-01T12:50:00Z"
    
    CAMPAIGNS_STORAGE.append(duplicate)
    
    return {
        "success": True,
        "message": "Campaign duplicated successfully",
        "data": duplicate
    }

@router.put("/campaigns/{campaign_id}", response_model=dict)
async def update_campaign(campaign_id: int):
    """Edit/Update a campaign"""
    campaign = next((c for c in CAMPAIGNS_STORAGE if c["id"] == campaign_id), None)
    
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail=f"Campaign with ID {campaign_id} not found"
        )
    
    return {
        "success": True,
        "message": f"Campaign {campaign_id} update endpoint ready - SQLite integration in progress",
        "data": campaign
    }

@router.delete("/campaigns/{campaign_id}", response_model=dict)
async def delete_campaign(campaign_id: int):
    """Delete a campaign"""
    global CAMPAIGNS_STORAGE, EMAIL_STATS
    
    campaign_index = next((i for i, c in enumerate(CAMPAIGNS_STORAGE) if c["id"] == campaign_id), None)
    
    if campaign_index is None:
        raise HTTPException(
            status_code=404,
            detail=f"Campaign with ID {campaign_id} not found"
        )
    
    deleted_campaign = CAMPAIGNS_STORAGE.pop(campaign_index)
    
    # Update stats
    EMAIL_STATS["total_campaigns"] = len(CAMPAIGNS_STORAGE)
    EMAIL_STATS["active_campaigns"] = len([c for c in CAMPAIGNS_STORAGE if c["status"] == "active"])
    EMAIL_STATS["total_emails_sent"] = sum(c["total_sent"] for c in CAMPAIGNS_STORAGE)
    
    return {
        "success": True,
        "message": f"Campaign '{deleted_campaign['name']}' deleted successfully",
        "data": {"deleted_campaign_id": campaign_id}
    }
async def get_emailers_info():
    """Get emailers module information"""
    return {
        "success": True,
        "message": "Email Management API",
        "available_endpoints": {
            "templates": "/api/emailers/templates",
            "logs": "/api/emailers/logs", 
            "stats": "/api/emailers/stats",
            "send": "/api/emailers/send (POST)",
            "create_template": "/api/emailers/templates (POST)"
        }
    }

# Persistent campaign data (in real app, this would be in database)
CAMPAIGNS_STORAGE = [
    {
        "id": 1,
        "name": "Welcome Campaign",
        "subject": "Welcome to 99Acres!",
        "recipients": 150,
        "status": "active",
        "sent_date": "2025-10-01",
        "open_rate": 85.5,
        "total_sent": 150,
        "total_opened": 128,
        "created_at": "2025-10-01T10:00:00Z"
    },
    {
        "id": 2,
        "name": "Property Alert Campaign", 
        "subject": "New Properties Available",
        "recipients": 200,
        "status": "completed",
        "sent_date": "2025-09-30",
        "open_rate": 76.3,
        "total_sent": 200,
        "total_opened": 153,
        "created_at": "2025-09-30T15:30:00Z"
    }
]

# Global counters for persistent stats
EMAIL_STATS = {
    "total_campaigns": len(CAMPAIGNS_STORAGE),
    "active_campaigns": len([c for c in CAMPAIGNS_STORAGE if c["status"] == "active"]),
    "total_emails_sent": sum(c["total_sent"] for c in CAMPAIGNS_STORAGE),
    "overall_open_rate": 80.9
}
SAMPLE_EMAIL_TEMPLATES = [
    {
        "id": 1,
        "name": "Welcome Email",
        "subject": "Welcome to 99Acres!",
        "template": "Hello {{name}}, Welcome to 99Acres platform!",
        "type": "welcome",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Property Alert",
        "subject": "New Property Match Found!",
        "template": "Hi {{name}}, We found a property that matches your criteria.",
        "type": "property_alert",
        "is_active": True
    },
    {
        "id": 3,
        "name": "Appointment Confirmation",
        "subject": "Appointment Confirmed",
        "template": "Your appointment for {{property_title}} is confirmed for {{date}}.",
        "type": "appointment",
        "is_active": True
    }
]

SAMPLE_EMAIL_LOGS = [
    {
        "id": 1,
        "to_email": "user@example.com",
        "subject": "Welcome to 99Acres!",
        "template_id": 1,
        "status": "sent",
        "sent_at": "2025-01-01T10:00:00Z",
        "error_message": None
    },
    {
        "id": 2,
        "to_email": "agent@example.com",
        "subject": "New Property Match Found!",
        "template_id": 2,
        "status": "delivered",
        "sent_at": "2025-01-01T11:00:00Z",
        "error_message": None
    }
]

@router.get("/templates", response_model=dict)
async def get_email_templates():
    """Get all email templates - SQLite integration pending"""
    return {
        "success": True,
        "message": "Email templates retrieved successfully",
        "data": SAMPLE_EMAIL_TEMPLATES,
        "count": len(SAMPLE_EMAIL_TEMPLATES)
    }

@router.get("/templates/{template_id}", response_model=dict)
async def get_email_template(template_id: int):
    """Get single email template - SQLite integration pending"""
    template = next((t for t in SAMPLE_EMAIL_TEMPLATES if t["id"] == template_id), None)
    
    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Email template with ID {template_id} not found"
        )
    
    return {
        "success": True,
        "message": "Email template retrieved successfully",
        "data": template
    }

@router.get("/logs", response_model=dict)
async def get_email_logs(
    limit: int = 10,
    skip: int = 0,
    status: Optional[str] = None
):
    """Get email logs - SQLite integration pending"""
    
    filtered_logs = SAMPLE_EMAIL_LOGS.copy()
    
    if status:
        filtered_logs = [log for log in filtered_logs if log["status"] == status]
    
    total = len(filtered_logs)
    logs = filtered_logs[skip:skip + limit]
    
    return {
        "success": True,
        "message": "Email logs retrieved successfully",
        "data": logs,
        "pagination": {
            "total": total,
            "count": len(logs),
            "skip": skip,
            "limit": limit
        }
    }

@router.post("/send", response_model=dict)
async def send_email(email_data: EmailSendRequest):
    """Send email - SQLite integration pending"""
    return {
        "success": True,
        "message": "Email sent successfully - SQLite integration in progress",
        "data": {
            "email_id": "email_002",
            "template_name": email_data.name,
            "subject": email_data.subject,
            "recipients_count": email_data.recipients,
            "body_preview": email_data.body[:50] + "..." if len(email_data.body) > 50 else email_data.body,
            "status": "queued",
            "queued_at": "2025-10-01T12:50:00Z"
        }
    }

@router.post("/templates", response_model=dict)
async def create_email_template(template_data: EmailTemplateRequest):
    """Create email template - SQLite integration pending"""
    new_template = {
        "id": len(SAMPLE_EMAIL_TEMPLATES) + 1,
        "name": template_data.name,
        "subject": template_data.subject,
        "template": template_data.template,
        "type": template_data.type,
        "is_active": template_data.is_active,
        "created_at": "2025-10-01T12:50:00Z"
    }
    
    return {
        "success": True,
        "message": "Email template created successfully - SQLite integration in progress",
        "data": new_template
    }

@router.put("/templates/{template_id}", response_model=dict)
async def update_email_template(template_id: int):
    """Update email template - SQLite integration pending"""
    return {
        "success": False,
        "message": f"Email template {template_id} update - SQLite integration in progress"
    }

@router.delete("/templates/{template_id}", response_model=dict)
async def delete_email_template(template_id: int):
    """Delete email template - SQLite integration pending"""
    return {
        "success": False,
        "message": f"Email template {template_id} deletion - SQLite integration in progress"
    }

@router.get("/stats", response_model=dict)
async def get_email_stats():
    """Get email statistics - SQLite integration pending"""
    return {
        "success": True,
        "message": "Email statistics retrieved successfully",
        "data": {
            "total_sent": 156,
            "total_delivered": 148,
            "total_bounced": 5,
            "total_failed": 3,
            "delivery_rate": 94.9,
            "bounce_rate": 3.2
        }
    }