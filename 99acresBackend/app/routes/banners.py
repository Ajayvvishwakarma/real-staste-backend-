from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

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

# Sample banner data
SAMPLE_BANNERS = [
    {
        "id": 1,
        "title": "Luxury Apartments Sale",
        "description": "Get up to 20% off on luxury apartments in prime locations",
        "image_url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800",
        "link_url": "/properties?type=apartment",
        "position": "home",
        "is_active": True,
        "created_at": "2025-09-15T10:00:00",
        "views": 1250,
        "clicks": 89
    },
    {
        "id": 2,
        "title": "Commercial Spaces Available",
        "description": "Prime commercial spaces in business districts - Book now!",
        "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800",
        "link_url": "/properties?type=commercial",
        "position": "home",
        "is_active": True,
        "created_at": "2025-09-20T14:30:00",
        "views": 890,
        "clicks": 67
    },
    {
        "id": 3,
        "title": "Property Investment Guide",
        "description": "Download our comprehensive property investment guide",
        "image_url": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800",
        "link_url": "/resources/investment-guide",
        "position": "sidebar",
        "is_active": True,
        "created_at": "2025-09-25T09:15:00",
        "views": 456,
        "clicks": 23
    },
    {
        "id": 4,
        "title": "Weekend Property Fair",
        "description": "Join us this weekend for exclusive property deals",
        "image_url": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800",
        "link_url": "/events/property-fair",
        "position": "home",
        "is_active": False,
        "created_at": "2025-08-10T16:45:00",
        "views": 2340,
        "clicks": 156
    },
    {
        "id": 5,
        "title": "New Launch: Green Valley",
        "description": "Eco-friendly apartments with modern amenities",
        "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
        "link_url": "/properties/green-valley-apartments",
        "position": "listing",
        "is_active": True,
        "created_at": "2025-10-01T08:00:00",
        "views": 123,
        "clicks": 12
    }
]

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_banners(
    position: Optional[str] = Query(None, description="Filter by banner position"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: Optional[int] = Query(10, description="Number of banners to return")
):
    """Get website banners with optional filters"""
    try:
        filtered_banners = SAMPLE_BANNERS.copy()
        
        # Apply filters
        if position:
            filtered_banners = [b for b in filtered_banners if b["position"].lower() == position.lower()]
        
        if is_active is not None:
            filtered_banners = [b for b in filtered_banners if b["is_active"] == is_active]
        
        # Apply limit
        if limit:
            filtered_banners = filtered_banners[:limit]
        
        # Calculate statistics
        total_views = sum([b["views"] for b in SAMPLE_BANNERS])
        total_clicks = sum([b["clicks"] for b in SAMPLE_BANNERS])
        avg_ctr = round((total_clicks / total_views * 100), 2) if total_views > 0 else 0
        
        return {
            "success": True,
            "message": "Banners retrieved successfully",
            "data": filtered_banners,
            "count": len(filtered_banners),
            "total_available": len(SAMPLE_BANNERS),
            "statistics": {
                "total_views": total_views,
                "total_clicks": total_clicks,
                "average_ctr": f"{avg_ctr}%"
            },
            "filters_applied": {
                "position": position,
                "is_active": is_active,
                "limit": limit
            }
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
        banner = next((b for b in SAMPLE_BANNERS if b["id"] == banner_id), None)
        
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
        position_banners = [b for b in SAMPLE_BANNERS if b["position"].lower() == position.lower() and b["is_active"]]
        
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
        active_banners = [b for b in SAMPLE_BANNERS if b["is_active"]]
        
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
        total_banners = len(SAMPLE_BANNERS)
        active_banners = len([b for b in SAMPLE_BANNERS if b["is_active"]])
        total_views = sum([b["views"] for b in SAMPLE_BANNERS])
        total_clicks = sum([b["clicks"] for b in SAMPLE_BANNERS])
        avg_ctr = round((total_clicks / total_views * 100), 2) if total_views > 0 else 0
        
        # Position breakdown
        positions = {}
        for banner in SAMPLE_BANNERS:
            pos = banner["position"]
            if pos not in positions:
                positions[pos] = {"count": 0, "views": 0, "clicks": 0}
            positions[pos]["count"] += 1
            positions[pos]["views"] += banner["views"]
            positions[pos]["clicks"] += banner["clicks"]
        
        # Top performing banners
        top_banners = sorted(SAMPLE_BANNERS, key=lambda x: x["clicks"], reverse=True)[:3]
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
async def create_banner(banner_data: BannerCreate):
    """Create a new banner (simulation - would save to database)"""
    try:
        new_id = max([b["id"] for b in SAMPLE_BANNERS]) + 1
        new_banner = {
            "id": new_id,
            "title": banner_data.title,
            "description": banner_data.description,
            "image_url": banner_data.image_url,
            "link_url": banner_data.link_url,
            "position": banner_data.position,
            "is_active": banner_data.is_active,
            "created_at": datetime.now().isoformat(),
            "views": 0,
            "clicks": 0
        }
        
        # In real app, this would be saved to database
        SAMPLE_BANNERS.append(new_banner)
        
        return {
            "success": True,
            "message": "Banner created successfully",
            "data": new_banner
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
        banner_index = next((i for i, b in enumerate(SAMPLE_BANNERS) if b["id"] == banner_id), None)
        
        if banner_index is None:
            raise HTTPException(status_code=404, detail="Banner not found")
        
        # Update fields if provided
        if banner_data.title is not None:
            SAMPLE_BANNERS[banner_index]["title"] = banner_data.title
        if banner_data.description is not None:
            SAMPLE_BANNERS[banner_index]["description"] = banner_data.description
        if banner_data.image_url is not None:
            SAMPLE_BANNERS[banner_index]["image_url"] = banner_data.image_url
        if banner_data.link_url is not None:
            SAMPLE_BANNERS[banner_index]["link_url"] = banner_data.link_url
        if banner_data.position is not None:
            SAMPLE_BANNERS[banner_index]["position"] = banner_data.position
        if banner_data.is_active is not None:
            SAMPLE_BANNERS[banner_index]["is_active"] = banner_data.is_active
        
        return {
            "success": True,
            "message": "Banner updated successfully",
            "data": SAMPLE_BANNERS[banner_index]
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
        banner_index = next((i for i, b in enumerate(SAMPLE_BANNERS) if b["id"] == banner_id), None)
        
        if banner_index is None:
            raise HTTPException(status_code=404, detail="Banner not found")
        
        deleted_banner = SAMPLE_BANNERS.pop(banner_index)
        
        return {
            "success": True,
            "message": f"Banner '{deleted_banner['title']}' deleted successfully",
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