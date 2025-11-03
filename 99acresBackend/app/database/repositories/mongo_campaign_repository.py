# Campaign repository for MongoDB operations
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from app.database.schemas.campaign import Campaign, CampaignCreate, CampaignUpdate, CampaignStats
from app.database.mongodb import get_database

class MongoCampaignRepository:
    """Repository for campaign CRUD operations with MongoDB"""
    
    @staticmethod
    def _normalize_campaign(campaign_doc: dict) -> dict:
        """Normalize campaign data for frontend compatibility"""
        # Add createdAt if not present (use created_at)
        if 'created_at' in campaign_doc and 'createdAt' not in campaign_doc:
            campaign_doc['createdAt'] = campaign_doc['created_at']
        
        # Add updatedAt if not present (use updated_at)
        if 'updated_at' in campaign_doc and 'updatedAt' not in campaign_doc:
            campaign_doc['updatedAt'] = campaign_doc['updated_at']
        
        # Calculate open rate if not present
        if 'openRate' not in campaign_doc or campaign_doc.get('openRate') is None:
            emails_sent = campaign_doc.get('emailsSent', 0) or campaign_doc.get('recipients', 0)
            emails_opened = campaign_doc.get('emailsOpened', 0)
            campaign_doc['openRate'] = (emails_opened / emails_sent * 100) if emails_sent > 0 else 0.0
        
        # Calculate click rate if not present
        if 'clickRate' not in campaign_doc or campaign_doc.get('clickRate') is None:
            emails_sent = campaign_doc.get('emailsSent', 0) or campaign_doc.get('recipients', 0)
            emails_clicked = campaign_doc.get('emailsClicked', 0)
            campaign_doc['clickRate'] = (emails_clicked / emails_sent * 100) if emails_sent > 0 else 0.0
        
        # Ensure email metrics exist
        campaign_doc.setdefault('emailsSent', 0)
        campaign_doc.setdefault('emailsOpened', 0)
        campaign_doc.setdefault('emailsClicked', 0)
        
        return campaign_doc
    
    @staticmethod
    async def create_campaign(campaign_data: CampaignCreate, user_id: str) -> Campaign:
        """Create a new campaign"""
        db = get_database()
        
        campaign_dict = campaign_data.model_dump(exclude_unset=True)
        
        # Use campaignName as name if name is not provided
        if not campaign_dict.get('name') and campaign_dict.get('campaignName'):
            campaign_dict['name'] = campaign_dict['campaignName']
        elif campaign_dict.get('name') and not campaign_dict.get('campaignName'):
            campaign_dict['campaignName'] = campaign_dict['name']
        
        # Set recipients count from recipientList if not provided
        if 'recipientList' in campaign_dict and not campaign_dict.get('recipients'):
            campaign_dict['recipients'] = len(campaign_dict['recipientList'])
        
        # Remove createdAt from frontend if present (use server time)
        campaign_dict.pop('createdAt', None)
        
        # Set timestamps
        now = datetime.utcnow()
        campaign_dict['created_at'] = now
        campaign_dict['createdAt'] = now  # For frontend compatibility
        campaign_dict['created_by'] = user_id
        campaign_dict['owner_id'] = user_id
        
        # Initialize metrics
        campaign_dict['impressions'] = campaign_dict.get('impressions', 0)
        campaign_dict['clicks'] = campaign_dict.get('clicks', 0)
        campaign_dict['conversions'] = campaign_dict.get('conversions', 0)
        campaign_dict['leads_generated'] = campaign_dict.get('leads_generated', 0)
        campaign_dict['spent'] = campaign_dict.get('spent', 0.0)
        
        # Initialize email metrics
        campaign_dict['emailsSent'] = campaign_dict.get('emailsSent', 0)
        campaign_dict['emailsOpened'] = campaign_dict.get('emailsOpened', 0)
        campaign_dict['emailsClicked'] = campaign_dict.get('emailsClicked', 0)
        campaign_dict['openRate'] = 0.0
        campaign_dict['clickRate'] = 0.0
        
        result = await db.campaigns.insert_one(campaign_dict)
        created_campaign = await db.campaigns.find_one({"_id": result.inserted_id})
        return Campaign(**created_campaign)
    
    @staticmethod
    async def get_campaign_by_id(campaign_id: str) -> Optional[Campaign]:
        """Get campaign by ID"""
        db = get_database()
        try:
            campaign_doc = await db.campaigns.find_one({"_id": ObjectId(campaign_id)})
            if campaign_doc:
                campaign_doc = MongoCampaignRepository._normalize_campaign(campaign_doc)
                return Campaign(**campaign_doc)
            return None
        except Exception as e:
            print(f"Error getting campaign by ID: {e}")
            return None
    
    @staticmethod
    async def get_campaigns(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        campaign_type: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> List[Campaign]:
        """Get campaigns with optional filtering"""
        db = get_database()
        try:
            query = {}
            
            if status:
                query['status'] = status
            if campaign_type:
                query['campaign_type'] = campaign_type
            if user_id:
                query['owner_id'] = user_id
            
            cursor = db.campaigns.find(query).skip(skip).limit(limit).sort("created_at", -1)
            campaigns = await cursor.to_list(length=limit)
            
            # Normalize all campaigns
            normalized_campaigns = [
                Campaign(**MongoCampaignRepository._normalize_campaign(campaign)) 
                for campaign in campaigns
            ]
            return normalized_campaigns
        except Exception as e:
            print(f"Error getting campaigns: {e}")
            return []
    
    @staticmethod
    async def update_campaign(campaign_id: str, update_data: CampaignUpdate) -> Optional[Campaign]:
        """Update campaign"""
        db = get_database()
        try:
            update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
            if not update_dict:
                return await MongoCampaignRepository.get_campaign_by_id(campaign_id)
            
            update_dict['updated_at'] = datetime.utcnow()
            
            result = await db.campaigns.update_one(
                {"_id": ObjectId(campaign_id)},
                {"$set": update_dict}
            )
            
            if result.modified_count > 0:
                return await MongoCampaignRepository.get_campaign_by_id(campaign_id)
            return None
        except Exception as e:
            print(f"Error updating campaign: {e}")
            return None
    
    @staticmethod
    async def delete_campaign(campaign_id: str) -> bool:
        """Delete campaign"""
        db = get_database()
        try:
            result = await db.campaigns.delete_one({"_id": ObjectId(campaign_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting campaign: {e}")
            return False
    
    @staticmethod
    async def get_campaign_stats(user_id: Optional[str] = None) -> CampaignStats:
        """Get campaign statistics"""
        db = get_database()
        try:
            query = {}
            if user_id:
                query['owner_id'] = user_id
            
            # Aggregate statistics
            pipeline = [
                {"$match": query},
                {
                    "$group": {
                        "_id": None,
                        "total_campaigns": {"$sum": 1},
                        "active_campaigns": {
                            "$sum": {"$cond": [{"$eq": ["$status", "active"]}, 1, 0]}
                        },
                        "paused_campaigns": {
                            "$sum": {"$cond": [{"$eq": ["$status", "paused"]}, 1, 0]}
                        },
                        "completed_campaigns": {
                            "$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}
                        },
                        "total_budget": {"$sum": "$budget"},
                        "total_spent": {"$sum": "$spent"},
                        "total_impressions": {"$sum": "$impressions"},
                        "total_clicks": {"$sum": "$clicks"},
                        "total_conversions": {"$sum": "$conversions"},
                        "total_leads": {"$sum": "$leads_generated"}
                    }
                }
            ]
            
            result = await db.campaigns.aggregate(pipeline).to_list(length=1)
            
            if result:
                stats_data = result[0]
                # Calculate rates
                total_impressions = stats_data.get('total_impressions', 0)
                total_clicks = stats_data.get('total_clicks', 0)
                
                avg_click_rate = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
                avg_conversion_rate = (stats_data.get('total_conversions', 0) / total_clicks * 100) if total_clicks > 0 else 0
                
                return CampaignStats(
                    total_campaigns=stats_data.get('total_campaigns', 0),
                    active_campaigns=stats_data.get('active_campaigns', 0),
                    paused_campaigns=stats_data.get('paused_campaigns', 0),
                    completed_campaigns=stats_data.get('completed_campaigns', 0),
                    total_budget=stats_data.get('total_budget', 0.0),
                    total_spent=stats_data.get('total_spent', 0.0),
                    total_impressions=stats_data.get('total_impressions', 0),
                    total_clicks=stats_data.get('total_clicks', 0),
                    total_conversions=stats_data.get('total_conversions', 0),
                    total_leads=stats_data.get('total_leads', 0),
                    avg_click_rate=round(avg_click_rate, 2),
                    avg_conversion_rate=round(avg_conversion_rate, 2)
                )
            
            return CampaignStats()
        except Exception as e:
            print(f"Error getting campaign stats: {e}")
            return CampaignStats()
    
    @staticmethod
    async def count_campaigns(status: Optional[str] = None, user_id: Optional[str] = None) -> int:
        """Count campaigns with optional filtering"""
        db = get_database()
        try:
            query = {}
            if status:
                query['status'] = status
            if user_id:
                query['owner_id'] = user_id
            
            return await db.campaigns.count_documents(query)
        except Exception as e:
            print(f"Error counting campaigns: {e}")
            return 0
