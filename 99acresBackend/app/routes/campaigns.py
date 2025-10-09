# Campaign routes with MongoDB integration
from fastapi import APIRouter, HTTPException, status, Depends, Query, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List
from app.database.repositories.mongo_campaign_repository import MongoCampaignRepository
from app.database.repositories.mongo_user_repository import MongoUserRepository
from app.database.schemas.campaign import Campaign, CampaignCreate, CampaignUpdate, CampaignStats
from app.database.mongo_models import User

security = HTTPBearer(auto_error=False)
router = APIRouter()

async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> Optional[User]:
    """Get current user from token (optional - returns None if no token)"""
    if not credentials:
        return None
    try:
        token = credentials.credentials
        user = await MongoUserRepository.get_user_from_token(token)
        return user
    except Exception as e:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from token (required)"""
    try:
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = credentials.credentials
        user = await MongoUserRepository.get_user_from_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/", response_model=List[Campaign])
async def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status: Optional[str] = Query(None, description="Filter by status: active, paused, completed, archived"),
    campaign_type: Optional[str] = Query(None, description="Filter by type: marketing, email, sms, social_media"),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get all campaigns with optional filtering (authentication optional for viewing)"""
    try:
        # If authenticated: Admins see all campaigns, others see only their own
        # If not authenticated: See all campaigns
        user_id = None
        if current_user:
            user_id = None if current_user.role == "admin" else str(current_user.id)
        
        campaigns = await MongoCampaignRepository.get_campaigns(
            skip=skip,
            limit=limit,
            status=status,
            campaign_type=campaign_type,
            user_id=user_id
        )
        return campaigns
    except Exception as e:
        print(f"Error fetching campaigns: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching campaigns: {str(e)}")

@router.get("/stats", response_model=CampaignStats)
async def get_campaign_statistics(
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get campaign statistics (authentication optional for viewing)"""
    try:
        # If authenticated: Admins see all stats, others see only their own
        # If not authenticated: See all stats
        user_id = None
        if current_user:
            user_id = None if current_user.role == "admin" else str(current_user.id)
        
        stats = await MongoCampaignRepository.get_campaign_stats(user_id=user_id)
        return stats
    except Exception as e:
        print(f"Error fetching campaign stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(
    campaign_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get campaign by ID (authentication optional for viewing)"""
    try:
        campaign = await MongoCampaignRepository.get_campaign_by_id(campaign_id)
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # If authenticated, check ownership unless admin
        if current_user:
            if current_user.role != "admin" and campaign.owner_id != str(current_user.id):
                raise HTTPException(status_code=403, detail="Not authorized to access this campaign")
        
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching campaign: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching campaign: {str(e)}")

@router.post("/", response_model=Campaign, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new campaign"""
    try:
        campaign = await MongoCampaignRepository.create_campaign(
            campaign_data=campaign_data,
            user_id=str(current_user.id)
        )
        return campaign
    except Exception as e:
        print(f"Error creating campaign: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating campaign: {str(e)}")

@router.put("/{campaign_id}", response_model=Campaign)
async def update_campaign(
    campaign_id: str,
    update_data: CampaignUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update campaign"""
    try:
        # Check if campaign exists and user has permission
        existing_campaign = await MongoCampaignRepository.get_campaign_by_id(campaign_id)
        
        if not existing_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Check ownership unless admin
        if current_user.role != "admin" and existing_campaign.owner_id != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized to update this campaign")
        
        updated_campaign = await MongoCampaignRepository.update_campaign(campaign_id, update_data)
        
        if not updated_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found or no changes made")
        
        return updated_campaign
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating campaign: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating campaign: {str(e)}")

@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete campaign"""
    try:
        # Check if campaign exists and user has permission
        existing_campaign = await MongoCampaignRepository.get_campaign_by_id(campaign_id)
        
        if not existing_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Check ownership unless admin
        if current_user.role != "admin" and existing_campaign.owner_id != str(current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized to delete this campaign")
        
        success = await MongoCampaignRepository.delete_campaign(campaign_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting campaign: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting campaign: {str(e)}")

@router.get("/count/total")
async def count_campaigns(
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_user)
):
    """Count campaigns with optional filtering"""
    try:
        # Admins can count all campaigns, others count only their own
        user_id = None if current_user.role == "admin" else str(current_user.id)
        
        count = await MongoCampaignRepository.count_campaigns(status=status, user_id=user_id)
        return {"count": count}
    except Exception as e:
        print(f"Error counting campaigns: {e}")
        raise HTTPException(status_code=500, detail=f"Error counting campaigns: {str(e)}")
