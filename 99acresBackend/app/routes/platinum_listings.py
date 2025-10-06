from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime

router = APIRouter()

# Platinum listings data - premium features with maximum visibility
PLATINUM_LISTINGS = [
    {
        "id": 1,
        "property_id": "PT001",
        "title": "Exclusive 4BHK Penthouse",
        "description": "Ultra-luxurious 4BHK penthouse with panoramic city views, private terrace, and world-class amenities in the heart of the city",
        "price": 45000000,
        "location": "Golf Course Road, Gurgaon",
        "city": "Gurgaon",
        "state": "Haryana",
        "type": "apartment",
        "status": "active",
        "views": 3250,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg", "photo10.jpg"],
        "video_tour": "virtual_tour_001.mp4",
        "floor_plan": "floor_plan_001.pdf",
        "bedrooms": 4,
        "bathrooms": 4,
        "area": 3500,
        "furnishing": "Fully Furnished",
        "parking": "3 Covered",
        "balconies": 3,
        "contact_visible": True,
        "priority_placement": True,
        "top_search_results": True,
        "verified": True,
        "featured": True,
        "premium_badge": True,
        "social_media_promotion": True,
        "created_date": "2025-09-10",
        "listing_type": "platinum",
        "agent_name": "Vikram Malhotra",
        "agent_phone": "9876543220",
        "agent_email": "vikram@premiumproperties.com",
        "agency": "Premium Properties Ltd",
        "amenities": ["Private Pool", "Gym", "Spa", "Concierge", "Valet Parking", "Security", "Garden", "Club House"],
        "nearby": ["Metro Station - 500m", "Shopping Mall - 1km", "Hospital - 2km", "School - 800m"],
        "price_per_sqft": 12857,
        "emi_calculator": True,
        "virtual_tour_360": True,
        "drone_photography": True,
        "actions": ["edit", "delete", "view", "promote", "feature", "social_share", "analytics"]
    },
    {
        "id": 2,
        "property_id": "PT002",
        "title": "Luxury Commercial Tower",
        "description": "Grade A commercial tower with state-of-the-art facilities, perfect for corporate headquarters and premium office spaces",
        "price": 125000000,
        "location": "Connaught Place, Delhi",
        "city": "Delhi",
        "state": "Delhi",
        "type": "commercial",
        "status": "active",
        "views": 5670,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg", "photo10.jpg"],
        "video_tour": "virtual_tour_002.mp4",
        "floor_plan": "floor_plan_002.pdf",
        "bedrooms": 0,
        "bathrooms": 20,
        "area": 15000,
        "furnishing": "Semi Furnished",
        "parking": "50 Covered",
        "balconies": 0,
        "contact_visible": True,
        "priority_placement": True,
        "top_search_results": True,
        "verified": True,
        "featured": True,
        "premium_badge": True,
        "social_media_promotion": True,
        "created_date": "2025-09-12",
        "listing_type": "platinum",
        "agent_name": "Anita Kapoor",
        "agent_phone": "9876543221",
        "agent_email": "anita@elitecommercial.com",
        "agency": "Elite Commercial Realty",
        "amenities": ["Central AC", "Power Backup", "High Speed Elevators", "Security", "CCTV", "Fire Safety", "Cafeteria", "Conference Rooms"],
        "nearby": ["Metro Station - 200m", "Bus Stop - 100m", "Bank - 150m", "Restaurant - 50m"],
        "price_per_sqft": 8333,
        "emi_calculator": True,
        "virtual_tour_360": True,
        "drone_photography": True,
        "actions": ["edit", "delete", "view", "promote", "feature", "social_share", "analytics"]
    },
    {
        "id": 3,
        "property_id": "PT003",
        "title": "Premium Villa Estate",
        "description": "Sprawling villa estate with private gardens, swimming pool, and luxurious interiors designed by renowned architects",
        "price": 85000000,
        "location": "Whitefield, Bangalore",
        "city": "Bangalore",
        "state": "Karnataka",
        "type": "villa",
        "status": "active",
        "views": 2890,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg", "photo10.jpg"],
        "video_tour": "virtual_tour_003.mp4",
        "floor_plan": "floor_plan_003.pdf",
        "bedrooms": 5,
        "bathrooms": 6,
        "area": 8000,
        "furnishing": "Fully Furnished",
        "parking": "4 Covered",
        "balconies": 4,
        "contact_visible": True,
        "priority_placement": True,
        "top_search_results": True,
        "verified": True,
        "featured": True,
        "premium_badge": True,
        "social_media_promotion": True,
        "created_date": "2025-09-15",
        "listing_type": "platinum",
        "agent_name": "Rajesh Nair",
        "agent_phone": "9876543222",
        "agent_email": "rajesh@luxuryvillas.com",
        "agency": "Luxury Villas Bangalore",
        "amenities": ["Private Pool", "Garden", "Home Theater", "Wine Cellar", "Gym", "Maid Quarters", "Generator", "Security"],
        "nearby": ["IT Park - 2km", "International School - 1km", "Hospital - 3km", "Shopping Center - 1.5km"],
        "price_per_sqft": 10625,
        "emi_calculator": True,
        "virtual_tour_360": True,
        "drone_photography": True,
        "actions": ["edit", "delete", "view", "promote", "feature", "social_share", "analytics"]
    },
    {
        "id": 4,
        "property_id": "PT004",
        "title": "Luxury Farmhouse Resort",
        "description": "Exclusive farmhouse resort with multiple villas, event spaces, and recreational facilities on 50 acres of pristine land",
        "price": 150000000,
        "location": "Sohna Road, Gurgaon",
        "city": "Gurgaon",
        "state": "Haryana",
        "type": "farmhouse",
        "status": "active",
        "views": 4120,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg", "photo10.jpg"],
        "video_tour": "virtual_tour_004.mp4",
        "floor_plan": "floor_plan_004.pdf",
        "bedrooms": 8,
        "bathrooms": 10,
        "area": 25000,
        "furnishing": "Fully Furnished",
        "parking": "20 Open",
        "balconies": 6,
        "contact_visible": True,
        "priority_placement": True,
        "top_search_results": True,
        "verified": True,
        "featured": True,
        "premium_badge": True,
        "social_media_promotion": True,
        "created_date": "2025-09-18",
        "listing_type": "platinum",
        "agent_name": "Meera Gupta",
        "agent_phone": "9876543223",
        "agent_email": "meera@resortproperties.com",
        "agency": "Resort Properties India",
        "amenities": ["Multiple Pools", "Horse Riding", "Golf Course", "Spa", "Restaurant", "Event Halls", "Lake", "Organic Farm"],
        "nearby": ["Highway Access - 500m", "Resort - 2km", "Golf Club - 1km", "Farmhouse Community - 3km"],
        "price_per_sqft": 6000,
        "emi_calculator": True,
        "virtual_tour_360": True,
        "drone_photography": True,
        "actions": ["edit", "delete", "view", "promote", "feature", "social_share", "analytics"]
    },
    {
        "id": 5,
        "property_id": "PT005",
        "title": "Penthouse with Sky Deck",
        "description": "Magnificent penthouse with private sky deck, infinity pool, and 360-degree views of the city skyline",
        "price": 65000000,
        "location": "Marine Drive, Mumbai",
        "city": "Mumbai",
        "state": "Maharashtra",
        "type": "apartment",
        "status": "active",
        "views": 3890,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg", "photo10.jpg"],
        "video_tour": "virtual_tour_005.mp4",
        "floor_plan": "floor_plan_005.pdf",
        "bedrooms": 4,
        "bathrooms": 5,
        "area": 4500,
        "furnishing": "Designer Furnished",
        "parking": "3 Covered",
        "balconies": 5,
        "contact_visible": True,
        "priority_placement": True,
        "top_search_results": True,
        "verified": True,
        "featured": True,
        "premium_badge": True,
        "social_media_promotion": True,
        "created_date": "2025-09-20",
        "listing_type": "platinum",
        "agent_name": "Arjun Shah",
        "agent_phone": "9876543224",
        "agent_email": "arjun@mumbaiplatinum.com",
        "agency": "Mumbai Platinum Realty",
        "amenities": ["Infinity Pool", "Sky Deck", "Private Elevator", "Jacuzzi", "Home Automation", "Concierge", "Valet", "Wine Storage"],
        "nearby": ["Beach - 100m", "5-Star Hotel - 200m", "Business District - 1km", "Airport - 15km"],
        "price_per_sqft": 14444,
        "emi_calculator": True,
        "virtual_tour_360": True,
        "drone_photography": True,
        "actions": ["edit", "delete", "view", "promote", "feature", "social_share", "analytics"]
    },
    {
        "id": 6,
        "property_id": "PT006",
        "title": "Heritage Mansion",
        "description": "Restored heritage mansion with colonial architecture, sprawling lawns, and modern luxury amenities",
        "price": 95000000,
        "location": "Civil Lines, Delhi",
        "city": "Delhi",
        "state": "Delhi",
        "type": "house",
        "status": "sold",
        "views": 5420,
        "photos": ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg", "photo10.jpg"],
        "video_tour": "virtual_tour_006.mp4",
        "floor_plan": "floor_plan_006.pdf",
        "bedrooms": 6,
        "bathrooms": 8,
        "area": 12000,
        "furnishing": "Antique Furnished",
        "parking": "8 Covered",
        "balconies": 4,
        "contact_visible": False,
        "priority_placement": False,
        "top_search_results": False,
        "verified": True,
        "featured": False,
        "premium_badge": False,
        "social_media_promotion": False,
        "created_date": "2025-08-05",
        "listing_type": "platinum",
        "agent_name": "Rohit Sharma",
        "agent_phone": "9876543225",
        "agent_email": "rohit@heritagehomes.com",
        "agency": "Heritage Homes Delhi",
        "amenities": ["Library", "Ballroom", "Servants Quarters", "Garden", "Heritage Architecture", "Wine Cellar", "Study", "Guest House"],
        "nearby": ["Metro Station - 1km", "Club - 500m", "Park - 200m", "Hospital - 2km"],
        "price_per_sqft": 7916,
        "emi_calculator": True,
        "virtual_tour_360": True,
        "drone_photography": True,
        "actions": ["view"]
    }
]

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_platinum_listings(
    city: Optional[str] = Query(None, description="Filter by city"),
    type: Optional[str] = Query(None, description="Filter by property type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    featured: Optional[bool] = Query(None, description="Filter by featured status"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    furnishing: Optional[str] = Query(None, description="Filter by furnishing type"),
    limit: Optional[int] = Query(10, description="Number of listings to return")
):
    """Get platinum listings with premium features and maximum visibility"""
    try:
        filtered_listings = PLATINUM_LISTINGS.copy()
        
        # Apply filters
        if city:
            filtered_listings = [l for l in filtered_listings if l["city"].lower() == city.lower()]
        
        if type:
            filtered_listings = [l for l in filtered_listings if l["type"].lower() == type.lower()]
        
        if status:
            filtered_listings = [l for l in filtered_listings if l["status"].lower() == status.lower()]
            
        if featured is not None:
            filtered_listings = [l for l in filtered_listings if l["featured"] == featured]
            
        if furnishing:
            filtered_listings = [l for l in filtered_listings if furnishing.lower() in l["furnishing"].lower()]
        
        if min_price is not None:
            filtered_listings = [l for l in filtered_listings if l["price"] >= min_price]
            
        if max_price is not None:
            filtered_listings = [l for l in filtered_listings if l["price"] <= max_price]
        
        # Apply limit
        if limit:
            filtered_listings = filtered_listings[:limit]
        
        # Calculate advanced statistics
        total_views = sum([l["views"] for l in PLATINUM_LISTINGS])
        featured_count = len([l for l in PLATINUM_LISTINGS if l["featured"]])
        premium_badge_count = len([l for l in PLATINUM_LISTINGS if l["premium_badge"]])
        avg_price_per_sqft = sum([l["price_per_sqft"] for l in PLATINUM_LISTINGS]) // len(PLATINUM_LISTINGS)
        
        return {
            "success": True,
            "message": "Platinum listings retrieved successfully",
            "data": filtered_listings,
            "count": len(filtered_listings),
            "total_available": len(PLATINUM_LISTINGS),
            "statistics": {
                "total_views": total_views,
                "featured_listings": featured_count,
                "premium_badge_listings": premium_badge_count,
                "average_price_per_sqft": avg_price_per_sqft
            },
            "filters_applied": {
                "city": city,
                "type": type,
                "status": status,
                "featured": featured,
                "furnishing": furnishing,
                "min_price": min_price,
                "max_price": max_price,
                "limit": limit
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving platinum listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/dashboard", response_model=dict)
async def get_platinum_dashboard():
    """Get platinum listings dashboard data with premium features overview"""
    try:
        total_listings = len(PLATINUM_LISTINGS)
        active_listings = len([l for l in PLATINUM_LISTINGS if l["status"] == "active"])
        featured_listings = len([l for l in PLATINUM_LISTINGS if l["featured"]])
        premium_badge_listings = len([l for l in PLATINUM_LISTINGS if l["premium_badge"]])
        social_promotion_listings = len([l for l in PLATINUM_LISTINGS if l["social_media_promotion"]])
        views_this_month = sum([l["views"] for l in PLATINUM_LISTINGS if l["created_date"].startswith("2025-10")])
        total_views = sum([l["views"] for l in PLATINUM_LISTINGS])
        
        # Calculate average price per sqft
        avg_price_per_sqft = sum([l["price_per_sqft"] for l in PLATINUM_LISTINGS]) // len(PLATINUM_LISTINGS)
        
        # Format listings for dashboard
        formatted_listings = []
        for listing in PLATINUM_LISTINGS:
            formatted_listings.append({
                "property_id": listing["property_id"],
                "title": listing["title"],
                "location": f"{listing['location']}, {listing['city']}",
                "price": f"₹{listing['price']:,}",
                "price_per_sqft": f"₹{listing['price_per_sqft']:,}",
                "status": listing["status"],
                "views": listing["views"],
                "featured": listing["featured"],
                "premium_badge": listing["premium_badge"],
                "virtual_tour_360": listing["virtual_tour_360"],
                "drone_photography": listing["drone_photography"],
                "actions": listing["actions"]
            })
        
        return {
            "success": True,
            "message": "Platinum listings dashboard data retrieved successfully",
            "dashboard": {
                "total_platinum_listings": total_listings,
                "active_listings": active_listings,
                "featured_listings": featured_listings,
                "premium_badge_listings": premium_badge_listings,
                "social_promotion_listings": social_promotion_listings,
                "views_this_month": views_this_month,
                "total_views": total_views,
                "average_price_per_sqft": avg_price_per_sqft,
                "features": {
                    "unlimited_photos": "Up to 20 photos",
                    "video_tours": True,
                    "virtual_tour_360": True,
                    "drone_photography": True,
                    "floor_plans": True,
                    "priority_placement": True,
                    "top_search_results": True,
                    "premium_badge": True,
                    "social_media_promotion": True,
                    "emi_calculator": True,
                    "detailed_analytics": True,
                    "agent_contact_details": True
                }
            },
            "listings": formatted_listings,
            "count": len(formatted_listings)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving platinum dashboard data: {str(e)}",
            "dashboard": {},
            "listings": []
        }

@router.get("/featured", response_model=dict)
async def get_featured_platinum_listings():
    """Get featured platinum listings with premium placement"""
    try:
        featured_listings = [l for l in PLATINUM_LISTINGS if l["featured"] and l["status"] == "active"]
        
        return {
            "success": True,
            "message": "Featured platinum listings retrieved successfully",
            "data": featured_listings,
            "count": len(featured_listings)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving featured platinum listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/premium-badge", response_model=dict)
async def get_premium_badge_listings():
    """Get listings with premium badge status"""
    try:
        premium_listings = [l for l in PLATINUM_LISTINGS if l["premium_badge"] and l["status"] == "active"]
        
        return {
            "success": True,
            "message": "Premium badge listings retrieved successfully",
            "data": premium_listings,
            "count": len(premium_listings)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving premium badge listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/analytics", response_model=dict)
async def get_platinum_analytics():
    """Get comprehensive analytics for platinum listings"""
    try:
        total_listings = len(PLATINUM_LISTINGS)
        active_listings = len([l for l in PLATINUM_LISTINGS if l["status"] == "active"])
        sold_listings = len([l for l in PLATINUM_LISTINGS if l["status"] == "sold"])
        
        # Performance metrics
        total_views = sum([l["views"] for l in PLATINUM_LISTINGS])
        avg_views = total_views // len(PLATINUM_LISTINGS) if PLATINUM_LISTINGS else 0
        top_viewed = max(PLATINUM_LISTINGS, key=lambda x: x["views"]) if PLATINUM_LISTINGS else None
        
        # Price analytics
        prices = [l["price"] for l in PLATINUM_LISTINGS if l["status"] == "active"]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        avg_price = sum(prices) // len(prices) if prices else 0
        
        # Price per sqft analytics
        price_per_sqft_values = [l["price_per_sqft"] for l in PLATINUM_LISTINGS if l["status"] == "active"]
        avg_price_per_sqft = sum(price_per_sqft_values) // len(price_per_sqft_values) if price_per_sqft_values else 0
        
        # Feature adoption
        virtual_tour_count = len([l for l in PLATINUM_LISTINGS if l["virtual_tour_360"]])
        drone_photo_count = len([l for l in PLATINUM_LISTINGS if l["drone_photography"]])
        social_promotion_count = len([l for l in PLATINUM_LISTINGS if l["social_media_promotion"]])
        
        # Geographic distribution
        city_distribution = {}
        for listing in PLATINUM_LISTINGS:
            city = listing["city"]
            city_distribution[city] = city_distribution.get(city, 0) + 1
        
        # Type distribution
        type_distribution = {}
        for listing in PLATINUM_LISTINGS:
            prop_type = listing["type"]
            type_distribution[prop_type] = type_distribution.get(prop_type, 0) + 1
        
        return {
            "success": True,
            "message": "Platinum listings analytics retrieved successfully",
            "data": {
                "overview": {
                    "total_listings": total_listings,
                    "active_listings": active_listings,
                    "sold_listings": sold_listings
                },
                "performance": {
                    "total_views": total_views,
                    "average_views": avg_views,
                    "top_viewed_property": top_viewed["title"] if top_viewed else None,
                    "top_viewed_views": top_viewed["views"] if top_viewed else 0
                },
                "pricing": {
                    "min_price": min_price,
                    "max_price": max_price,
                    "average_price": avg_price,
                    "average_price_per_sqft": avg_price_per_sqft
                },
                "features": {
                    "virtual_tours": virtual_tour_count,
                    "drone_photography": drone_photo_count,
                    "social_media_promotion": social_promotion_count
                },
                "distribution": {
                    "by_city": city_distribution,
                    "by_type": type_distribution
                }
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving platinum analytics: {str(e)}",
            "data": {}
        }

@router.get("/{listing_id}", response_model=dict)
async def get_platinum_listing_by_id(listing_id: int):
    """Get a specific platinum listing with all premium details"""
    try:
        listing = next((l for l in PLATINUM_LISTINGS if l["id"] == listing_id), None)
        
        if not listing:
            raise HTTPException(status_code=404, detail="Platinum listing not found")
        
        return {
            "success": True,
            "message": "Platinum listing retrieved successfully",
            "data": listing
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving platinum listing: {str(e)}",
            "data": None
        }