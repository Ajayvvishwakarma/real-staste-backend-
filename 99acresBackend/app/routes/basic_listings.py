from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

router = APIRouter()

# Basic listings data - enhanced features compared to plain listings
BASIC_LISTINGS = [
    {
        "id": 1,
        "property_id": "BL001",
        "title": "Premium 3BHK Apartment",
        "description": "Luxurious 3BHK apartment with modern amenities in prime location",
        "price": 15000000,
        "location": "Sector 62, Noida",
        "city": "Noida",
        "state": "Uttar Pradesh",
        "type": "apartment",
        "status": "active",
        "views": 1250,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg"],
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1200,
        "contact_visible": True,
        "priority_placement": True,
        "verified": True,
        "featured": True,
        "created_date": "2025-09-15",
        "listing_type": "basic",
        "agent_name": "Rajesh Kumar",
        "agent_phone": "9876543210",
        "amenities": ["Parking", "Gym", "Swimming Pool", "Security"],
        "actions": ["edit", "delete", "view", "promote", "feature"]
    },
    {
        "id": 2,
        "property_id": "BL002",
        "title": "Modern 2BHK Builder Floor",
        "description": "Well-designed 2BHK builder floor with excellent ventilation",
        "price": 8500000,
        "location": "Lajpat Nagar, Delhi",
        "city": "Delhi",
        "state": "Delhi",
        "type": "house",
        "status": "active",
        "views": 892,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg"],
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 900,
        "contact_visible": True,
        "priority_placement": True,
        "verified": True,
        "featured": False,
        "created_date": "2025-09-18",
        "listing_type": "basic",
        "agent_name": "Priya Sharma",
        "agent_phone": "9876543211",
        "amenities": ["Parking", "Garden", "Security"],
        "actions": ["edit", "delete", "view", "promote", "feature"]
    },
    {
        "id": 3,
        "property_id": "BL003",
        "title": "Commercial Office Space",
        "description": "Prime commercial office space in business district",
        "price": 25000000,
        "location": "Cyber City, Gurgaon",
        "city": "Gurgaon",
        "state": "Haryana",
        "type": "commercial",
        "status": "active",
        "views": 1567,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg"],
        "bedrooms": 0,
        "bathrooms": 4,
        "area": 2000,
        "contact_visible": True,
        "priority_placement": True,
        "verified": True,
        "featured": True,
        "created_date": "2025-09-20",
        "listing_type": "basic",
        "agent_name": "Amit Singh",
        "agent_phone": "9876543212",
        "amenities": ["Parking", "AC", "Power Backup", "Elevator"],
        "actions": ["edit", "delete", "view", "promote", "feature"]
    },
    {
        "id": 4,
        "property_id": "BL004",
        "title": "Luxury Farmhouse",
        "description": "Spacious farmhouse with beautiful garden and modern amenities",
        "price": 8500000,
        "location": "Manesar, Gurgaon",
        "city": "Gurgaon",
        "state": "Haryana",
        "type": "farmhouse",
        "status": "active",
        "views": 723,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg"],
        "bedrooms": 4,
        "bathrooms": 3,
        "area": 5000,
        "contact_visible": True,
        "priority_placement": True,
        "verified": True,
        "featured": False,
        "created_date": "2025-09-22",
        "listing_type": "basic",
        "agent_name": "Sunita Gupta",
        "agent_phone": "9876543213",
        "amenities": ["Garden", "Swimming Pool", "Parking", "Security"],
        "actions": ["edit", "delete", "view", "promote", "feature"]
    },
    {
        "id": 5,
        "property_id": "BL005",
        "title": "Compact Studio Apartment",
        "description": "Modern studio apartment perfect for young professionals",
        "price": 2500000,
        "location": "Koramangala, Bangalore",
        "city": "Bangalore",
        "state": "Karnataka",
        "type": "apartment",
        "status": "active",
        "views": 456,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg"],
        "bedrooms": 1,
        "bathrooms": 1,
        "area": 400,
        "contact_visible": True,
        "priority_placement": True,
        "verified": True,
        "featured": False,
        "created_date": "2025-09-25",
        "listing_type": "basic",
        "agent_name": "Ravi Patel",
        "agent_phone": "9876543214",
        "amenities": ["AC", "Parking", "Security"],
        "actions": ["edit", "delete", "view", "promote", "feature"]
    },
    {
        "id": 6,
        "property_id": "BL006",
        "title": "Duplex Villa",
        "description": "Elegant duplex villa with premium finishes",
        "price": 35000000,
        "location": "Golf Course Road, Gurgaon",
        "city": "Gurgaon",
        "state": "Haryana",
        "type": "villa",
        "status": "sold",
        "views": 2145,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg"],
        "bedrooms": 4,
        "bathrooms": 4,
        "area": 3500,
        "contact_visible": False,
        "priority_placement": False,
        "verified": True,
        "featured": False,
        "created_date": "2025-08-10",
        "listing_type": "basic",
        "agent_name": "Neha Agarwal",
        "agent_phone": "9876543215",
        "amenities": ["Garden", "Swimming Pool", "Gym", "Parking"],
        "actions": ["view"]
    },
    {
        "id": 7,
        "property_id": "BL007",
        "title": "1BHK Affordable Flat",
        "description": "Affordable 1BHK flat in well-connected area",
        "price": 4500000,
        "location": "Dwarka, Delhi",
        "city": "Delhi",
        "state": "Delhi",
        "type": "apartment",
        "status": "active",
        "views": 678,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg"],
        "bedrooms": 1,
        "bathrooms": 1,
        "area": 600,
        "contact_visible": True,
        "priority_placement": True,
        "verified": True,
        "featured": False,
        "created_date": "2025-09-28",
        "listing_type": "basic",
        "agent_name": "Deepak Mehta",
        "agent_phone": "9876543216",
        "amenities": ["Parking", "Security", "Lift"],
        "actions": ["edit", "delete", "view", "promote", "feature"]
    },
    {
        "id": 8,
        "property_id": "BL008",
        "title": "Prime Retail Shop",
        "description": "High-footfall retail space in premium location",
        "price": 12000000,
        "location": "Connaught Place, Delhi",
        "city": "Delhi",
        "state": "Delhi",
        "type": "commercial",
        "status": "active",
        "views": 1234,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg"],
        "bedrooms": 0,
        "bathrooms": 1,
        "area": 800,
        "contact_visible": True,
        "priority_placement": True,
        "verified": True,
        "featured": True,
        "created_date": "2025-09-30",
        "listing_type": "basic",
        "agent_name": "Kiran Joshi",
        "agent_phone": "9876543217",
        "amenities": ["AC", "Parking", "CCTV"],
        "actions": ["edit", "delete", "view", "promote", "feature"]
    }
]

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_basic_listings(
    city: Optional[str] = Query(None, description="Filter by city"),
    type: Optional[str] = Query(None, description="Filter by property type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    featured: Optional[bool] = Query(None, description="Filter by featured status"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    limit: Optional[int] = Query(10, description="Number of listings to return")
):
    """Get basic listings with enhanced features and filtering"""
    try:
        filtered_listings = BASIC_LISTINGS.copy()
        
        # Apply filters
        if city:
            filtered_listings = [l for l in filtered_listings if l["city"].lower() == city.lower()]
        
        if type:
            filtered_listings = [l for l in filtered_listings if l["type"].lower() == type.lower()]
        
        if status:
            filtered_listings = [l for l in filtered_listings if l["status"].lower() == status.lower()]
            
        if featured is not None:
            filtered_listings = [l for l in filtered_listings if l["featured"] == featured]
        
        if min_price is not None:
            filtered_listings = [l for l in filtered_listings if l["price"] >= min_price]
            
        if max_price is not None:
            filtered_listings = [l for l in filtered_listings if l["price"] <= max_price]
        
        # Apply limit
        if limit:
            filtered_listings = filtered_listings[:limit]
        
        # Calculate statistics
        total_views = sum([l["views"] for l in BASIC_LISTINGS])
        featured_count = len([l for l in BASIC_LISTINGS if l["featured"]])
        verified_count = len([l for l in BASIC_LISTINGS if l["verified"]])
        
        return {
            "success": True,
            "message": "Basic listings retrieved successfully",
            "data": filtered_listings,
            "count": len(filtered_listings),
            "total_available": len(BASIC_LISTINGS),
            "statistics": {
                "total_views": total_views,
                "featured_listings": featured_count,
                "verified_listings": verified_count
            },
            "filters_applied": {
                "city": city,
                "type": type,
                "status": status,
                "featured": featured,
                "min_price": min_price,
                "max_price": max_price,
                "limit": limit
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving basic listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/dashboard", response_model=dict)
async def get_basic_dashboard():
    """Get basic listings dashboard data"""
    try:
        total_listings = len(BASIC_LISTINGS)
        active_listings = len([l for l in BASIC_LISTINGS if l["status"] == "active"])
        featured_listings = len([l for l in BASIC_LISTINGS if l["featured"]])
        views_this_month = sum([l["views"] for l in BASIC_LISTINGS if l["created_date"].startswith("2025-10")])
        total_views = sum([l["views"] for l in BASIC_LISTINGS])
        
        # Format listings for dashboard
        formatted_listings = []
        for listing in BASIC_LISTINGS:
            formatted_listings.append({
                "property_id": listing["property_id"],
                "title": listing["title"],
                "location": f"{listing['location']}, {listing['city']}",
                "price": f"₹{listing['price']:,}",
                "status": listing["status"],
                "views": listing["views"],
                "featured": listing["featured"],
                "verified": listing["verified"],
                "actions": listing["actions"]
            })
        
        return {
            "success": True,
            "message": "Basic listings dashboard data retrieved successfully",
            "dashboard": {
                "total_basic_listings": total_listings,
                "active_listings": active_listings,
                "featured_listings": featured_listings,
                "views_this_month": views_this_month,
                "total_views": total_views,
                "features": {
                    "enhanced_photos": "Up to 10 photos",
                    "priority_placement": True,
                    "contact_details_visible": True,
                    "property_verification": True,
                    "agent_details": True,
                    "amenities_listing": True
                }
            },
            "listings": formatted_listings,
            "count": len(formatted_listings)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving basic dashboard data: {str(e)}",
            "dashboard": {},
            "listings": []
        }

@router.get("/featured", response_model=dict)
async def get_featured_basic_listings():
    """Get featured basic listings only"""
    try:
        featured_listings = [l for l in BASIC_LISTINGS if l["featured"] and l["status"] == "active"]
        
        return {
            "success": True,
            "message": "Featured basic listings retrieved successfully",
            "data": featured_listings,
            "count": len(featured_listings)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving featured basic listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/verified", response_model=dict)
async def get_verified_basic_listings():
    """Get verified basic listings only"""
    try:
        verified_listings = [l for l in BASIC_LISTINGS if l["verified"] and l["status"] == "active"]
        
        return {
            "success": True,
            "message": "Verified basic listings retrieved successfully",
            "data": verified_listings,
            "count": len(verified_listings)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving verified basic listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/stats", response_model=dict)
async def get_basic_listings_stats():
    """Get comprehensive statistics for basic listings"""
    try:
        total_listings = len(BASIC_LISTINGS)
        active_listings = len([l for l in BASIC_LISTINGS if l["status"] == "active"])
        sold_listings = len([l for l in BASIC_LISTINGS if l["status"] == "sold"])
        featured_listings = len([l for l in BASIC_LISTINGS if l["featured"]])
        verified_listings = len([l for l in BASIC_LISTINGS if l["verified"]])
        
        # Price statistics for active listings
        active_prices = [l["price"] for l in BASIC_LISTINGS if l["status"] == "active"]
        min_price = min(active_prices) if active_prices else 0
        max_price = max(active_prices) if active_prices else 0
        avg_price = sum(active_prices) // len(active_prices) if active_prices else 0
        
        # Views statistics
        total_views = sum([l["views"] for l in BASIC_LISTINGS])
        avg_views = total_views // len(BASIC_LISTINGS) if BASIC_LISTINGS else 0
        
        # Type breakdown
        type_stats = {}
        for listing in BASIC_LISTINGS:
            prop_type = listing["type"]
            if prop_type not in type_stats:
                type_stats[prop_type] = {"count": 0, "views": 0}
            type_stats[prop_type]["count"] += 1
            type_stats[prop_type]["views"] += listing["views"]
        
        # City breakdown
        city_stats = {}
        for listing in BASIC_LISTINGS:
            city = listing["city"]
            city_stats[city] = city_stats.get(city, 0) + 1
        
        return {
            "success": True,
            "message": "Basic listings statistics retrieved successfully",
            "data": {
                "overview": {
                    "total_listings": total_listings,
                    "active_listings": active_listings,
                    "sold_listings": sold_listings,
                    "featured_listings": featured_listings,
                    "verified_listings": verified_listings
                },
                "pricing": {
                    "min_price": min_price,
                    "max_price": max_price,
                    "average_price": avg_price
                },
                "engagement": {
                    "total_views": total_views,
                    "average_views_per_listing": avg_views
                },
                "by_type": type_stats,
                "by_city": city_stats
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving basic listings statistics: {str(e)}",
            "data": {}
        }

@router.get("/{listing_id}", response_model=dict)
async def get_basic_listing_by_id(listing_id: int):
    """Get a specific basic listing by ID"""
    try:
        listing = next((l for l in BASIC_LISTINGS if l["id"] == listing_id), None)
        
        if not listing:
            raise HTTPException(status_code=404, detail="Basic listing not found")
        
        return {
            "success": True,
            "message": "Basic listing retrieved successfully",
            "data": listing
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving basic listing: {str(e)}",
            "data": None
        }