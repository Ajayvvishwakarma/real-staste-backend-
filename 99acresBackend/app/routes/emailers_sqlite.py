from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.database.sqlite_db import get_db
from app.database.sqlite_models import EmailCampaign, EmailTemplate, EmailLog

router = APIRouter()

# Pydantic models
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

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_emailers_info(db: AsyncSession = Depends(get_db)):
    """Get emailers module information and dashboard stats from SQLite"""
    try:
        # Get campaign counts
        total_campaigns_result = await db.execute(select(func.count(EmailCampaign.id)))
        total_campaigns = total_campaigns_result.scalar()
        
        active_campaigns_result = await db.execute(
            select(func.count(EmailCampaign.id)).where(EmailCampaign.status == "active")
        )
        active_campaigns = active_campaigns_result.scalar()
        
        # Get total emails sent
        total_sent_result = await db.execute(select(func.sum(EmailCampaign.total_sent)))
        total_sent = total_sent_result.scalar() or 0
        
        # Get recent campaigns
        recent_campaigns_result = await db.execute(
            select(EmailCampaign).order_by(EmailCampaign.created_at.desc()).limit(3)
        )
        recent_campaigns = recent_campaigns_result.scalars().all()
        
        # Calculate overall open rate
        if total_sent > 0:
            total_opened_result = await db.execute(select(func.sum(EmailCampaign.total_opened)))
            total_opened = total_opened_result.scalar() or 0
            open_rate = round((total_opened / total_sent) * 100, 1) if total_sent > 0 else 0
        else:
            open_rate = 0
        
        # Convert campaigns to dict
        campaigns_data = []
        for campaign in recent_campaigns:
            campaigns_data.append({
                "id": campaign.id,
                "name": campaign.name,
                "subject": campaign.subject,
                "recipients": campaign.recipients,
                "status": campaign.status,
                "sent_date": campaign.created_at.strftime("%Y-%m-%d") if campaign.created_at else None,
                "open_rate": campaign.open_rate,
                "total_sent": campaign.total_sent,
                "total_opened": campaign.total_opened
            })
        
        return {
            "success": True,
            "message": "Email Management API - SQLite Data",
            "dashboard": {
                "total_campaigns": total_campaigns,
                "active_campaigns": active_campaigns,
                "total_emails_sent": total_sent,
                "open_rate": f"{open_rate}%"
            },
            "recent_campaigns": campaigns_data,
            "available_endpoints": {
                "dashboard": "/api/emailers/dashboard",
                "campaigns": "/api/emailers/campaigns",
                "templates": "/api/emailers/templates"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving emailers data: {str(e)}",
            "dashboard": {
                "total_campaigns": 0,
                "active_campaigns": 0,
                "total_emails_sent": 0,
                "open_rate": "0%"
            }
        }

@router.post("", response_model=dict)
@router.post("/", response_model=dict)
async def create_campaign(email_data: EmailSendRequest, db: AsyncSession = Depends(get_db)):
    """Create new email campaign and save to SQLite"""
    try:
        # Create new campaign
        new_campaign = EmailCampaign(
            name=email_data.name,
            subject=email_data.subject,
            body=email_data.body,
            recipients=email_data.recipients,
            status="active",
            total_sent=email_data.recipients,
            total_opened=0,
            open_rate=0.0
        )
        
        db.add(new_campaign)
        await db.commit()
        await db.refresh(new_campaign)
        
        return {
            "success": True,
            "message": "Campaign created and saved to SQLite successfully",
            "data": {
                "campaign_id": new_campaign.id,
                "name": new_campaign.name,
                "subject": new_campaign.subject,
                "recipients": new_campaign.recipients,
                "status": new_campaign.status,
                "created_at": new_campaign.created_at.isoformat() if new_campaign.created_at else None
            }
        }
        
    except Exception as e:
        await db.rollback()
        return {
            "success": False,
            "message": f"Error creating campaign: {str(e)}"
        }

@router.get("/campaigns", response_model=dict)
async def get_campaigns(db: AsyncSession = Depends(get_db)):
    """Get all campaigns from SQLite"""
    try:
        result = await db.execute(select(EmailCampaign).order_by(EmailCampaign.created_at.desc()))
        campaigns = result.scalars().all()
        
        campaigns_data = []
        for campaign in campaigns:
            campaigns_data.append({
                "id": campaign.id,
                "name": campaign.name,
                "subject": campaign.subject,
                "recipients": campaign.recipients,
                "status": campaign.status,
                "sent_date": campaign.created_at.strftime("%Y-%m-%d") if campaign.created_at else None,
                "open_rate": campaign.open_rate,
                "total_sent": campaign.total_sent,
                "total_opened": campaign.total_opened,
                "created_at": campaign.created_at.isoformat() if campaign.created_at else None
            })
        
        return {
            "success": True,
            "message": "Campaigns retrieved from SQLite successfully",
            "data": campaigns_data,
            "count": len(campaigns_data)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving campaigns: {str(e)}",
            "data": []
        }

@router.get("/templates", response_model=dict)
async def get_templates(db: AsyncSession = Depends(get_db)):
    """Get all email templates from SQLite"""
    try:
        result = await db.execute(select(EmailTemplate).where(EmailTemplate.is_active == True))
        templates = result.scalars().all()
        
        templates_data = []
        for template in templates:
            templates_data.append({
                "id": template.id,
                "name": template.name,
                "subject": template.subject,
                "template": template.template,
                "type": template.type,
                "is_active": template.is_active,
                "created_at": template.created_at.isoformat() if template.created_at else None
            })
        
        return {
            "success": True,
            "message": "Templates retrieved from SQLite successfully",
            "data": templates_data,
            "count": len(templates_data)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving templates: {str(e)}",
            "data": []
        }

@router.delete("/campaigns/{campaign_id}", response_model=dict)
async def delete_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    """Delete campaign from SQLite"""
    try:
        result = await db.execute(select(EmailCampaign).where(EmailCampaign.id == campaign_id))
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        await db.delete(campaign)
        await db.commit()
        
        return {
            "success": True,
            "message": f"Campaign '{campaign.name}' deleted from SQLite successfully",
            "data": {"deleted_campaign_id": campaign_id}
        }
        
    except Exception as e:
        await db.rollback()
        return {
            "success": False,
            "message": f"Error deleting campaign: {str(e)}"
        }








        