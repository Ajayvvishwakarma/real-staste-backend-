from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.database.mongodb import mongodb

router = APIRouter()

# Pydantic models for banners
class BannerCreate(BaseModel):
    title: str
    description: str
    image_url: str
    link_url: Optional[str] = None
    position: str = "home"  # home, listing, property, etc.
    is_active: bool = True

class BannerUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_banners(
    position: Optional[str] = Query(None, description="Filter by banner position"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: Optional[int] = Query(10, description="Number of banners to return")
):
    """Get website banners with optional filters"""
    try:
        query = {}
        if position:
            query["position"] = position
        if is_active is not None:
            query["is_active"] = is_active

        banners = await mongodb.database.banners.find(query).to_list(limit)
        total_count = await mongodb.database.banners.count_documents(query)
        
        return {
            "success": True,
            "message": "Banners retrieved successfully",
            "data": banners,
            "count": len(banners),
            "total_available": total_count
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving banners: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/{banner_id}", response_model=dict)
async def get_banner_by_id(banner_id: int):
    """Get a specific banner by ID"""
    try:
        banner = await mongodb.database.banners.find_one({"_id": banner_id})
        
        if not banner:
            raise HTTPException(status_code=404, detail="Banner not found")
        
        return {
            "success": True,
            "message": "Banner retrieved successfully",
            "data": banner
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving banner: {str(e)}",
            "data": None
        }

@router.get("/position/{position}", response_model=dict)
async def get_banners_by_position(position: str):
    """Get banners by position (home, sidebar, listing, etc.)"""
    try:
        position_banners = await mongodb.database.banners.find({"position": position, "is_active": True}).to_list(100)
        
        return {
            "success": True,
            "message": f"Banners for {position} position retrieved successfully",
            "data": position_banners,
            "count": len(position_banners),
            "position": position
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving banners for {position}: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/active/list", response_model=dict)
async def get_active_banners():
    """Get only active banners"""
    try:
        active_banners = await mongodb.database.banners.find({"is_active": True}).to_list(100)
        
        return {
            "success": True,
            "message": "Active banners retrieved successfully",
            "data": active_banners,
            "count": len(active_banners)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving active banners: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/stats/overview", response_model=dict)
async def get_banner_statistics():
    """Get banner performance statistics"""
    try:
        total_banners = await mongodb.database.banners.count_documents({})
        active_banners = await mongodb.database.banners.count_documents({"is_active": True})
        total_views = sum([b["views"] for b in await mongodb.database.banners.find({}).to_list(1000)])
        total_clicks = sum([b["clicks"] for b in await mongodb.database.banners.find({}).to_list(1000)])
        avg_ctr = round((total_clicks / total_views * 100), 2) if total_views > 0 else 0
        
        # Position breakdown
        positions = {}
        for banner in await mongodb.database.banners.find({}).to_list(1000):
            pos = banner["position"]
            if pos not in positions:
                positions[pos] = {"count": 0, "views": 0, "clicks": 0}
            positions[pos]["count"] += 1
            positions[pos]["views"] += banner["views"]
            positions[pos]["clicks"] += banner["clicks"]
        
        # Top performing banners
        top_banners = sorted(await mongodb.database.banners.find({}).to_list(1000), key=lambda x: x["clicks"], reverse=True)[:3]
        top_performers = [{"id": b["id"], "title": b["title"], "clicks": b["clicks"]} for b in top_banners]
        
        return {
            "success": True,
            "message": "Banner statistics retrieved successfully",
            "data": {
                "overview": {
                    "total_banners": total_banners,
                    "active_banners": active_banners,
                    "inactive_banners": total_banners - active_banners,
                    "total_views": total_views,
                    "total_clicks": total_clicks,
                    "average_ctr": f"{avg_ctr}%"
                },
                "by_position": positions,
                "top_performers": top_performers
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving banner statistics: {str(e)}",
            "data": {}
        }

@router.post("/", response_model=dict)
async def create_banner(banner: BannerCreate):
    """Create a new banner"""
    try:
        banner_data = banner.dict()
        banner_data["created_at"] = datetime.utcnow()
        banner_data["views"] = 0
        banner_data["clicks"] = 0
        result = await mongodb.database.banners.insert_one(banner_data)
        
        return {
            "success": True,
            "message": "Banner created successfully",
            "data": {"id": str(result.inserted_id)}
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating banner: {str(e)}",
            "data": None
        }

@router.put("/{banner_id}", response_model=dict)
async def update_banner(banner_id: int, banner_data: BannerUpdate):
    """Update an existing banner (simulation)"""
    try:
        update_data = {k: v for k, v in banner_data.dict().items() if v is not None}
        result = await mongodb.database.banners.update_one({"_id": banner_id}, {"$set": update_data})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Banner not found or no changes made")
        
        updated_banner = await mongodb.database.banners.find_one({"_id": banner_id})
        
        return {
            "success": True,
            "message": "Banner updated successfully",
            "data": updated_banner
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating banner: {str(e)}",
            "data": None
        }

@router.delete("/{banner_id}", response_model=dict)
async def delete_banner(banner_id: int):
    """Delete a banner (simulation)"""
    try:
        result = await mongodb.database.banners.delete_one({"_id": banner_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Banner not found")
        
        return {
            "success": True,
            "message": f"Banner deleted successfully",
            "data": {"deleted_banner_id": banner_id}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting banner: {str(e)}",
            "data": None
        }