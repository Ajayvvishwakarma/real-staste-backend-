from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

router = APIRouter()

# Sample listings data (same as properties for now)
SAMPLE_LISTINGS = [
    {
        "id": 1,
        "title": "Luxury 3BHK Apartment",
        "description": "Spacious 3BHK apartment with modern amenities",
        "property_type": "apartment",
        "price": 15000000,
        "area": 1200,
        "bedrooms": 3,
        "bathrooms": 2,
        "address": "Sector 62, Noida",
        "city": "Noida",
        "state": "Uttar Pradesh",
        "pincode": "201301",
        "status": "available",
        "is_featured": True,
        "listing_type": "sale",
        "agent_contact": "9876543210"
    },
    {
        "id": 2,
        "title": "2BHK Builder Floor",
        "description": "Well-ventilated 2BHK builder floor",
        "property_type": "house",
        "price": 8500000,
        "area": 900,
        "bedrooms": 2,
        "bathrooms": 2,
        "address": "Lajpat Nagar, Delhi",
        "city": "Delhi",
        "state": "Delhi",
        "pincode": "110024",
        "status": "available",
        "is_featured": False,
        "listing_type": "sale",
        "agent_contact": "9876543211"
    },
    {
        "id": 3,
        "title": "Commercial Office Space",
        "description": "Modern office space in business district",
        "property_type": "commercial",
        "price": 25000000,
        "area": 2000,
        "bedrooms": 0,
        "bathrooms": 4,
        "address": "Cyber City, Gurgaon",
        "city": "Gurgaon",
        "state": "Haryana",
        "pincode": "122001",
        "status": "available",
        "is_featured": True,
        "listing_type": "rent",
        "agent_contact": "9876543212"
    },
    {
        "id": 4,
        "title": "Farmhouse for Rent",
        "description": "Spacious farmhouse with garden",
        "property_type": "farmhouse",
        "price": 50000,
        "area": 5000,
        "bedrooms": 4,
        "bathrooms": 3,
        "address": "Manesar, Gurgaon",
        "city": "Gurgaon",
        "state": "Haryana",
        "pincode": "122001",
        "status": "available",
        "is_featured": False,
        "listing_type": "rent",
        "agent_contact": "9876543213"
    },
    {
        "id": 5,
        "title": "Studio Apartment",
        "description": "Compact studio apartment for young professionals",
        "property_type": "apartment",
        "price": 2500000,
        "area": 400,
        "bedrooms": 1,
        "bathrooms": 1,
        "address": "Koramangala, Bangalore",
        "city": "Bangalore",
        "state": "Karnataka",
        "pincode": "560034",
        "status": "available",
        "is_featured": False,
        "listing_type": "sale",
        "agent_contact": "9876543214"
    }
]

@router.get("", response_model=dict)
@router.get("/", response_model=dict)
async def get_listings(
    city: Optional[str] = Query(None, description="Filter by city"),
    property_type: Optional[str] = Query(None, description="Filter by property type"),
    listing_type: Optional[str] = Query(None, description="Filter by listing type (sale/rent)"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    limit: Optional[int] = Query(10, description="Number of listings to return")
):
    """Get property listings with optional filters"""
    try:
        filtered_listings = SAMPLE_LISTINGS.copy()
        
        # Apply filters
        if city:
            filtered_listings = [l for l in filtered_listings if l["city"].lower() == city.lower()]
        
        if property_type:
            filtered_listings = [l for l in filtered_listings if l["property_type"].lower() == property_type.lower()]
            
        if listing_type:
            filtered_listings = [l for l in filtered_listings if l["listing_type"].lower() == listing_type.lower()]
        
        if min_price is not None:
            filtered_listings = [l for l in filtered_listings if l["price"] >= min_price]
            
        if max_price is not None:
            filtered_listings = [l for l in filtered_listings if l["price"] <= max_price]
        
        # Apply limit
        if limit:
            filtered_listings = filtered_listings[:limit]
        
        return {
            "success": True,
            "message": "Listings retrieved successfully",
            "data": filtered_listings,
            "count": len(filtered_listings),
            "total_available": len(SAMPLE_LISTINGS),
            "filters_applied": {
                "city": city,
                "property_type": property_type,
                "listing_type": listing_type,
                "min_price": min_price,
                "max_price": max_price,
                "limit": limit
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/{listing_id}", response_model=dict)
async def get_listing_by_id(listing_id: int):
    """Get a specific listing by ID"""
    try:
        listing = next((l for l in SAMPLE_LISTINGS if l["id"] == listing_id), None)
        
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        
        return {
            "success": True,
            "message": "Listing retrieved successfully",
            "data": listing
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving listing: {str(e)}",
            "data": None
        }

@router.get("/featured/list", response_model=dict)
async def get_featured_listings():
    """Get featured property listings"""
    try:
        featured_listings = [l for l in SAMPLE_LISTINGS if l.get("is_featured", False)]
        
        return {
            "success": True,
            "message": "Featured listings retrieved successfully",
            "data": featured_listings,
            "count": len(featured_listings)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving featured listings: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/search/by-city/{city}", response_model=dict)
async def get_listings_by_city(city: str):
    """Get listings by city name"""
    try:
        city_listings = [l for l in SAMPLE_LISTINGS if l["city"].lower() == city.lower()]
        
        return {
            "success": True,
            "message": f"Listings for {city} retrieved successfully",
            "data": city_listings,
            "count": len(city_listings),
            "city": city
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving listings for {city}: {str(e)}",
            "data": [],
            "count": 0
        }

@router.get("/types/available", response_model=dict)
async def get_available_listing_types():
    """Get available property types and listing types"""
    try:
        property_types = list(set([l["property_type"] for l in SAMPLE_LISTINGS]))
        listing_types = list(set([l["listing_type"] for l in SAMPLE_LISTINGS]))
        cities = list(set([l["city"] for l in SAMPLE_LISTINGS]))
        
        return {
            "success": True,
            "message": "Available listing types retrieved successfully",
            "data": {
                "property_types": property_types,
                "listing_types": listing_types,
                "cities": cities,
                "total_listings": len(SAMPLE_LISTINGS)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving listing types: {str(e)}",
            "data": {}
        }