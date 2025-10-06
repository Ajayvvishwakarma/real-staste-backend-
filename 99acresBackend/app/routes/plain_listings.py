from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

router = APIRouter()

# Simple plain listings data - basic property information
PLAIN_LISTINGS = [
    {
        "id": 1,
        "property_id": "PL001",
        "title": "Luxury 3BHK Apartment",
        "price": 15000000,
        "location": "Sector 62, Noida",
        "type": "apartment",
        "status": "active",
        "views": 245,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-09-15",
        "actions": ["edit", "delete", "view"]
    },
    {
        "id": 2,
        "property_id": "PL002",
        "title": "2BHK Builder Floor",
        "price": 8500000,
        "location": "Lajpat Nagar, Delhi",
        "type": "house",
        "status": "active",
        "views": 189,
        "photos": ["photo1.jpg", "photo2.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-09-18",
        "actions": ["edit", "delete", "view"]
    },
    {
        "id": 3,
        "property_id": "PL003",
        "title": "Commercial Office Space",
        "price": 25000000,
        "location": "Cyber City, Gurgaon",
        "type": "commercial",
        "status": "active",
        "views": 567,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-09-20",
        "actions": ["edit", "delete", "view"]
    },
    {
        "id": 4,
        "property_id": "PL004",
        "title": "Farmhouse for Rent",
        "price": 50000,
        "location": "Manesar, Gurgaon",
        "type": "farmhouse",
        "status": "active",
        "views": 123,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-09-22",
        "actions": ["edit", "delete", "view"]
    },
    {
        "id": 5,
        "property_id": "PL005",
        "title": "Studio Apartment",
        "price": 2500000,
        "location": "Koramangala, Bangalore",
        "type": "apartment",
        "status": "active",
        "views": 89,
        "photos": ["photo1.jpg", "photo2.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-09-25",
        "actions": ["edit", "delete", "view"]
    },
    {
        "id": 6,
        "property_id": "PL006",
        "title": "Duplex Villa",
        "price": 35000000,
        "location": "Golf Course Road, Gurgaon",
        "type": "villa",
        "status": "sold",
        "views": 456,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg"],
        "contact_visible": False,
        "priority_placement": False,
        "created_date": "2025-08-10",
        "actions": ["view"]
    },
    {
        "id": 7,
        "property_id": "PL007",
        "title": "1BHK Flat",
        "price": 4500000,
        "location": "Dwarka, Delhi",
        "type": "apartment",
        "status": "active",
        "views": 234,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-09-28",
        "actions": ["edit", "delete", "view"]
    },
    {
        "id": 8,
        "property_id": "PL008",
        "title": "Retail Shop",
        "price": 12000000,
        "location": "Connaught Place, Delhi",
        "type": "commercial",
        "status": "active",
        "views": 345,
        "photos": ["photo1.jpg", "photo2.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-09-30",
        "actions": ["edit", "delete", "view"]
    },
    {
        "id": 9,
        "property_id": "PL009",
        "title": "3BHK Independent House",
        "price": 18000000,
        "location": "Rajouri Garden, Delhi",
        "type": "house",
        "status": "active",
        "views": 178,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-10-01",
        "actions": ["edit", "delete", "view"]
    },
    {
        "id": 10,
        "property_id": "PL010",
        "title": "Warehouse Space",
        "price": 45000000,
        "location": "Bhiwadi, Rajasthan",
        "type": "commercial",
        "status": "active",
        "views": 67,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg"],
        "contact_visible": True,
        "priority_placement": False,
        "created_date": "2025-10-01",
        "actions": ["edit", "delete", "view"]
    }
]

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_plain_listings(
    limit: Optional[int] = Query(None, description="Number of listings to return"),
    type: Optional[str] = Query(None, description="Filter by property type"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    """Get simple property listings with basic information only"""
    try:
        filtered_listings = PLAIN_LISTINGS.copy()
        
        # Apply filters
        if type:
            filtered_listings = [l for l in filtered_listings if l["type"].lower() == type.lower()]
        
        if status:
            filtered_listings = [l for l in filtered_listings if l["status"].lower() == status.lower()]
        
        # Apply limit
        if limit:
            filtered_listings = filtered_listings[:limit]
        
        return {
            "success": True,
            "message": "Plain listings retrieved successfully",
            "data": filtered_listings,
            "count": len(filtered_listings),
            "total": len(PLAIN_LISTINGS)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving plain listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/basic", response_model=dict)
async def get_basic_listings():
    """Get the most basic listing information - just ID, title, and price"""
    try:
        basic_data = [
            {
                "id": listing["id"],
                "title": listing["title"],
                "price": listing["price"]
            }
            for listing in PLAIN_LISTINGS
        ]
        
        return {
            "success": True,
            "message": "Basic listings retrieved successfully",
            "data": basic_data,
            "count": len(basic_data)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving basic listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/simple", response_model=dict)
async def get_simple_listings():
    """Get simplified listings without filtering options"""
    try:
        return {
            "success": True,
            "message": "Simple listings retrieved successfully",
            "listings": PLAIN_LISTINGS,
            "total_count": len(PLAIN_LISTINGS)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving simple listings: {str(e)}",
            "listings": [],
            "total_count": 0
        }

@router.get("/types", response_model=dict)
async def get_listing_types():
    """Get available property types in plain listings"""
    try:
        types = list(set([listing["type"] for listing in PLAIN_LISTINGS]))
        statuses = list(set([listing["status"] for listing in PLAIN_LISTINGS]))
        
        return {
            "success": True,
            "message": "Listing types retrieved successfully",
            "data": {
                "property_types": types,
                "statuses": statuses,
                "total_listings": len(PLAIN_LISTINGS)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving listing types: {str(e)}",
            "data": {}
        }

@router.get("/summary", response_model=dict)
async def get_listings_summary():
    """Get summary statistics of plain listings"""
    try:
        total_listings = len(PLAIN_LISTINGS)
        active_count = len([l for l in PLAIN_LISTINGS if l["status"] == "active"])
        sold_count = len([l for l in PLAIN_LISTINGS if l["status"] == "sold"])
        
        # Views statistics
        total_views = sum([l["views"] for l in PLAIN_LISTINGS])
        views_this_month = sum([l["views"] for l in PLAIN_LISTINGS if l["created_date"].startswith("2025-10")])
        
        # Price statistics
        prices = [l["price"] for l in PLAIN_LISTINGS if l["status"] == "active"]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        avg_price = sum(prices) // len(prices) if prices else 0
        
        # Type breakdown
        type_counts = {}
        for listing in PLAIN_LISTINGS:
            prop_type = listing["type"]
            type_counts[prop_type] = type_counts.get(prop_type, 0) + 1
        
        return {
            "success": True,
            "message": "Listings summary retrieved successfully",
            "data": {
                "total_listings": total_listings,
                "active_listings": active_count,
                "sold_listings": sold_count,
                "total_views": total_views,
                "views_this_month": views_this_month,
                "price_range": {
                    "min_price": min_price,
                    "max_price": max_price,
                    "average_price": avg_price
                },
                "by_type": type_counts
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving listings summary: {str(e)}",
            "data": {}
        }

@router.get("/dashboard", response_model=dict)
async def get_dashboard_data():
    """Get dashboard data specifically formatted for frontend"""
    try:
        total_listings = len(PLAIN_LISTINGS)
        active_listings = len([l for l in PLAIN_LISTINGS if l["status"] == "active"])
        views_this_month = sum([l["views"] for l in PLAIN_LISTINGS if l["created_date"].startswith("2025-10")])
        
        # Format listings for table display
        formatted_listings = []
        for listing in PLAIN_LISTINGS:
            formatted_listings.append({
                "property_id": listing["property_id"],
                "title": listing["title"],
                "location": listing["location"],
                "price": f"₹{listing['price']:,}",
                "status": listing["status"],
                "views": listing["views"],
                "actions": listing["actions"]
            })
        
        return {
            "success": True,
            "message": "Dashboard data retrieved successfully",
            "dashboard": {
                "total_plain_listings": total_listings,
                "active_listings": active_listings,
                "views_this_month": views_this_month,
                "features": {
                    "basic_property_details": True,
                    "up_to_5_photos": True,
                    "contact_details_visible": True,
                    "priority_placement": False
                }
            },
            "listings": formatted_listings,
            "count": len(formatted_listings)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving dashboard data: {str(e)}",
            "dashboard": {},
            "listings": []
        }

@router.get("/{listing_id}", response_model=dict)
async def get_plain_listing_by_id(listing_id: int):
    """Get a specific plain listing by ID"""
    try:
        listing = next((l for l in PLAIN_LISTINGS if l["id"] == listing_id), None)
        
        if not listing:
            raise HTTPException(status_code=404, detail="Plain listing not found")
        
        return {
            "success": True,
            "message": "Plain listing retrieved successfully",
            "data": listing
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving plain listing: {str(e)}",
            "data": None
        }